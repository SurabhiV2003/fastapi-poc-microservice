from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String)

    # Relationship: A user can have many orders
    orders = relationship("Order", back_populates="owner")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    category = Column(String)

    # Relationship: A product can appear in many order items
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_date = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    endpoint = Column(String)
    request_payload = Column(Text)   # Storing JSON as text
    response_payload = Column(Text)  # Storing JSON as text
    status_code = Column(Integer)