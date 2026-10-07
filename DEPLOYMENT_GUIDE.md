# 🚀 دليل رفع المشروع على GitHub ونشره أونلاين

هذا الدليل يوضح لك بالخطوات السريعة كيفية رفع هذا المشروع على حسابك في GitHub ثم نشره ليعمل أونلاين للجميع.

---

## الخطوة 1: الرفع على GitHub عبر الـ Terminal

المشروع جاهز ومُهيأ بالكامل (Git Initialized). كل ما عليك فعله:

1. افتح موقع **[GitHub.com](https://github.com/)** وأنشئ مستودعاً جديداً (**New Repository**).
2. سمِّ المستودع بأي اسم تريده (مثلاً: `electronics-store`).
3. **لا تضع علامة صح** على "Add a README" أو ".gitignore" (لأننا جهزناهم بالفعل).
4. بعد إنشاء المستودع، انسخ الرابط الخاص به، ثم افتح الـ Terminal ونفذ:

```bash
cd /Users/shrief/electronics-store

# 1. ربط المشروع بمستودع GitHub الخاص بك (استبدل YOUR_USERNAME باسم حسابك)
git remote add origin https://github.com/YOUR_USERNAME/electronics-store.git

# 2. رفع الملفات إلى فرع main
git branch -M main
git push -u origin main
```

> **ملاحظة:** إذا كنت تفضل استخدام واجهة رسومية، يمكنك سحب المجلد مباشرة إلى تطبيق **GitHub Desktop** أو رفع ملف `electronics-store-github.zip` الموجود على سطح المكتب (Desktop).

---

## الخطوة 2: نشر الباك إند (Backend) مجاناً (Render / Railway)

1. سجل دخول في **[Render.com](https://render.com/)**.
2. اختر **New +** ثم **Web Service**.
3. اربط مستودع GitHub الخاص بك (`electronics-store`).
4. اضبط الإعدادات التالية:
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r ../requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. في قسم **Environment Variables**، يمكنك إضافة:
   - `JWT_SECRET`: مفتاح عشوائي لحماية التوكن.
6. اضغط **Deploy**. سيعطيك Render رابطاً عاماً للباك إند (مثل: `https://electronics-store-api.onrender.com`).

---

## الخطوة 3: نشر الفرونت إند (Frontend)

### الخيار أ: عبر GitHub Pages (الأسهل والأسرع)
1. في صفحة المستودع على GitHub، اذهب إلى **Settings** > **Pages**.
2. تحت **Branch**، اختر `main` واجعل المجلد `/frontend` (أو `/root` إذا نقلت ملفات الفرونت إند للجذر).
3. اضغط **Save**، وخلال دقيقة سيعطيك GitHub رابط موقعك مجاناً.

### الخيار ب: عبر Vercel أو Netlify
1. ادخل على **Vercel.com** واضغط **Add New Project**.
2. اختر مستودع GitHub وحدد الـ **Root Directory** ليكون `frontend`.
3. اضغط **Deploy** وسيعمل الموقع فوراً مع شهادة SSL مجانية.

> ⚠️ **مهم جداً:** بعد نشر الباك إند والحصول على الرابط أونلاين، قم بتعديل `API_BASE` في `frontend/config.js` أو وضع رابط الباك إند في متغيرات البيئة ليتصل الفرونت إند بالباك إند الحي.
