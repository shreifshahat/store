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
