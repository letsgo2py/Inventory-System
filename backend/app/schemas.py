from pydantic import BaseModel, EmailStr, Field


# Product

class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    quantity: int = Field(..., ge=0)

class ProductUpdate(BaseModel):
    name: str
    sku: str
    price: float
    quantity: int = Field(..., ge=0)
    
class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True


# Customer

class CustomerCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str


class CustomerResponse(CustomerCreate):
    id: int

    class Config:
        from_attributes = True


# Order

class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float

    class Config:
        from_attributes = True