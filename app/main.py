from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from .middleware import AuditMiddleware

from . import models, schemas, crud
from .database import engine, get_db

from fastapi import Request
from fastapi.responses import JSONResponse
import logging
# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI POC Microservice")

app.add_middleware(AuditMiddleware)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 1. Log the actual error for the developer (you) to see in the terminal
    logging.error(f"Global Error Catch: {str(exc)}")
    
    # 2. Return a clean, "massaged" response to the user
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred.",
            "detail": str(exc) if app.debug else "Contact support for more information."
        },
    )
# --- USER ENDPOINTS ---

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# --- PRODUCT ENDPOINTS ---

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

# --- ORDER ENDPOINTS (Complex Join & Transformation) ---

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)

@app.get("/users/{user_id}/orders-summary")
def get_user_orders_summary(user_id: int, db: Session = Depends(get_db)):
    orders = crud.get_user_orders_with_details(db, user_id=user_id)
    
    # DATA MASSAGE: Transforming raw DB results into a summary
    summary = []
    for order in orders:
        total_qty = sum(item.quantity for item in order.items)
        summary.append({
            "order_id": order.id,
            "date": order.order_date,
            "total_items": total_qty,
            "items": [
                {"product": item.product.name, "qty": item.quantity} 
                for item in order.items
            ]
        })
    return {"user_id": user_id, "order_history": summary}

# --- ROOT ---
@app.get("/")
def read_root():
    return {"message": "API is live. Go to /docs for Swagger UI"}