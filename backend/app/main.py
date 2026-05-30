from fastapi import FastAPI

from app.database import engine 
from app.models import Base
from app.routers import products, customers, orders

app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return {"message": "Inventory API Running"}