======================================================================
FILE: electronics-store/requirements.txt
======================================================================

fastapi>=0.115.0
uvicorn[standard]>=0.30.0
sqlalchemy>=2.0.0
pydantic>=2.10.0
python-jose[cryptography]>=3.3.0
bcrypt>=4.0.0
python-multipart>=0.0.9
email-validator>=2.0.0
python-dotenv>=1.0.0
# psycopg2-binary>=2.9.0  # اختياري: فعّله فقط إذا أردت استخدام PostgreSQL / Supabase بدلاً من SQLite


======================================================================
FILE: electronics-store/backend/main.py
======================================================================

"""نقطة تشغيل الباك إند — FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import auth_router, dashboard_router, homepage_router, orders_router, products_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Electronics Store API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(orders_router.router)
app.include_router(dashboard_router.router)
app.include_router(homepage_router.router)


@app.get("/")
def root():
    return {"ok": True, "service": "Electronics Store API", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"ok": True}


======================================================================
FILE: electronics-store/backend/database.py
======================================================================

"""إعداد قاعدة البيانات — SQLite افتراضياً، أو Supabase Postgres عبر DATABASE_URL في backend/.env."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

try:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./store.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:  # Postgres (Supabase) — بدون check_same_thread
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


======================================================================
FILE: electronics-store/backend/models.py
======================================================================

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


======================================================================
FILE: electronics-store/backend/schemas.py
======================================================================

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


======================================================================
FILE: electronics-store/backend/auth.py
======================================================================

"""المصادقة JWT + تشفير كلمات المرور (bcrypt مباشرة بدون passlib)."""
import os
from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import models
from database import get_db

SECRET_KEY = os.getenv("JWT_SECRET", "electronics-store-super-secret-change-me-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

pwd_context = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login-form")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="غير مصرح — سجل الدخول أولاً",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise exc
    except JWTError:
        raise exc
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise exc
    return user


def get_current_admin(user: models.User = Depends(get_current_user)) -> models.User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="هذه الصفحة للإدارة فقط")
    return user


def get_optional_user(
    db: Session = Depends(get_db),
    token: str | None = Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/login-form", auto_error=False)),
) -> models.User | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            return None
        return db.query(models.User).filter(models.User.email == email).first()
    except JWTError:
        return None


======================================================================
FILE: electronics-store/backend/seed.py
======================================================================

"""بيانات تجريبية: أدمن + منتجات إلكترونيات + أقسام رئيسية."""
import json

import models
from auth import hash_password
from database import Base, SessionLocal, engine

PRODUCTS = [
    {
        "name": "آيفون 15 برو ماكس 256GB",
        "description": "شاشة Super Retina XDR مقاس 6.7 بوصة، شريحة A17 Pro، كاميرا 48MP، هيكل تيتانيوم.",
        "price": 61999.0,
        "old_price": 66999.0,
        "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&q=80",
        "category": "mobiles",
        "brand": "Apple",
        "stock": 25,
        "specs": {"الشاشة": "6.7 بوصة OLED", "المعالج": "A17 Pro", "التخزين": "256GB", "الكاميرا": "48MP", "البطارية": "4422mAh"},
        "rating": 4.9,
        "reviews_count": 412,
        "is_featured": True,
    },
    {
        "name": "سامسونج جالاكسي S24 ألترا",
        "description": "قلم S Pen مدمج، كاميرا 200MP مع ذكاء اصطناعي، شاشة 6.8 بوصة QHD+.",
        "price": 54999.0,
        "old_price": 58999.0,
        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&q=80",
        "category": "mobiles",
        "brand": "Samsung",
        "stock": 30,
        "specs": {"الشاشة": "6.8 بوصة Dynamic AMOLED", "المعالج": "Snapdragon 8 Gen 3", "الرام": "12GB", "التخزين": "512GB"},
        "rating": 4.8,
        "reviews_count": 356,
        "is_featured": True,
    },
    {
        "name": "لابتوب ماك بوك إير M3",
        "description": "شريحة Apple M3، شاشة Liquid Retina مقاس 13.6 بوصة، بطارية حتى 18 ساعة.",
        "price": 58999.0,
        "old_price": None,
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&q=80",
        "category": "laptops",
        "brand": "Apple",
        "stock": 15,
        "specs": {"المعالج": "Apple M3", "الرام": "8GB", "التخزين": "512GB SSD", "الشاشة": "13.6 بوصة"},
        "rating": 4.9,
        "reviews_count": 208,
        "is_featured": True,
    },
    {
        "name": "لابتوب لينوفو Legion 5 للألعاب",
        "description": "RTX 4060، رايزن 7، شاشة 165Hz — وحش الألعاب بسعر منافس.",
        "price": 47500.0,
        "old_price": 52000.0,
        "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&q=80",
        "category": "laptops",
        "brand": "Lenovo",
        "stock": 12,
        "specs": {"كرت الشاشة": "RTX 4060 8GB", "المعالج": "Ryzen 7 7745HX", "الرام": "16GB", "الشاشة": "15.6 بوصة 165Hz"},
        "rating": 4.7,
        "reviews_count": 154,
        "is_featured": False,
    },
    {
        "name": "سماعات سوني WH-1000XM5",
        "description": "أفضل عزل ضوضاء في العالم، بطارية 30 ساعة، صوت Hi-Res.",
        "price": 15999.0,
        "old_price": 17999.0,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80",
        "category": "audio",
        "brand": "Sony",
        "stock": 40,
        "specs": {"النوع": "Over-Ear", "البطارية": "30 ساعة", "البلوتوث": "5.2", "عزل الضوضاء": "نعم"},
        "rating": 4.8,
        "reviews_count": 521,
        "is_featured": True,
    },
    {
        "name": "إيربودز برو الجيل الثاني",
        "description": "عزل ضوضاء مضاعف، علبة شحن MagSafe، مقاومة للماء IP54.",
        "price": 10999.0,
        "old_price": None,
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80",
        "category": "audio",
        "brand": "Apple",
        "stock": 60,
        "specs": {"الشريحة": "H2", "البطارية": "6 ساعات + 24 بالعلبة", "مقاومة الماء": "IP54"},
        "rating": 4.7,
        "reviews_count": 689,
        "is_featured": False,
    },
    {
        "name": "شاشة سامسونج 55 بوصة QLED 4K",
        "description": "دقة 4K، معدل تحديث 120Hz، نظام Tizen ذكي مع مساعد صوتي.",
        "price": 27999.0,
        "old_price": 32999.0,
        "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800&q=80",
        "category": "tv",
        "brand": "Samsung",
        "stock": 10,
        "specs": {"الحجم": "55 بوصة", "الدقة": "4K QLED", "التحديث": "120Hz", "النظام": "Tizen"},
        "rating": 4.6,
        "reviews_count": 132,
        "is_featured": True,
    },
    {
        "name": "بلايستيشن 5 سليم + يد إضافية",
        "description": "نسخة السليم بمساحة 1TB مع يد تحكم DualSense إضافية.",
        "price": 24999.0,
        "old_price": None,
        "image_url": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&q=80",
        "category": "gaming",
        "brand": "Sony",
        "stock": 8,
        "specs": {"التخزين": "1TB SSD", "الدقة": "حتى 8K", "الأيدي": "2 × DualSense"},
        "rating": 4.9,
        "reviews_count": 298,
        "is_featured": True,
    },
    {
        "name": "ساعة أبل واتش سيريس 9",
        "description": "شريحة S9، شاشة أكثر سطوعاً، ميزة Double Tap، مقاومة للماء 50م.",
        "price": 18999.0,
        "old_price": 20999.0,
        "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&q=80",
        "category": "accessories",
        "brand": "Apple",
        "stock": 35,
        "specs": {"الحجم": "45mm", "الشريحة": "S9", "المقاومة": "WR50", "البطارية": "18 ساعة"},
        "rating": 4.7,
        "reviews_count": 187,
        "is_featured": False,
    },
    {
        "name": "شاحن أنكر 737 السريع 120W",
        "description": "شاحن GaN بثلاثة منافذ يشحن لابتوب وموبايلين معاً بأمان.",
        "price": 2499.0,
        "old_price": 2999.0,
        "image_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&q=80",
        "category": "accessories",
        "brand": "Anker",
        "stock": 100,
        "specs": {"القدرة": "120W GaN", "المنافذ": "2×USB-C + USB-A", "الحماية": "ActiveShield"},
        "rating": 4.6,
        "reviews_count": 843,
        "is_featured": False,
    },
    {
        "name": "كيبورد لوجيتك MX Keys S",
        "description": "كيبورد لاسلكي بإضاءة ذكية وراحة كتابة استثنائية للمحترفين.",
        "price": 5499.0,
        "old_price": None,
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80",
        "category": "accessories",
        "brand": "Logitech",
        "stock": 45,
        "specs": {"الاتصال": "بلوتوث + USB", "الإضاءة": "خلفية ذكية", "البطارية": "10 أيام"},
        "rating": 4.8,
        "reviews_count": 264,
        "is_featured": False,
    },
    {
        "name": "درون DJI Mini 4 Pro",
        "description": "كاميرا 4K/60، وزن أقل من 249g، تتبع ذكي وتفادي عوائق.",
        "price": 38500.0,
        "old_price": 42000.0,
        "image_url": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=800&q=80",
        "category": "gaming",
        "brand": "DJI",
        "stock": 6,
        "specs": {"الكاميرا": "4K/60fps", "الوزن": "249g", "الطيران": "34 دقيقة"},
        "rating": 4.8,
        "reviews_count": 96,
        "is_featured": False,
    },
]

SECTIONS = [
    {
        "key": "hero",
        "title": "أقوى عروض الإلكترونيات في مصر",
        "subtitle": "خصومات حتى 30% على الموبايلات واللابتوبات والسماعات — شحن سريع ودفع عند الاستلام",
        "image_url": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=1200&q=80",
        "link": "#products",
        "content": {"button_text": "تسوق الآن", "badge": "خصم حتى 30%"},
        "is_visible": True,
        "sort_order": 0,
    },
    {
        "key": "banner_shipping",
        "title": "شحن مجاني للطلبات فوق 5000 جنيه",
        "subtitle": "ودفع عند الاستلام + ضمان سنتين على كل الأجهزة",
        "image_url": "",
        "link": "",
        "content": {"icon": "truck"},
        "is_visible": True,
        "sort_order": 1,
    },
    {
        "key": "featured_title",
        "title": "منتجات مميزة",
        "subtitle": "مختارات فريقنا الأكثر مبيعاً وتقييماً",
        "image_url": "",
        "link": "",
        "content": {},
        "is_visible": True,
        "sort_order": 2,
    },
]


import random
from datetime import datetime, timedelta


def seed_demo_analytics(db):
    if db.query(models.Order).count() > 0:
        return

    products = db.query(models.Product).all()
    if not products:
        return

    now = datetime.utcnow()

    # 1. زيارات تجريبية لآخر 14 يوماً
    for day_offset in range(13, -1, -1):
        day_date = now - timedelta(days=day_offset)
        visits_count = random.randint(35, 120)
        for i in range(visits_count):
            visit_time = day_date.replace(hour=random.randint(9, 23), minute=random.randint(0, 59))
            sess = f"sess_{day_offset}_{i % 25}"
            db.add(models.PageVisit(page="home", session_id=sess, created_at=visit_time))

            # نسبة إضافة للسلة
            if random.random() < 0.28:
                prod = random.choice(products)
                db.add(models.CartEvent(product_id=prod.id, event_type="add", session_id=sess, created_at=visit_time))

    db.commit()

    # 2. طلبات تجريبية لآخر 14 يوماً بمختلف الحالات
    sample_customers = [
        ("محمد أحمد", "01012345678", "القاهرة، المعادي، شارع 9"),
        ("سارة محمود", "01123456789", "الجيزة، الدقي، شارع مصدق"),
        ("كريم عادل", "01234567890", "الإسكندرية، سموحة، شارع فوزي معاذ"),
        ("منى الشريف", "01098765432", "القاهرة، التجمع الخامس، النرجس"),
        ("عمر خالد", "01512344321", "المنصورة، شارع الجمهورية"),
        ("هدى إبراهيم", "01187654321", "طنطا، شارع النحاس"),
        ("يوسف طارق", "01299887766", "القاهرة، مدينة نصر، عباس العقاد"),
    ]

    order_statuses = ["delivered", "delivered", "shipped", "confirmed", "pending", "cancelled"]

    for idx, (c_name, c_phone, c_addr) in enumerate(sample_customers):
        created = now - timedelta(days=random.randint(0, 10), hours=random.randint(1, 12))
        st = order_statuses[idx % len(order_statuses)]
        ord_num = f"ORD-{created.strftime('%Y%m%d')}-{random.randint(100, 999)}"

        chosen_prods = random.sample(products, k=random.randint(1, 2))
        subtotal = 0.0
        items_data = []
        for p in chosen_prods:
            qty = random.randint(1, 2)
            subtotal += p.price * qty
            items_data.append((p, qty))

        shipping = 0.0 if subtotal >= 5000 else 60.0
        total = subtotal + shipping

        order = models.Order(
            order_number=ord_num,
            customer_name=c_name,
            phone=c_phone,
            address=c_addr,
            email=f"client{idx+1}@gmail.com",
            status=st,
            subtotal=round(subtotal, 2),
            shipping=round(shipping, 2),
            total=round(total, 2),
            payment_method="cod",
            created_at=created,
        )
        db.add(order)
        db.flush()

        for p, qty in items_data:
            db.add(
                models.OrderItem(
                    order_id=order.id,
                    product_id=p.id,
                    product_name=p.name,
                    quantity=qty,
                    price=p.price,
                )
            )

    db.commit()
    print("Demo analytics and orders seeded successfully!")


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(models.User).filter(models.User.email == "admin@store.com").first():
            db.add(
                models.User(
                    name="مدير المتجر",
                    email="admin@store.com",
                    hashed_password=hash_password("admin123"),
                    is_admin=True,
                )
            )
        if db.query(models.Product).count() == 0:
            for item in PRODUCTS:
                specs = item.pop("specs")
                db.add(models.Product(**item, specs=json.dumps(specs, ensure_ascii=False)))
        if db.query(models.HomepageSection).count() == 0:
            for s in SECTIONS:
                content = s.pop("content")
                db.add(models.HomepageSection(**s, content=json.dumps(content, ensure_ascii=False)))
        db.commit()
        seed_demo_analytics(db)
        print("Seed done: admin@store.com / admin123")
    finally:
        db.close()


if __name__ == "__main__":
    run()



======================================================================
FILE: electronics-store/backend/routers/__init__.py
======================================================================



======================================================================
FILE: electronics-store/backend/routers/auth_router.py
======================================================================

"""تسجيل الدخول / إنشاء حساب."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth
import models
import schemas
from database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.Token)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == data.email.lower().strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="هذا البريد مسجل بالفعل")
    user = models.User(
        name=data.name.strip(),
        email=data.email.lower().strip(),
        hashed_password=auth.hash_password(data.password),
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = auth.create_access_token({"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }


@router.post("/login", response_model=schemas.Token)
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email.lower().strip()).first()
    if not user or not auth.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="البريد أو كلمة المرور غير صحيحة")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.post("/login-form", response_model=schemas.Token)
def login_form(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form.username.lower().strip()).first()
    if not user or not auth.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="البريد أو كلمة المرور غير صحيحة")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.get("/me", response_model=schemas.UserOut)
def me(user: models.User = Depends(auth.get_current_user)):
    return user


======================================================================
FILE: electronics-store/backend/routers/products_router.py
======================================================================

"""المنتجات: بحث + فلاتر + CRUD للإدارة."""
import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

import auth
import models
import schemas
from database import get_db

router = APIRouter(prefix="/api/products", tags=["products"])

ALLOWED_SORT = {"newest", "price_asc", "price_desc", "rating", "popular"}


def to_out(p: models.Product) -> dict:
    try:
        specs = json.loads(p.specs) if p.specs else {}
    except Exception:
        specs = {}
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "old_price": p.old_price,
        "image_url": p.image_url,
        "category": p.category,
        "brand": p.brand,
        "stock": p.stock,
        "specs": specs,
        "rating": p.rating,
        "reviews_count": p.reviews_count,
        "is_active": p.is_active,
        "is_featured": p.is_featured,
        "created_at": p.created_at,
    }


@router.get("", response_model=list[schemas.ProductOut])
def list_products(
    search: str = Query(default=""),
    category: str = Query(default=""),
    brand: str = Query(default=""),
    min_price: float = Query(default=0),
    max_price: float = Query(default=0),
    sort: str = Query(default="newest"),
    featured: bool = Query(default=False),
    include_inactive: bool = Query(default=False),
    limit: int = Query(default=60, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(models.Product)
    if not include_inactive:
        q = q.filter(models.Product.is_active.is_(True))
    if search.strip():
        like = f"%{search.strip()}%"
        q = q.filter(
            or_(
                models.Product.name.ilike(like),
                models.Product.description.ilike(like),
                models.Product.brand.ilike(like),
            )
        )
    if category.strip():
        q = q.filter(models.Product.category == category.strip())
    if brand.strip():
        q = q.filter(models.Product.brand == brand.strip())
    if min_price > 0:
        q = q.filter(models.Product.price >= min_price)
    if max_price > 0:
        q = q.filter(models.Product.price <= max_price)
    if featured:
        q = q.filter(models.Product.is_featured.is_(True))

    sort = sort if sort in ALLOWED_SORT else "newest"
    if sort == "price_asc":
        q = q.order_by(models.Product.price.asc())
    elif sort == "price_desc":
        q = q.order_by(models.Product.price.desc())
    elif sort == "rating":
        q = q.order_by(models.Product.rating.desc())
    elif sort == "popular":
        q = q.order_by(models.Product.reviews_count.desc())
    else:
        q = q.order_by(models.Product.id.desc())

    products = q.limit(limit).all()
    return [to_out(p) for p in products]


@router.get("/categories")
def categories(db: Session = Depends(get_db)):
    rows = db.query(models.Product.category).filter(models.Product.is_active.is_(True)).distinct().all()
    cats = sorted([r[0] for r in rows if r[0]])
    brands = sorted(
        [r[0] for r in db.query(models.Product.brand).filter(models.Product.is_active.is_(True)).distinct().all() if r[0]]
    )
    counts = {}
    for c in cats:
        counts[c] = db.query(models.Product).filter(models.Product.category == c, models.Product.is_active.is_(True)).count()
    return {"categories": cats, "brands": brands, "counts": counts}


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="المنتج غير موجود")
    return to_out(p)


@router.post("", response_model=schemas.ProductOut)
def create_product(
    data: schemas.ProductCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_current_admin),
):
    p = models.Product(
        name=data.name.strip(),
        description=data.description,
        price=data.price,
        old_price=data.old_price,
        image_url=data.image_url,
        category=data.category.strip() or "mobiles",
        brand=data.brand.strip(),
        stock=data.stock,
        specs=json.dumps(data.specs or {}, ensure_ascii=False),
        rating=data.rating,
        reviews_count=data.reviews_count,
        is_active=data.is_active,
        is_featured=data.is_featured,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return to_out(p)


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    data: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_current_admin),
):
    p = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="المنتج غير موجود")
    payload = data.model_dump(exclude_unset=True)
    for field, value in payload.items():
        if field == "specs" and value is not None:
            setattr(p, "specs", json.dumps(value, ensure_ascii=False))
        elif value is not None:
            setattr(p, field, value.strip() if isinstance(value, str) else value)
    db.commit()
    db.refresh(p)
    return to_out(p)


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_current_admin),
):
    p = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="المنتج غير موجود")
    p.is_active = False
    db.commit()
    return {"ok": True, "message": "تم إخفاء المنتج من المتجر"}


======================================================================
FILE: electronics-store/backend/routers/orders_router.py
======================================================================

"""الطلبات: شراء بدون حساب (ضيف) + إلغاء + إدارة."""
import random
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import auth
import models
import schemas
from database import get_db

router = APIRouter(prefix="/api/orders", tags=["orders"])

VALID_STATUSES = {"pending", "confirmed", "shipped", "delivered", "cancelled"}
FREE_SHIPPING_LIMIT = 5000.0
SHIPPING_FEE = 60.0


def new_order_number() -> str:
    stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    rand = random.randint(100, 999)
    return f"ORD-{stamp}-{rand}"


@router.post("", response_model=schemas.OrderOut)
def create_order(
    data: schemas.OrderCreate,
    db: Session = Depends(get_db),
    user: models.User | None = Depends(auth.get_optional_user),
):
    subtotal = 0.0
    items_rows: list[tuple[models.Product, int]] = []
    for item in data.items:
        p = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not p or not p.is_active:
            raise HTTPException(status_code=404, detail=f"المنتج رقم {item.product_id} غير متاح")
        if p.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"الكمية غير متوفرة للمنتج: {p.name}")
        subtotal += p.price * item.quantity
        items_rows.append((p, item.quantity))

    shipping = 0.0 if subtotal >= FREE_SHIPPING_LIMIT else SHIPPING_FEE
    total = subtotal + shipping

    order = models.Order(
        order_number=new_order_number(),
        customer_name=data.customer_name.strip(),
        phone=data.phone.strip(),
        address=data.address.strip(),
        email=(data.email.lower().strip() if data.email else None),
        user_id=(user.id if user else None),
        status="pending",
        subtotal=round(subtotal, 2),
        shipping=round(shipping, 2),
        total=round(total, 2),
        payment_method=data.payment_method or "cod",
        notes=data.notes or "",
    )
    db.add(order)
    db.flush()

    for p, qty in items_rows:
        db.add(
            models.OrderItem(
                order_id=order.id,
                product_id=p.id,
                product_name=p.name,
                quantity=qty,
                price=p.price,
            )
        )
        p.stock -= qty

    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=list[schemas.OrderOut])
def list_orders(
    phone: str = Query(default=""),
    mine: bool = Query(default=False),
    db: Session = Depends(get_db),
    user: models.User | None = Depends(auth.get_optional_user),
):
    q = db.query(models.Order).order_by(models.Order.id.desc())
    # لو أدمن بدون فلاتر: يرجع كل الطلبات
    is_admin = bool(user and user.is_admin)
    if mine and user:
        q = q.filter(models.Order.user_id == user.id)
    elif phone.strip():
        q = q.filter(models.Order.phone == phone.strip())
    elif not is_admin:
        # الزائر بدون هاتف يرى آخر 20 طلب عامة؟ لا — نرجع فارغ حماية للخصوصية
        return []
    return q.limit(200).all()


@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    return order


@router.patch("/{order_id}/cancel", response_model=schemas.OrderOut)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    if order.status in ("shipped", "delivered"):
        raise HTTPException(status_code=400, detail="لا يمكن إلغاء طلب تم شحنه")
    if order.status == "cancelled":
        return order
    order.status = "cancelled"
    # إرجاع المخزون
    for item in order.items:
        p = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if p:
            p.stock += item.quantity
    db.commit()
    db.refresh(order)
    return order


@router.patch("/{order_id}/status", response_model=schemas.OrderOut)
def change_status(
    order_id: int,
    data: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_current_admin),
):
    if data.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="حالة غير صالحة")
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    order.status = data.status
    db.commit()
    db.refresh(order)
    return order


======================================================================
FILE: electronics-store/backend/routers/dashboard_router.py
======================================================================

"""الداش بورد: جزأين — تجربة العميل / تشغيل الاستور — كل الأرقام من قاعدة البيانات."""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

import auth
import models
import schemas
from database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def start_of_today() -> datetime:
    now = datetime.utcnow()
    return datetime(now.year, now.month, now.day)


@router.post("/track/visit")
def track_visit(data: schemas.VisitIn, db: Session = Depends(get_db)):
    db.add(models.PageVisit(page=data.page or "home", session_id=data.session_id))
    db.commit()
    return {"ok": True}


@router.post("/track/cart")
def track_cart(data: schemas.CartEventIn, db: Session = Depends(get_db)):
    event = data.event_type if data.event_type in ("add", "remove") else "add"
    db.add(models.CartEvent(product_id=data.product_id, event_type=event, session_id=data.session_id))
    db.commit()
    return {"ok": True}


@router.get("/customer-experience")
def customer_experience(
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_current_admin),
):
    today = start_of_today()

    total_visits = db.query(func.count(models.PageVisit.id)).scalar() or 0
    visits_today = (
        db.query(func.count(models.PageVisit.id)).filter(models.PageVisit.created_at >= today).scalar() or 0
    )
    visits_by_page = (
        db.query(models.PageVisit.page, func.count(models.PageVisit.id))
        .group_by(models.PageVisit.page)
        .order_by(func.count(models.PageVisit.id).desc())
        .all()
    )

    cart_adds_total = (
        db.query(func.count(models.CartEvent.id)).filter(models.CartEvent.event_type == "add").scalar() or 0
    )
    cart_adds_today = (
        db.query(func.count(models.CartEvent.id))
        .filter(models.CartEvent.event_type == "add", models.CartEvent.created_at >= today)
        .scalar()
        or 0
    )
    unique_sessions = db.query(func.count(func.distinct(models.PageVisit.session_id))).scalar() or 0

    top_added = (
        db.query(models.Product.id, models.Product.name, func.count(models.CartEvent.id).label("adds"))
        .join(models.CartEvent, models.CartEvent.product_id == models.Product.id)
        .filter(models.CartEvent.event_type == "add")
        .group_by(models.Product.id, models.Product.name)
        .order_by(func.count(models.CartEvent.id).desc())
        .limit(8)
        .all()
    )

    # آخر 14 يوم زيارات
    daily = []
    for i in range(13, -1, -1):
        day = datetime.utcnow().date() - timedelta(days=i)
        day_start = datetime(day.year, day.month, day.day)
        day_end = day_start + timedelta(days=1)
        count = (
            db.query(func.count(models.PageVisit.id))
            .filter(models.PageVisit.created_at >= day_start, models.PageVisit.created_at < day_end)
            .scalar()
            or 0
        )
        daily.append({"date": day.isoformat(), "visits": count})

    conversion = round((cart_adds_total / total_visits * 100) if total_visits else 0, 2)

    return {
        "total_visits": total_visits,
        "visits_today": visits_today,
        "unique_sessions": unique_sessions,
        "visits_by_page": [{"page": p, "count": c} for p, c in visits_by_page],
        "cart_adds_total": cart_adds_total,
        "cart_adds_today": cart_adds_today,
        "add_to_cart_rate_percent": conversion,
        "top_added_products": [{"id": pid, "name": name, "adds": adds} for pid, name, adds in top_added],
        "visits_last_14_days": daily,
    }


@router.get("/store")
def store_operations(
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_current_admin),
):
    today = start_of_today()

    orders = db.query(models.Order).all()
    valid = [o for o in orders if o.status != "cancelled"]
    cancelled = [o for o in orders if o.status == "cancelled"]

    total_sales = round(sum(o.total for o in valid), 2)
    sales_today = round(sum(o.total for o in valid if o.created_at and o.created_at >= today), 2)
    orders_today = sum(1 for o in orders if o.created_at and o.created_at >= today)

    by_status: dict[str, int] = {}
    for o in orders:
        by_status[o.status] = by_status.get(o.status, 0) + 1

    cancel_rate = round((len(cancelled) / len(orders) * 100) if orders else 0, 2)

    # إيراد آخر 14 يوم (من قاعدة البيانات)
    revenue_daily = []
    for i in range(13, -1, -1):
        day = datetime.utcnow().date() - timedelta(days=i)
        day_start = datetime(day.year, day.month, day.day)
        day_end = day_start + timedelta(days=1)
        rev = (
            db.query(func.coalesce(func.sum(models.Order.total), 0))
            .filter(
                models.Order.status != "cancelled",
                models.Order.created_at >= day_start,
                models.Order.created_at < day_end,
            )
            .scalar()
            or 0
        )
        revenue_daily.append({"date": day.isoformat(), "revenue": round(float(rev), 2)})

    # الأكثر مبيعاً من OrderItem
    top_selling = (
        db.query(
            models.OrderItem.product_id,
            models.OrderItem.product_name,
            func.sum(models.OrderItem.quantity).label("qty"),
            func.sum(models.OrderItem.quantity * models.OrderItem.price).label("revenue"),
        )
        .join(models.Order, models.Order.id == models.OrderItem.order_id)
        .filter(models.Order.status != "cancelled")
        .group_by(models.OrderItem.product_id, models.OrderItem.product_name)
        .order_by(func.sum(models.OrderItem.quantity).desc())
        .limit(8)
        .all()
    )

    low_stock = (
        db.query(models.Product)
        .filter(models.Product.is_active.is_(True), models.Product.stock <= 8)
        .order_by(models.Product.stock.asc())
        .limit(10)
        .all()
    )

    return {
        "orders_count": len(orders),
        "orders_today": orders_today,
        "total_sales": total_sales,
        "sales_today": sales_today,
        "cancelled_count": len(cancelled),
        "cancel_rate_percent": cancel_rate,
        "orders_by_status": by_status,
        "revenue_last_14_days": revenue_daily,
        "top_selling_products": [
            {"product_id": pid, "name": name, "quantity": int(qty or 0), "revenue": round(float(rev or 0), 2)}
            for pid, name, qty, rev in top_selling
        ],
        "low_stock": [{"id": p.id, "name": p.name, "stock": p.stock} for p in low_stock],
    }


======================================================================
FILE: electronics-store/backend/routers/homepage_router.py
======================================================================

"""أقسام الصفحة الرئيسية القابلة للتعديل (هيرو + عروض + بانرات)."""
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import auth
import models
import schemas
from database import get_db

router = APIRouter(prefix="/api/homepage", tags=["homepage"])


def to_out(s: models.HomepageSection) -> dict:
    try:
        content = json.loads(s.content) if s.content else {}
    except Exception:
        content = {}
    return {
        "id": s.id,
        "key": s.key,
        "title": s.title,
        "subtitle": s.subtitle,
        "image_url": s.image_url,
        "link": s.link,
        "content": content,
        "is_visible": s.is_visible,
        "sort_order": s.sort_order,
    }


@router.get("", response_model=list[schemas.HomepageSectionOut])
def list_sections(visible_only: bool = False, db: Session = Depends(get_db)):
    q = db.query(models.HomepageSection).order_by(models.HomepageSection.sort_order.asc())
    if visible_only:
        q = q.filter(models.HomepageSection.is_visible.is_(True))
    return [to_out(s) for s in q.all()]


@router.post("", response_model=schemas.HomepageSectionOut)
def create_section(
    data: schemas.HomepageSectionCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_current_admin),
):
    existing = db.query(models.HomepageSection).filter(models.HomepageSection.key == data.key).first()
    if existing:
        raise HTTPException(status_code=400, detail="هذا القسم موجود بالفعل")
    s = models.HomepageSection(
        key=data.key.strip(),
        title=data.title,
        subtitle=data.subtitle,
        image_url=data.image_url,
        link=data.link,
        content=json.dumps(data.content or {}, ensure_ascii=False),
        is_visible=data.is_visible,
        sort_order=data.sort_order,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return to_out(s)


@router.put("/{key}", response_model=schemas.HomepageSectionOut)
def update_section(
    key: str,
    data: schemas.HomepageSectionUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_current_admin),
):
    s = db.query(models.HomepageSection).filter(models.HomepageSection.key == key).first()
    if not s:
        raise HTTPException(status_code=404, detail="القسم غير موجود")
    payload = data.model_dump(exclude_unset=True)
    for field, value in payload.items():
        if field == "content" and value is not None:
            s.content = json.dumps(value, ensure_ascii=False)
        elif value is not None:
            setattr(s, field, value)
    db.commit()
    db.refresh(s)
    return to_out(s)


@router.delete("/{key}")
def delete_section(
    key: str,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_current_admin),
):
    s = db.query(models.HomepageSection).filter(models.HomepageSection.key == key).first()
    if not s:
        raise HTTPException(status_code=404, detail="القسم غير موجود")
    db.delete(s)
    db.commit()
    return {"ok": True}


======================================================================
FILE: electronics-store/backend/.env.example
======================================================================

# انسخ الملف ده إلى .env واملأ القيم الحقيقية (لا ترفع المفاتيح الحقيقية أبداً)
SUPABASE_URL=https://xyzcompany.supabase.co
SUPABASE_ANON_KEY=sb_publishable_PUT_YOUR_KEY_HERE
SUPABASE_SECRET_KEY=sb_secret_PUT_YOUR_KEY_HERE

DATABASE_URL=sqlite:///./store.db
# DATABASE_URL=postgresql://postgres:[DB_PASSWORD]@db.[REF].supabase.co:5432/postgres

JWT_SECRET=change-me-to-a-random-string


