"""جداول قاعدة البيانات — كل أرقام الطلبات والمبيعات تُقرأ من هنا."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, default="", nullable=False)
    price = Column(Float, nullable=False)
    old_price = Column(Float, nullable=True)
    image_url = Column(String(500), default="", nullable=False)
    category = Column(String(80), nullable=False, index=True, default="mobiles")
    brand = Column(String(80), nullable=False, default="", index=True)
    stock = Column(Integer, nullable=False, default=50)
    specs = Column(Text, default="{}", nullable=False)  # JSON string
    rating = Column(Float, nullable=False, default=4.5)
    reviews_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    is_featured = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(40), unique=True, index=True, nullable=False)
    customer_name = Column(String(120), nullable=False)
    phone = Column(String(40), nullable=False, index=True)
    address = Column(String(400), nullable=False)
    email = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(30), nullable=False, default="pending", index=True)
    subtotal = Column(Float, nullable=False, default=0.0)
    shipping = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)
    payment_method = Column(String(40), nullable=False, default="cod")
    notes = Column(String(400), nullable=False, default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_name = Column(String(200), nullable=False, default="")
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False, default=0.0)

    order = relationship("Order", back_populates="items")


class PageVisit(Base):
    __tablename__ = "page_visits"

    id = Column(Integer, primary_key=True, index=True)
    page = Column(String(120), nullable=False, index=True, default="home")
    session_id = Column(String(80), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class CartEvent(Base):
    __tablename__ = "cart_events"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True, index=True)
    event_type = Column(String(20), nullable=False, default="add", index=True)
    session_id = Column(String(80), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class HomepageSection(Base):
    __tablename__ = "homepage_sections"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(80), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False, default="")
    subtitle = Column(String(400), nullable=False, default="")
    image_url = Column(String(500), nullable=False, default="")
    link = Column(String(300), nullable=False, default="")
    content = Column(Text, nullable=False, default="{}")
    is_visible = Column(Boolean, nullable=False, default=True)
    sort_order = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
