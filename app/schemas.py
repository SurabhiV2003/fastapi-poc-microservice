from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    name: str
    email: str
    role: str

class UserCreate(UserBase):
    pass  # Used when creating a user (no ID yet)

class User(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# --- PRODUCT SCHEMAS ---
class ProductBase(BaseModel):
    name: str
    price: float
    category: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# --- ORDER ITEM SCHEMAS ---
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItem(OrderItemBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# --- ORDER SCHEMAS ---
class OrderBase(BaseModel):
    user_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemBase] # To create an order with multiple items at once

class Order(OrderBase):
    id: int
    order_date: datetime
    items: List[OrderItem] = [] # Nested relationship

    model_config = ConfigDict(from_attributes=True)

# --- AUDIT LOG SCHEMA ---
class AuditLog(BaseModel):
    id: int
    timestamp: datetime
    endpoint: str
    request_payload: str
    response_payload: str
    status_code: int

    model_config = ConfigDict(from_attributes=True)