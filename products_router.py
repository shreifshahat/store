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
