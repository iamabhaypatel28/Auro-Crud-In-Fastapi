"""
Auto CRUD Module
================
Complete auto-CRUD system for FastAPI with SQLAlchemy.
Automatically discovers models and schemas from folders and generates CRUD APIs!

Usage:
1. Put SQLAlchemy models in 'models/' folder
2. Put Pydantic schemas in 'schemas/' folder  
3. Call auto_crud.setup(app) from main.py
4. All CRUD APIs are automatically generated!

Features:
- Auto-discovery of models and schemas from folders
- Automatic CRUD API generation
- Database table creation
- Complete CRUD operations (Create, Read, Update, Delete)
- Pagination support
- Error handling
- Proper FastAPI project structure
"""

import inspect
import importlib
import pkgutil
import os
import sys
from pathlib import Path
from typing import Type, TypeVar, Optional, List, Any, Dict
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, APIRouter, Query
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, create_model

ModelType = TypeVar("ModelType")

class AutoCRUD:
    def __init__(self):
        self.models = {}
        self.schemas = {}
        
    def setup(self, app: FastAPI, models_folder: str = "models", schemas_folder: str = "schemas", create_tables: bool = True):
        """
        Setup auto CRUD system with folder-based discovery
        
        Args:
            app: FastAPI application instance
            models_folder: Folder containing SQLAlchemy models
            schemas_folder: Folder containing Pydantic schemas
            create_tables: Whether to create tables automatically
        """
        # Import database from the project
        try:
            from database import Base, engine, get_db
            self.Base = Base
            self.engine = engine
            self.get_db = get_db
        except ImportError:
            raise ImportError("Please create database.py with Base, engine, and get_db")
        
        # Auto-discover models and schemas from folders
        self._discover_models_from_folder(models_folder)
        self._discover_schemas_from_folder(schemas_folder)
        
        # Match models with schemas
        self._match_models_with_schemas()
        
        # Create tables
        if create_tables:
            self.Base.metadata.create_all(bind=self.engine)
            
        # Generate CRUD routes
        self._generate_all_routes(app)
        
        print(f"✅ Auto CRUD setup complete!")
        print(f"📊 Discovered {len(self.models)} models")
        print(f"📋 Found {len(self.schemas)} schema sets")
        print(f"🚀 Generated CRUD APIs for: {list(self.models.keys())}")
    
    def _discover_models_from_folder(self, folder_name: str):
        """Discover SQLAlchemy models from folder"""
        if not os.path.exists(folder_name):
            print(f"⚠️  Models folder '{folder_name}' not found")
            return
            
        # Add current directory to Python path
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import all Python files from models folder
        for file_path in Path(folder_name).glob("*.py"):
            if file_path.name.startswith("__"):
                continue
                
            module_name = f"{folder_name}.{file_path.stem}"
            try:
                module = importlib.import_module(module_name)
                
                # Find SQLAlchemy models in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        hasattr(obj, '__tablename__') and 
                        isinstance(obj, DeclarativeMeta)):
                        
                        model_key = file_path.stem.lower()  # Use filename as key
                        self.models[model_key] = {
                            'db_model': obj,
                            'table_name': obj.__tablename__,
                            'class_name': name
                        }
                        print(f"📋 Found model: {name} -> /{model_key}s")
                        
            except Exception as e:
                print(f"⚠️  Error importing {module_name}: {e}")
    
    def _discover_schemas_from_folder(self, folder_name: str):
        """Discover Pydantic schemas from folder"""
        if not os.path.exists(folder_name):
            print(f"⚠️  Schemas folder '{folder_name}' not found")
            return
            
        # Add current directory to Python path
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import all Python files from schemas folder
        for file_path in Path(folder_name).glob("*.py"):
            if file_path.name.startswith("__"):
                continue
                
            module_name = f"{folder_name}.{file_path.stem}"
            try:
                module = importlib.import_module(module_name)
                
                schema_key = file_path.stem.lower()
                schemas = {}
                
                # Find Pydantic models in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BaseModel) and 
                        obj != BaseModel):
                        
                        name_lower = name.lower()
                        if 'create' in name_lower:
                            schemas['create'] = obj
                        elif 'update' in name_lower:
                            schemas['update'] = obj
                        elif 'response' in name_lower:
                            schemas['response'] = obj
                        elif 'base' in name_lower:
                            schemas['base'] = obj
                
                if schemas:
                    self.schemas[schema_key] = schemas
                    print(f"📋 Found schemas for {schema_key}: {list(schemas.keys())}")
                    
            except Exception as e:
                print(f"⚠️  Error importing {module_name}: {e}")
    
    def _match_models_with_schemas(self):
        """Match discovered models with their corresponding schemas"""
        matched_models = {}
        
        for model_key, model_info in self.models.items():
            if model_key in self.schemas:
                schema_info = self.schemas[model_key]
                
                # Ensure we have the required schemas
                if 'create' in schema_info and 'update' in schema_info and 'response' in schema_info:
                    matched_models[model_key] = {
                        **model_info,
                        'schemas': schema_info
                    }
                    print(f"✅ Matched {model_key} with existing schemas")
                else:
                    print(f"⚠️  {model_key} missing required schemas, auto-generating...")
                    auto_schemas = self._auto_generate_schemas(model_key, model_info['db_model'])
                    matched_models[model_key] = {
                        **model_info,
                        'schemas': auto_schemas
                    }
                    print(f"✅ Auto-generated schemas for {model_key}")
            else:
                print(f"📋 No schemas found for {model_key}, auto-generating...")
                auto_schemas = self._auto_generate_schemas(model_key, model_info['db_model'])
                matched_models[model_key] = {
                    **model_info,
                    'schemas': auto_schemas
                }
                print(f"✅ Auto-generated schemas for {model_key}")
        
        self.models = matched_models
    
    def _auto_generate_schemas(self, model_name: str, db_model: Type):
        """Auto-generate Pydantic schemas from SQLAlchemy model"""
        
        # Get model fields
        fields = {}
        create_fields = {}
        update_fields = {}
        
        for column in db_model.__table__.columns:
            field_name = column.name
            python_type = self._sqlalchemy_to_python_type(column.type)
            
            # For response schema
            if column.primary_key:
                # Primary keys (ID) should be required in response
                fields[field_name] = (str, ...)
            elif column.nullable:
                fields[field_name] = (Optional[python_type], None)
            else:
                fields[field_name] = (python_type, ...)
            
            # For create schema
            if not column.primary_key and not self._is_auto_field(column):
                if column.nullable or column.default is not None:
                    create_fields[field_name] = (Optional[python_type], column.default)
                else:
                    create_fields[field_name] = (python_type, ...)
            
            # For update schema (all optional)
            if not column.primary_key:
                update_fields[field_name] = (Optional[python_type], None)
        
        # Create Pydantic models
        ResponseModel = create_model(
            f"{model_name.capitalize()}Response",
            **fields,
            __config__=type('Config', (), {
                'from_attributes': True,
                'json_encoders': {
                    'UUID': str
                }
            })
        )
        
        CreateModel = create_model(f"{model_name.capitalize()}Create", **create_fields)
        UpdateModel = create_model(f"{model_name.capitalize()}Update", **update_fields)
        
        return {
            'response': ResponseModel,
            'create': CreateModel,
            'update': UpdateModel
        }
    
    def _sqlalchemy_to_python_type(self, column_type):
        """Convert SQLAlchemy column type to Python type"""
        type_mapping = {
            'VARCHAR': str,
            'TEXT': str,
            'STRING': str,
            'INTEGER': int,
            'BIGINT': int,
            'FLOAT': float,
            'REAL': float,
            'BOOLEAN': bool,
            'DATETIME': datetime,
            'UUID': str,
        }
        
        column_type_str = str(column_type).upper()
        for sql_type, python_type in type_mapping.items():
            if sql_type in column_type_str:
                return python_type
        
        return str  # Default to string
    
    def _is_auto_field(self, column):
        """Check if field is auto-generated"""
        return (column.primary_key or 
                column.default is not None or 
                column.server_default is not None or
                'created_at' in column.name.lower() or
                'updated_at' in column.name.lower())
    
    def _generate_all_routes(self, app: FastAPI):
        """Generate CRUD routes for all discovered models"""
        for model_name, model_config in self.models.items():
            router = self._create_crud_router(model_name, model_config)
            app.include_router(router)
    
    def _serialize_db_item(self, db_item, db_model):
        """Convert database item to serializable dict"""
        result = {}
        for column in db_model.__table__.columns:
            value = getattr(db_item, column.name)
            
            # Handle UUID objects (convert to string)
            if hasattr(value, 'hex'):  # UUID object
                result[column.name] = str(value)
            # Handle datetime objects
            elif hasattr(value, 'isoformat'):  # datetime object
                result[column.name] = value.isoformat() if value else None
            # Handle None values
            elif value is None:
                result[column.name] = None
            # Handle other types
            else:
                result[column.name] = value
                
        return result
    
    def _handle_integrity_error(self, error: IntegrityError, model_name: str) -> HTTPException:
        """Handle database integrity errors with user-friendly messages"""
        error_msg = str(error.orig)
        
        if "duplicate key value violates unique constraint" in error_msg:
            # Extract field name from constraint name
            if "_email_key" in error_msg:
                return HTTPException(
                    status_code=409, 
                    detail=f"Email already exists. Please use a different email address."
                )
            elif "_username_key" in error_msg:
                return HTTPException(
                    status_code=409, 
                    detail=f"Username already exists. Please choose a different username."
                )
            elif "_employee_id_key" in error_msg:
                return HTTPException(
                    status_code=409, 
                    detail=f"Employee ID already exists. Please use a different employee ID."
                )
            else:
                # Generic unique constraint violation
                return HTTPException(
                    status_code=409, 
                    detail=f"A {model_name} with this information already exists. Please check your input."
                )
        
        elif "violates not-null constraint" in error_msg:
            return HTTPException(
                status_code=400, 
                detail=f"Missing required field. Please provide all required information."
            )
        
        elif "violates foreign key constraint" in error_msg:
            return HTTPException(
                status_code=400, 
                detail=f"Referenced record does not exist. Please check your input."
            )
        
        else:
            # Generic database error
            return HTTPException(
                status_code=400, 
                detail=f"Database error: Unable to process request. Please check your input."
            )
    
    def _create_crud_router(self, model_name: str, model_config: Dict) -> APIRouter:
        """Create CRUD router for a specific model"""
        router = APIRouter(
            prefix=f"/{model_name}s",
            tags=[model_name.capitalize() + "s"]
        )
        
        db_model = model_config['db_model']
        schemas = model_config['schemas']
        
        # CREATE
        @router.post("/", response_model=schemas['response'])
        def create_item(item: schemas['create'], db: Session = Depends(self.get_db)):
            try:
                item_data = item.dict(exclude_unset=True)
                db_item = db_model(**item_data)
                db.add(db_item)
                db.commit()
                db.refresh(db_item)
                
                return self._serialize_db_item(db_item, db_model)
            except IntegrityError as e:
                db.rollback()
                raise self._handle_integrity_error(e, model_name)
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Error creating {model_name}: {str(e)}")
        
        # READ ALL
        @router.get("/", response_model=List[schemas['response']])
        def read_items(
            skip: int = Query(0, ge=0), 
            limit: int = Query(100, ge=1, le=1000),
            db: Session = Depends(self.get_db)
        ):
            items = db.query(db_model).offset(skip).limit(limit).all()
            
            return [self._serialize_db_item(item, db_model) for item in items]
        
        # READ ONE
        @router.get("/{item_id}", response_model=schemas['response'])
        def read_item(item_id: str, db: Session = Depends(self.get_db)):
            item = db.query(db_model).filter(db_model.id == item_id).first()
            if not item:
                raise HTTPException(status_code=404, detail=f"{model_name.capitalize()} not found")
            
            return self._serialize_db_item(item, db_model)
        
        # UPDATE
        @router.put("/{item_id}", response_model=schemas['response'])
        def update_item(item_id: str, item_update: schemas['update'], db: Session = Depends(self.get_db)):
            db_item = db.query(db_model).filter(db_model.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=404, detail=f"{model_name.capitalize()} not found")
            
            try:
                update_data = item_update.dict(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(db_item, field, value)
                
                db.commit()
                db.refresh(db_item)
                
                return self._serialize_db_item(db_item, db_model)
            except IntegrityError as e:
                db.rollback()
                raise self._handle_integrity_error(e, model_name)
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Error updating {model_name}: {str(e)}")
        
        # DELETE
        @router.delete("/{item_id}")
        def delete_item(item_id: str, db: Session = Depends(self.get_db)):
            db_item = db.query(db_model).filter(db_model.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=404, detail=f"{model_name.capitalize()} not found")
            
            try:
                db.delete(db_item)
                db.commit()
                return {"message": f"{model_name.capitalize()} deleted successfully"}
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Error deleting {model_name}: {str(e)}")
        
        return router

# Global instance
auto_crud = AutoCRUD()

# Convenience functions
def setup(app: FastAPI, models_folder: str = "models", schemas_folder: str = "schemas", create_tables: bool = True):
    """Setup auto CRUD system with folder-based discovery"""
    return auto_crud.setup(app, models_folder, schemas_folder, create_tables)