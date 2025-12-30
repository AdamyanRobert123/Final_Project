import psycopg2

def apply():
    try:
        conn = psycopg2.connect(
            dbname="sales_project",
            user="rob1234",
            password="admin123",
            host="127.0.0.1",
            port="5432"
        )
        cur = conn.cursor()
        
        cur.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS discount INTEGER DEFAULT 0;")
        cur.execute("CREATE INDEX IF NOT EXISTS ix_products_name ON products (name);")
        
        conn.commit()
        print("Success")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    apply()