from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import Optional, List
import json

DATABASE_URL = "postgresql://rob1234:admin123@localhost:5432/sales_project"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

def run_migrations():
    db = SessionLocal()
    try:
        db.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        db.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS details_text TEXT;"))
        db.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS discount INTEGER DEFAULT 0;"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_products_name ON products (name);"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_products_details_gin ON products USING GIN (details_text gin_trgm_ops);"))
        db.commit()
    except:
        pass
    finally:
        db.close()

run_migrations()

class ProductSchema(BaseModel):
    name: str
    price: float
    category_id: int
    details: Optional[dict] = None

@app.post("/products/")
def create_product(item: ProductSchema):
    db = SessionLocal()
    query = text("""
        INSERT INTO products (name, price, category_id, details, details_text) 
        VALUES (:name, :price, :category_id, :details, :details_text) RETURNING id
    """)
    d_str = json.dumps(item.details) if item.details else "{}"
    result = db.execute(query, {
        "name": item.name, 
        "price": item.price, 
        "category_id": item.category_id, 
        "details": d_str,
        "details_text": d_str
    })
    db.commit()
    product_id = result.fetchone()[0]
    db.close()
    return {"id": product_id}

@app.get("/products/search-details/")
def search_details(regex: str):
    db = SessionLocal()
    sql = text("SELECT * FROM products WHERE details_text ~ :regex")
    result = db.execute(sql, {"regex": regex}).fetchall()
    db.close()
    return [dict(row._mapping) for row in result]

@app.get("/products/")
def read_products(limit: int = 10, offset: int = 0):
    db = SessionLocal()
    query = text("""
        SELECT id, name, price, category_id, details 
        FROM products 
        LIMIT :limit OFFSET :offset
    """)
    result = db.execute(query, {"limit": limit, "offset": offset}).fetchall()
    total = db.execute(text("SELECT COUNT(*) FROM products")).scalar()
    db.close()
    return {
        "total_count": total,
        "limit": limit,
        "offset": offset,
        "data": [dict(row._mapping) for row in result]
    }

@app.put("/products/{product_id}")
def update_product(product_id: int, item: ProductSchema):
    db = SessionLocal()
    query = text("""
        UPDATE products 
        SET name = :name, price = :price, category_id = :category_id, details = :details, details_text = :details_text
        WHERE id = :id
    """)
    d_str = json.dumps(item.details) if item.details else "{}"
    db.execute(query, {
        "id": product_id,
        "name": item.name,
        "price": item.price,
        "category_id": item.category_id,
        "details": d_str,
        "details_text": d_str
    })
    db.commit()
    db.close()
    return {"status": "updated"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()
    db.execute(text("DELETE FROM products WHERE id = :id"), {"id": product_id})
    db.commit()
    db.close()
    return {"status": "deleted"}

@app.get("/filter-products/")
def filter_products(min_price: float, cat_id: int):
    db = SessionLocal()
    sql = text("SELECT * FROM products WHERE price >= :min_price AND category_id = :cat_id")
    result = db.execute(sql, {"min_price": min_price, "cat_id": cat_id}).fetchall()
    db.close()
    return [dict(row._mapping) for row in result]

@app.get("/products-with-categories/")
def get_joined_data():
    db = SessionLocal()
    sql = text("""
        SELECT p.name AS product, c.name AS category 
        FROM products p 
        JOIN categories c ON p.category_id = c.id
    """)
    result = db.execute(sql).fetchall()
    db.close()
    return [dict(row._mapping) for row in result]

@app.get("/stats/")
def get_stats():
    db = SessionLocal()
    sql = text("SELECT category_id, COUNT(*) as total FROM products GROUP BY category_id")
    result = db.execute(sql).fetchall()
    db.close()
    return [dict(row._mapping) for row in result]

@app.get("/sorted-products/")
def get_sorted(order: str = "asc"):
    db = SessionLocal()
    sql_text = "SELECT * FROM products ORDER BY price DESC" if order == "desc" else "SELECT * FROM products ORDER BY price ASC"
    result = db.execute(text(sql_text)).fetchall()
    db.close()
    return [dict(row._mapping) for row in result]
















    