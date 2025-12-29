CREATE USER sales_admin WITH PASSWORD 'admin123';

CREATE DATABASE sales_department OWNER sales_admin;

GRANT ALL PRIVILEGES ON DATABASE sales_department TO sales_admin;