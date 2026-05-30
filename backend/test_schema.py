from app.schemas import ProductCreate

product = ProductCreate(
    name="Laptop",
    sku="LP001",
    price=50000,
    quantity=10
)

print(product)