"""
FastAPI Auto CRUD Application
=============================
Automatically discovers models and schemas from folders and generates CRUD APIs.

Project Structure:
- models/     -> SQLAlchemy models (User, Admin, Employee)
- schemas/    -> Pydantic schemas (Create, Update, Response)
- database.py -> Database configuration
- auto_crud.py -> Auto CRUD magic
- main.py     -> This file (FastAPI app)

Usage:
1. Run: python main.py
2. Visit: http://localhost:8000/docs
3. All CRUD APIs automatically available!
"""

from fastapi import FastAPI
import auto_crud

# Create FastAPI application
app = FastAPI(
    title="Auto CRUD API",
    description="Automatically generated CRUD APIs from models and schemas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Auto-discover models and schemas from folders and generate CRUD APIs
auto_crud.setup(
    app=app,
    models_folder="models",
    schemas_folder="schemas", 
    create_tables=True
)

@app.get("/")
def root():
    return {
        "message": "🚀 Auto CRUD API",
        "info": "CRUD APIs automatically generated from models and schemas",
        "project_structure": {
            "models": "SQLAlchemy models in models/ folder",
            "schemas": "Pydantic schemas in schemas/ folder",
            "auto_discovery": "Automatically finds and matches models with schemas"
        },
        "available_endpoints": {
            "users": "/users/ - User management",
            "admins": "/admins/ - Admin management", 
            "employees": "/employees/ - Employee management"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "features": [
            "✅ Auto model discovery",
            "✅ Auto schema matching", 
            "✅ Complete CRUD operations",
            "✅ Pagination support",
            "✅ Error handling",
            "✅ Type validation"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Auto CRUD API is running"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Auto CRUD API...")
    print("📖 Visit http://localhost:8000/docs for interactive documentation")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)