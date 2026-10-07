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

