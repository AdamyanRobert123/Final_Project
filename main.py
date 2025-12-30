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

def run_migrations():
    db = SessionLocal()
    try:
        db.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS discount INTEGER DEFAULT 0;"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_products_name ON products (name);"))
        db.commit()
    except Exception as e:
        print(f"Migration error: {e}")
    finally:
        db.close()

run_migrations()

@app.get("/products-with-categories/")
def get_products_with_categories():
    db = SessionLocal()
    query = text("""
        SELECT p.id, p.name, p.price, c.name as category_name 
        FROM products p 
        JOIN categories c ON p.category_id = c.id
    """)
    result = db.execute(query).fetchall()
    return [dict(row._mapping) for row in result]

@app.get("/category-stats/")
def get_category_stats():
    db = SessionLocal()
    query = text("""
        SELECT c.name, COUNT(p.id) as product_count 
        FROM categories c 
        LEFT JOIN products p ON c.id = p.category_id 
        GROUP BY c.name
    """)
    result = db.execute(query).fetchall()
    return [dict(row._mapping) for row in result]