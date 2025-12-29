import random
from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models

fake = Faker()
db = SessionLocal()

for _ in range(1000):
    product = models.Product(
        name=fake.catch_phrase(),
        manufacturer=fake.company(),
        unit="pcs",
        specifications={
            "weight": f"{random.randint(1, 50)}kg",
            "material": fake.word(),
            "warranty": f"{random.randint(1, 5)} years"
        }
    )
    db.add(product)

for _ in range(1000):
    customer = models.Customer(
        name=fake.name(),
        address=fake.address(),
        phone=fake.phone_number()
    )
    db.add(customer)

db.commit()

for _ in range(5000):
    purchase = models.Purchase(
        product_id=random.randint(1, 100),
        customer_id=random.randint(1, 100),
        quantity=random.randint(1, 10),
        price_per_unit=random.uniform(10.0, 1000.0)
    )
    db.add(purchase)

db.commit()
db.close()