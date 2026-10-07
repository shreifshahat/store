"""Pydantic schemas للتحقق من البيانات."""
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Products ----------
class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str = ""
    price: float = Field(gt=0)
    old_price: Optional[float] = None
    image_url: str = ""
    category: str = "mobiles"
    brand: str = ""
    stock: int = Field(default=50, ge=0)
    specs: Dict[str, Any] = {}
    rating: float = Field(default=4.5, ge=0, le=5)
    reviews_count: int = Field(default=0, ge=0)
    is_active: bool = True
    is_featured: bool = False


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    old_price: Optional[float] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    stock: Optional[int] = Field(default=None, ge=0)
    specs: Optional[Dict[str, Any]] = None
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    reviews_count: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    old_price: Optional[float]
    image_url: str
    category: str
    brand: str
    stock: int
    specs: Dict[str, Any] = {}
    rating: float
    reviews_count: int
    is_active: bool
    is_featured: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Orders ----------
class OrderItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, le=20)


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=6, max_length=40)
    address: str = Field(min_length=4, max_length=400)
    email: Optional[EmailStr] = None
    items: List[OrderItemIn] = Field(min_length=1)
    payment_method: str = "cod"
    notes: str = ""


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    order_number: str
    customer_name: str
    phone: str
    address: str
    email: Optional[str]
    status: str
    subtotal: float
    shipping: float
    total: float
    payment_method: str
    notes: str
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str


# ---------- Tracking ----------
class VisitIn(BaseModel):
    page: str = "home"
    session_id: Optional[str] = None


class CartEventIn(BaseModel):
    product_id: Optional[int] = None
    event_type: str = "add"
    session_id: Optional[str] = None


# ---------- Homepage ----------
class HomepageSectionCreate(BaseModel):
    key: str = Field(min_length=2, max_length=80)
    title: str = ""
    subtitle: str = ""
    image_url: str = ""
    link: str = ""
    content: Dict[str, Any] = {}
    is_visible: bool = True
    sort_order: int = 0


class HomepageSectionUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    image_url: Optional[str] = None
    link: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    is_visible: Optional[bool] = None
    sort_order: Optional[int] = None


class HomepageSectionOut(BaseModel):
    id: int
    key: str
    title: str
    subtitle: str
    image_url: str
    link: str
    content: Dict[str, Any] = {}
    is_visible: bool
    sort_order: int

    class Config:
        from_attributes = True
