from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    customer = (
        db.query(models.Customer)
        .filter(models.Customer.id == order.customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    product = (
        db.query(models.Product)
        .filter(models.Product.id == order.product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product.quantity < order.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    total_amount = product.price * order.quantity

    product.quantity -= order.quantity

    new_order = models.Order(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_amount=total_amount
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/", response_model=list[schemas.OrderResponse])
def get_orders(
    db: Session = Depends(get_db)
):
    return db.query(models.Order).all()


@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()

    return {"message": "Order deleted successfully"}