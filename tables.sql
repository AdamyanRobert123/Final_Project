CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    manufacturer VARCHAR(255),
    unit VARCHAR(50),
    specifications JSONB
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(20)
);

CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    customer_id INTEGER REFERENCES customers(id),
    quantity INTEGER NOT NULL,
    price_per_unit NUMERIC(10, 2) NOT NULL,
    purchase_date DATE DEFAULT CURRENT_DATE
);