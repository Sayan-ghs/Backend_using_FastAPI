from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import Session, engine
import database_models
from sqlalchemy.orm import Session


app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:3000'],
        allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind = engine)

def init_db():
        db = Session()

        count = db.query(database_models.Product).count

        if count == 0:
                for product in products:
                        db.add(database_models.Product(**product.model_dump()))

                db.commit()

init_db()

def get_db():
        db = Session()

        try:
                yield db
        finally:
                db.close()

# Rest - Representation State Transform
# API - Application Programming Interface

@app.get("/")
def greet():
        return "welcome back python"

products = [
        Product(id = 1, name= "Laptop", description="A Macbook", price="299999", quantity=50),
        Product(id=2, name="Phone", description="A smartphone", Price= 10000, quantity=100),
        Product(id=3, name="Pen", description="pain", price=1000, quantity=1000)
]

#pydantic - Data Validation
@app.get("/products")
def get_all_product(db: Session = Depends(get_db) ):
        db_products = db.query(database_models.Product).all()
        # db = Session()
        # db.query()
        return db_products

#CRUD 
#localhost:8000/docs --> swagger --> To check the end point

@app.get("/product/{id}") #dynamic path
def get_product_by_id(id:int, db: Session = Depends(get_db) ):
        # for product in products:
        db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
        if db_product:
                return db_product

        return "prouct not found"

#Create
@app.post("/product")
def add_product(product:Product,db: Session = Depends(get_db)):
        # products.append(product)
        db.add(database_models.Product(**product.model_dump()))
        db.commit()
        return product

#update 
@app.put("/product")
def update_product(id: int, product:Product, db:Session = Depends(get_db)):
        db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
        if db_product:
                db_product.name = product.name
                db_product.description = product.description
                db_product.quantity = product.quantity
                db.commit()
        return "No product found"

#Delete
@app.delete("/product")
def delete_product(id:int, db:Session = Depends(get_db)):
        db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
        if db_product:
                db.delete(db_product)
                db.commit()
        
        return "No product found"


