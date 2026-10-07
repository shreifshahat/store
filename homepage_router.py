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
