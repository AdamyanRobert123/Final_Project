from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import Optional, List

DATABASE_URL = "postgresql://rob1234:admin123@localhost:5432/sales_project"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

class ProductSchema(BaseModel):
    name: str
    price: float
    category_id: int
    details: Optional[dict] = None

@app.post("/products/")
def create_product(item: ProductSchema):
    db = SessionLocal()
    query = text("""
        INSERT INTO products (name, price, category_id, details) 
        VALUES (:name, :price, :category_id, :details) RETURNING id
    """)
    import json
    result = db.execute(query, {
        "name": item.name, 
        "price": item.price, 
        "category_id": item.category_id, 
        "details": json.dumps(item.details) if item.details else None
    })
    db.commit()
    return {"id": result.fetchone()[0]}

@app.get("/products/")
def read_products():
    db = SessionLocal()
    query = text("SELECT id, name, price, category_id, details FROM products")
    result = db.execute(query).fetchall()
    return [dict(row._mapping) for row in result]

@app.put("/products/{product_id}")
def update_product(product_id: int, item: ProductSchema):
    db = SessionLocal()
    query = text("""
        UPDATE products 
        SET name = :name, price = :price, category_id = :category_id, details = :details
        WHERE id = :id
    """)
    import json
    db.execute(query, {
        "id": product_id,
        "name": item.name,
        "price": item.price,
        "category_id": item.category_id,
        "details": json.dumps(item.details) if item.details else None
    })
    db.commit()
    return {"status": "updated"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()
    db.execute(text("DELETE FROM products WHERE id = :id"), {"id": product_id})
    db.commit()
    return {"status": "deleted"}