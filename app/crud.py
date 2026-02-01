from sqlalchemy.orm import Session
from . import models, schemas

# --- USER CRUD ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- PRODUCT CRUD ---
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# --- ORDER CRUD (The Complex Part) ---
def create_order(db: Session, order: schemas.OrderCreate):
    # 1. Create the Order base
    db_order = models.Order(user_id=order.user_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # 2. Create the Order Items
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_user_orders_with_details(db: Session, user_id: int):
    """
    Complex Query: Joins Orders, OrderItems, and Products 
    to give a full summary for a specific user.
    """
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()

# --- AUDIT LOG CRUD ---
def create_audit_log(db: Session, endpoint: str, request_payload: str, response_payload: str, status_code: int):
    db_log = models.AuditLog(
        endpoint=endpoint,
        request_payload=request_payload,
        response_payload=response_payload,
        status_code=status_code
    )
    db.add(db_log)
    db.commit()