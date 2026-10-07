# ⚡ تِك ستور — متجر إلكترونيات

متجر إلكترونيات كامل: باك إند **FastAPI + SQLite** وفورنت إند **HTML/CSS/JS** (بدون أي خطوة بناء).

## هيكل المجلدات

```
electronics-store/
├── requirements.txt
├── README.md
├── backend/
│   ├── main.py              # نقطة التشغيل
│   ├── database.py          # إعداد SQLite
│   ├── models.py            # الجداول (مستخدمين، منتجات، طلبات، زيارات، سلة، أقسام)
│   ├── schemas.py           # التحقق من البيانات
│   ├── auth.py              # JWT + bcrypt
│   ├── seed.py              # بيانات تجريبية + أدمن
│   └── routers/
│       ├── auth_router.py       # تسجيل الدخول / حساب جديد
│       ├── products_router.py   # بحث + فلاتر + CRUD
│       ├── orders_router.py     # شراء كضيف + إلغاء
│       ├── dashboard_router.py  # جزأين: تجربة العميل / تشغيل الاستور
│       └── homepage_router.py   # أقسام الرئيسية القابلة للتعديل
└── frontend/
    ├── index.html   # المتجر (بحث، فلاتر، سلة، شراء بدون حساب)
    ├── admin.html   # الداش بورد + إدارة المنتجات والطلبات والأقسام
    ├── login.html   # الدخول / إنشاء حساب
    ├── styles.css
    ├── app.js
    ├── admin.js
    └── config.js    # رابط الـ API
```

## التشغيل

### 1) الباك إند

```bash
cd electronics-store
pip install -r requirements.txt
cd backend
python seed.py        # أول مرة فقط: ينشئ أدمن + 12 منتج + أقسام
uvicorn main:app --reload --port 8000
```

- الـ API: http://localhost:8000
- التوثيق التفاعلي: http://localhost:8000/docs
- الأدمن التجريبي: `admin@store.com / admin123`

### 2) الفرونت إند

افتح ملف `frontend/index.html` في المتصفح مباشرة (أو عبر أي سيرفر ستاتيك):

```bash
cd frontend
python3 -m http.server 5500
# ثم افتح: http://localhost:5500/index.html
```

> لو الباك إند على عنوان غير `localhost:8000` عدّل `frontend/config.js`.

## الميزات

- تسجيل دخول + إنشاء حساب (JWT)
- داش بورد جزأين: **تجربة العميل** (الزيارات، الإضافة للسلة) و**تشغيل الاستور** (المبيعات، الإلغاءات) — كل الأرقام من قاعدة البيانات
- بحث + فلاتر حسب نوع المنتج والماركة والسعر + ترتيب
- شراء **بدون إجبار على إنشاء حساب** (ضيف)
- زر شراء واضح + صور واضحة + صفحات سريعة
- الصفحة الرئيسية أقسام قابلة للتعديل من الداش بورد (عنوان، صورة، وصف، إظهار/إخفاء)
- إضافة منتج + تعديل السعر والصور والمواصفات والمخزون من الداش بورد

## 🚀 النشر على GitHub والإنترنت

راجع ملف **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** لمعرفة الخطوات الكاملة لرفع المشروع على GitHub ونشره مجاناً على Render / Vercel / GitHub Pages.
