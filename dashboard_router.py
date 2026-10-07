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
