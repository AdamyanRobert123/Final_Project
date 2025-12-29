from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    manufacturer: str
    unit: str
    specifications: dict

products_db = []

@app.post("/products/", response_model=Product)
def create_product(product: Product):
    products_db.append(product)
    return product

@app.get("/products/", response_model=List[Product])
def read_all_products():
    return products_db

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int):
    for product in products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: Product):
    for index, product in enumerate(products_db):
        if product.id == product_id:
            products_db[index] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products_db):
        if product.id == product_id:
            del products_db[index]
            return {"status": "success", "message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")