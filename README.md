# 🚀 Auto CRUD - Universal FastAPI CRUD Generator

**Intelligent FastAPI module that automatically generates complete CRUD APIs from your SQLAlchemy models**

✨ **Just copy one file and get instant CRUD APIs for any project!**

🎯 **Key Features:**
- 🔥 **Single File Solution** - Copy `auto_crud.py` to any project
- 🧠 **Smart Auto-Detection** - Finds all models automatically 
- ⚡ **Schemas Optional** - Auto-generates if not provided
- 🚀 **Zero Configuration** - Works out of the box
- 📊 **Complete CRUD** - Create, Read, Update, Delete + Pagination
- 🛡️ **Production Ready** - Error handling, validation, documentation

## 📁 Project Structure

```
project/
├── main.py              # Main FastAPI application
├── database.py          # Database configuration
├── auto_crud.py         # Auto CRUD magic module ✨
├── requirements.txt     # Dependencies
├── models/              # SQLAlchemy Models
│   ├── __init__.py
│   ├── user.py         # User model
│   ├── admin.py        # Admin model
│   └── employee.py     # Employee model
└── schemas/             # Pydantic Schemas
    ├── __init__.py
    ├── user.py         # User schemas (Create, Update, Response)
    ├── admin.py        # Admin schemas
    └── employee.py     # Employee schemas
```

## 🚀 Quick Start - Current Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Update Database Connection
```python
# database.py mein apna database URL update karo
DATABASE_URL = "postgresql://username:password@localhost:5432/your_database"
```

### 3. Run Application
```bash
python main.py
```

### 4. Access APIs
- **API Documentation:** http://localhost:8000/docs
- **Root endpoint:** http://localhost:8000/

---

# 🔥 Use Auto CRUD in Any Project

## 📦 Single File Integration

### ✨ Copy Just One File!

**Step 1:** Copy the magic file
```bash
cp auto_crud.py /path/to/your/new/project/
```

**Step 2:** Install dependencies in your project
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic email-validator
```

**Step 3:** Create required `database.py`
```python
# database.py (MANDATORY)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/your_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Step 4:** Create your project structure
```
your_new_project/
├── auto_crud.py       # ✨ The copied magic file
├── database.py        # ✅ Required database config
├── main.py           # ✅ Your FastAPI app
├── models/           # ✅ Your SQLAlchemy models
│   ├── __init__.py
│   ├── product.py
│   ├── category.py
│   └── order.py
└── schemas/          # ⚡ Optional (auto-generated if missing)
    ├── __init__.py
    └── product.py    # Custom schemas (optional)
```

**Step 5:** Create your models
```python
# models/product.py
from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from database import Base  # ✅ Import from YOUR database.py
import uuid

class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
```

```python
# models/category.py
from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
```

**Step 6:** Setup in your `main.py` (Just 3 lines!)
```python
# main.py
from fastapi import FastAPI
import auto_crud  # ✨ Import the magic file

app = FastAPI(title="My Auto CRUD API")

# 🚀 That's it! Auto-generate CRUD APIs for ALL models
auto_crud.setup(
    app=app,
    models_folder="models",        # Your models folder
    schemas_folder="schemas",      # Optional - auto-generates if missing
    create_tables=True            # Creates database tables automatically
)

@app.get("/")
def root():
    return {"message": "My Auto CRUD API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Step 7:** Run and enjoy!
```bash
python main.py
# Visit: http://localhost:8000/docs
```

## 🎉 What Happens Automatically

### ✅ **Auto-Discovery:**
- Finds **all models** in `models/` folder
- Detects **existing schemas** in `schemas/` folder  
- **Auto-generates missing schemas** from SQLAlchemy models

### ✅ **Generated APIs (for each model):**
```
POST   /products/     - Create product
GET    /products/     - Get all products (with pagination ?skip=0&limit=10)
GET    /products/{id} - Get product by ID
PUT    /products/{id} - Update product
DELETE /products/{id} - Delete product

POST   /categories/     - Create category
GET    /categories/     - Get all categories
GET    /categories/{id} - Get category by ID
PUT    /categories/{id} - Update category
DELETE /categories/{id} - Delete category

# ... and so on for ALL your models!
```

### ✅ **Console Output:**
```bash
📋 Found model: Product -> /products
📋 Found model: Category -> /categories
📋 Found model: Order -> /orders
⚠️  Schemas folder 'schemas' not found
📋 No schemas found for product, auto-generating...
✅ Auto-generated schemas for product
📋 No schemas found for category, auto-generating...
✅ Auto-generated schemas for category
📋 No schemas found for order, auto-generating...
✅ Auto-generated schemas for order
✅ Auto CRUD setup complete!
📊 Discovered 3 models
🚀 Generated CRUD APIs for: ['product', 'category', 'order']
```

## 🎯 Requirements & Rules

### ✅ **MANDATORY Requirements:**
1. **`auto_crud.py`** - The main file (copy this)
2. **`database.py`** - Must have `Base`, `engine`, `get_db`
3. **`models/` folder** - Contains your SQLAlchemy models
4. **Model structure:**
   - Must inherit from `Base` 
   - Must have `id` field as primary key (UUID recommended)
   - Must have `__tablename__` defined

### ⚡ **OPTIONAL:**
1. **`schemas/` folder** - Custom Pydantic schemas (auto-generated if missing)
2. **Custom validation** - Add your own field validators

### 📋 **Model Requirements:**
```python
# ✅ CORRECT Model Structure
class YourModel(Base):  # ✅ Inherit from Base
    __tablename__ = "your_table"  # ✅ Table name required
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # ✅ ID required
    name = Column(String(100), nullable=False)  # ✅ Other fields
    # ... more fields

# ❌ WRONG - Missing requirements
class BadModel:  # ❌ No Base inheritance
    name = Column(String(100))  # ❌ No ID field, no __tablename__
```

## 📋 Schema Naming Convention

Auto CRUD expects specific schema names:

```python
# schemas/model_name.py
class ModelNameCreate(BaseModel):     # For POST requests
    # required fields

class ModelNameUpdate(BaseModel):     # For PUT requests  
    # optional fields

class ModelNameResponse(BaseModel):   # For API responses
    # all fields including id, timestamps
    
    class Config:
        from_attributes = True
```

## 🔧 Requirements

### Essential Files:
1. `auto_crud.py` - Main auto CRUD module
2. `database.py` - Database configuration  
3. `models/` folder - SQLAlchemy models
4. `schemas/` folder - Pydantic schemas

### Dependencies:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic email-validator
```

## ✨ Enhanced Features

- **🔍 Auto Discovery:** Automatically finds models and schemas from folders
- **🚀 Instant CRUD:** Complete REST APIs without writing code
- **🧠 Smart Schema Generation:** Auto-creates schemas from models if not provided
- **📊 Pagination:** Built-in pagination support (`?skip=0&limit=10`)
- **🛡️ Validation:** Full Pydantic validation and error handling
- **📝 Documentation:** Automatic FastAPI docs generation
- **🔄 Hot Reload:** Add new model, get instant CRUD APIs
- **⚡ Flexible:** Works with or without custom schemas

## 🎯 Generated APIs

For each model, automatically generates:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/model_names/` | Create new record |
| GET | `/model_names/` | Get all records (paginated) |
| GET | `/model_names/{id}` | Get record by ID |
| PUT | `/model_names/{id}` | Update record |
| DELETE | `/model_names/{id}` | Delete record |

## 💡 Smart Features

### 🧠 **Automatic Error Handling:**
```json
// Instead of ugly database errors, you get:
{
  "detail": "Email already exists. Please use a different email address."
}
```

### 🔧 **Built-in Validation:**
- **UUID fields** automatically converted to strings
- **Datetime fields** properly formatted
- **Unique constraints** handled with user-friendly messages
- **Required fields** validated automatically

### 📊 **Pagination Support:**
```bash
GET /products/?skip=0&limit=10  # First 10 products
GET /products/?skip=10&limit=5  # Next 5 products
```

### 🎯 **HTTP Status Codes:**
- **200** - Success
- **201** - Created  
- **400** - Bad Request (validation error)
- **404** - Not Found
- **409** - Conflict (duplicate data)

## 🚨 Important Rules & Tips

### ✅ **MUST Follow:**
1. **Model filename** = **Schema filename** (if using custom schemas)
2. **Models must inherit from `Base`**
3. **Models must have `id` primary key field**
4. **Database.py must exist** with `Base`, `engine`, `get_db`
5. **Models folder structure:** `models/model_name.py`

### 💡 **Best Practices:**
1. **Use UUID for primary keys** - Better for distributed systems
2. **Add `created_at`/`updated_at`** - Auto-excluded from create schema
3. **Use descriptive model names** - Becomes API endpoint names
4. **Keep models in separate files** - Better organization

### ⚠️ **Common Issues:**
```python
# ❌ WRONG - Will not work
class Product:  # Missing Base inheritance
    name = Column(String)  # Missing id, __tablename__

# ❌ WRONG - Will not work  
class Product(Base):
    name = Column(String)  # Missing id and __tablename__

# ✅ CORRECT - Will work perfectly
class Product(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
```

## 🎯 Usage Scenarios

### Scenario 1: Only Models (No Schemas) ✨ NEW
```python
# Just create models, schemas auto-generated!
# models/product.py
class Product(Base):
    __tablename__ = "products"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price = Column(Float)

# No schemas folder needed! Auto CRUD will generate:
# - ProductCreate schema
# - ProductUpdate schema  
# - ProductResponse schema
```

### Scenario 2: Models + Custom Schemas (Full Control)
```python
# Custom schemas for fine control
# schemas/product.py
class ProductCreate(BaseModel):
    name: str
    price: float
    
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    
class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    class Config:
        from_attributes = True
```

### Scenario 3: Mixed (Some Custom, Some Auto) ⚡
```python
# Some models have custom schemas, others don't
# Auto CRUD handles both automatically!
models/
├── user.py        # Has custom schemas in schemas/user.py
├── product.py     # No schemas - will auto-generate
└── category.py    # No schemas - will auto-generate

schemas/
└── user.py        # Only user has custom schemas
```

## 🎉 Enhanced Example Output

### With Mixed Schemas:
```bash
📋 Found model: User -> /users
📋 Found model: Product -> /products  
📋 Found schemas for user: ['create', 'update', 'response']
⚠️  Schemas folder 'schemas' not found
✅ Matched user with existing schemas
📋 No schemas found for product, auto-generating...
✅ Auto-generated schemas for product
✅ Auto CRUD setup complete!
📊 Discovered 2 models
🚀 Generated CRUD APIs for: ['user', 'product']
```

### With Only Models:
```bash
📋 Found model: Product -> /products
📋 Found model: Category -> /categories
⚠️  Schemas folder 'schemas' not found
📋 No schemas found for product, auto-generating...
✅ Auto-generated schemas for product
📋 No schemas found for category, auto-generating...
✅ Auto-generated schemas for category
✅ Auto CRUD setup complete!
📊 Discovered 2 models
🚀 Generated CRUD APIs for: ['product', 'category']
```

Ready to use at: http://localhost:8000/docs

---

## 🚀 Real-World Example

### Complete E-commerce Project Setup:

**1. Copy auto_crud.py:**
```bash
cp auto_crud.py /path/to/ecommerce-project/
cd /path/to/ecommerce-project/
```

**2. Install dependencies:**
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic email-validator
```

**3. Create database.py:**
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/ecommerce")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**4. Create models:**
```bash
mkdir -p models
touch models/__init__.py
```

```python
# models/user.py
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(100))
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

```python
# models/product.py
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from datetime import datetime
import uuid

class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    category = Column(String(100))
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

```python
# models/order.py
from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from datetime import datetime
import uuid

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, completed, cancelled
    shipping_address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**5. Create main.py (3 lines!):**
```python
# main.py
from fastapi import FastAPI
import auto_crud

app = FastAPI(title="E-commerce Auto CRUD API", version="1.0.0")

# 🚀 Auto-generate CRUD APIs for ALL models
auto_crud.setup(
    app=app,
    models_folder="models",
    schemas_folder="schemas",  # Will auto-generate since folder doesn't exist
    create_tables=True         # Creates all database tables
)

@app.get("/")
def root():
    return {
        "message": "E-commerce Auto CRUD API",
        "endpoints": [
            "/users/ - User management",
            "/products/ - Product catalog", 
            "/orders/ - Order processing",
            "/docs - API documentation"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**6. Run and get complete e-commerce API:**
```bash
python main.py
```

**🎉 Result - Complete E-commerce API:**
```
POST   /users/         - Register user
GET    /users/         - Get all users
GET    /users/{id}     - Get user profile  
PUT    /users/{id}     - Update user
DELETE /users/{id}     - Delete user

POST   /products/      - Add product
GET    /products/      - Browse products (with pagination)
GET    /products/{id}  - Get product details
PUT    /products/{id}  - Update product
DELETE /products/{id}  - Remove product

POST   /orders/        - Create order
GET    /orders/        - Get all orders
GET    /orders/{id}    - Get order details
PUT    /orders/{id}    - Update order status
DELETE /orders/{id}    - Cancel order

GET    /docs           - Interactive API documentation
```

**Console Output:**
```bash
📋 Found model: User -> /users
📋 Found model: Product -> /products
📋 Found model: Order -> /orders
⚠️  Schemas folder 'schemas' not found
📋 No schemas found for user, auto-generating...
✅ Auto-generated schemas for user
📋 No schemas found for product, auto-generating...
✅ Auto-generated schemas for product
📋 No schemas found for order, auto-generating...
✅ Auto-generated schemas for order
✅ Auto CRUD setup complete!
📊 Discovered 3 models
🚀 Generated CRUD APIs for: ['user', 'product', 'order']
```

Visit: **http://localhost:8000/docs** - Complete interactive API documentation!

---

## 🎯 Summary

### ✨ **What You Get:**
- **Copy 1 file** → Get complete CRUD APIs
- **Zero configuration** → Works out of the box
- **Smart auto-detection** → Finds all models automatically
- **Auto-generated schemas** → No manual Pydantic coding
- **Production ready** → Error handling, validation, documentation
- **Universal compatibility** → Works in any FastAPI project

### 🔥 **Why Use Auto CRUD:**
- **Save 90% development time** - No repetitive CRUD coding
- **Consistent APIs** - Same patterns across all models  
- **Focus on business logic** - Not infrastructure
- **Rapid prototyping** - MVP ready in minutes
- **Scalable architecture** - Add models, get APIs instantly

### 📈 **Perfect For:**
- **Startups** - MVP development
- **Prototypes** - Quick API development
- **Microservices** - Consistent CRUD services
- **Admin panels** - Backend APIs
- **Learning** - FastAPI best practices

---

**🚀 Made with ❤️ for developers who value their time!**

**One file. Infinite possibilities. Zero repetitive code.**