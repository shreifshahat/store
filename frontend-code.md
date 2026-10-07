======================================================================
FILE: electronics-store/frontend/index.html
======================================================================

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>تِك ستور | متجر الإلكترونيات</title>
  <meta name="description" content="متجر إلكترونيات: موبايلات، لابتوبات، سماعات، شاشات وألعاب — شحن سريع ودفع عند الاستلام" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <header class="header">
    <div class="container header-inner">
      <a class="logo" href="index.html">تِك <span>ستور</span> ⚡</a>
      <div class="searchbar">
        <input id="searchInput" type="search" placeholder="دوّر على موبايل، لابتوب، سماعة..." />
        <button class="btn" onclick="applyFilters()">بحث</button>
      </div>
      <nav class="nav-links">
        <a class="btn btn-ghost" href="login.html" id="loginLink">دخول</a>
        <a class="btn btn-ghost" href="admin.html" id="adminLink" style="display:none">الداش بورد</a>
        <button class="icon-btn" onclick="toggleCart(true)" aria-label="السلة">🛒<span class="cart-count" id="cartCount">0</span></button>
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="hero" id="heroSection">
      <div class="hero-text">
        <span class="badge" id="heroBadge">خصم حتى 30%</span>
        <h1 id="heroTitle">أقوى عروض الإلكترونيات في مصر</h1>
        <p id="heroSubtitle">خصومات حتى 30% على الموبايلات واللابتوبات والسماعات — شحن سريع ودفع عند الاستلام</p>
        <a class="btn btn-big" href="#products" id="heroBtn">تسوق الآن 🛍️</a>
      </div>
      <div class="hero-img"><img id="heroImg" src="https://images.unsplash.com/photo-1498049794561-7780e7231661?w=1200&q=80" alt="عروض الإلكترونيات" loading="eager" /></div>
    </section>

    <div class="ship-strip" id="shipStrip">🚚 شحن مجاني للطلبات فوق 5000 جنيه — ودفع عند الاستلام + ضمان سنتين</div>

    <h2 class="section-title" id="featuredTitle">منتجات مميزة</h2>
    <p class="section-sub" id="featuredSub">مختارات فريقنا الأكثر مبيعاً وتقييماً</p>

    <div class="filters">
      <div class="filter-group">
        <label>الفئة (نوع المنتج)</label>
        <select id="fCategory" onchange="applyFilters()"><option value="">كل الفئات</option></select>
      </div>
      <div class="filter-group">
        <label>الماركة</label>
        <select id="fBrand" onchange="applyFilters()"><option value="">كل الماركات</option></select>
      </div>
      <div class="filter-group">
        <label>السعر من</label>
        <input id="fMin" type="number" min="0" placeholder="0" onchange="applyFilters()" />
      </div>
      <div class="filter-group">
        <label>السعر إلى</label>
        <input id="fMax" type="number" min="0" placeholder="100000" onchange="applyFilters()" />
      </div>
      <div class="filter-group">
        <label>ترتيب حسب</label>
        <select id="fSort" onchange="applyFilters()">
          <option value="newest">الأحدث</option>
          <option value="price_asc">السعر: من الأقل</option>
          <option value="price_desc">السعر: من الأعلى</option>
          <option value="rating">الأعلى تقييماً</option>
          <option value="popular">الأكثر شهرة</option>
        </select>
      </div>
    </div>

    <div id="products"><div class="grid" id="grid"></div></div>
    <div class="empty" id="emptyState" style="display:none">لا توجد منتجات مطابقة — جرّب بحثاً مختلفاً 🔍</div>

    <h2 class="section-title">تتبع طلبك 📦</h2>
    <p class="section-sub">دخل رقم موبايلك اللي طلبت بيه عشان تشوف طلباتك وتلغي لو حابب</p>
    <div class="filters">
      <div class="filter-group"><label>رقم الموبايل</label><input id="trackPhone" placeholder="01xxxxxxxxx" /></div>
      <div class="filter-group" style="max-width:180px"><label>&nbsp;</label><button class="btn" onclick="trackOrders()">عرض طلباتي</button></div>
    </div>
    <div id="myOrders"></div>
  </main>

  <footer class="footer">تِك ستور © 2026 — ضمان سنتين • دفع عند الاستلام • إرجاع مجاني خلال 14 يوم</footer>

  <!-- السلة -->
  <div class="drawer-overlay" id="cartOverlay" onclick="toggleCart(false)"></div>
  <aside class="drawer" id="cartDrawer">
    <h2 style="margin:0">سلة المشتريات 🛒</h2>
    <div id="cartItems" style="display:grid;gap:10px"></div>
    <div class="cart-total"><span>الإجمالي</span><span id="cartTotal">0 ج.م</span></div>
    <p style="font-size:13px;color:var(--muted);margin:0">الشحن مجاني فوق 5000 ج.م — غير كده 60 ج.م • بدون إجبار على إنشاء حساب ✅</p>
    <button class="btn btn-green btn-big btn-block" onclick="openCheckout()">اشترِ الآن — زر واضح ⚡</button>
    <button class="btn btn-ghost btn-block" onclick="toggleCart(false)">متابعة التسوق</button>
  </aside>

  <!-- إتمام الشراء كضيف -->
  <div class="modal-overlay" id="checkoutModal">
    <div class="modal">
      <h2>إتمام الطلب — بدون حساب ✅</h2>
      <div class="form-grid">
        <label>الاسم بالكامل<input id="cName" placeholder="مثال: أحمد محمد" /></label>
        <label>رقم الموبايل<input id="cPhone" placeholder="01xxxxxxxxx" /></label>
        <label>العنوان بالتفصيل<textarea id="cAddress" rows="2" placeholder="المحافظة - الشارع - علامة مميزة"></textarea></label>
        <label>البريد (اختياري)<input id="cEmail" type="email" placeholder="you@mail.com" /></label>
        <label>الدفع
          <select id="cPay"><option value="cod">الدفع عند الاستلام 💵</option><option value="card">بطاقة بنكية 💳</option></select>
        </label>
        <label>ملاحظات (اختياري)<input id="cNotes" placeholder="وقت التوصيل المفضل..." /></label>
      </div>
      <div class="cart-total" style="margin:14px 0"><span>الإجمالي + الشحن</span><span id="checkoutTotal"></span></div>
      <button class="btn btn-green btn-big btn-block" id="confirmBtn" onclick="confirmOrder()">تأكيد الطلب 🎉</button>
      <button class="btn btn-ghost btn-block" style="margin-top:8px" onclick="closeCheckout()">رجوع</button>
      <div id="orderSuccess"></div>
    </div>
  </div>

  <!-- تفاصيل منتج -->
  <div class="modal-overlay" id="detailModal">
    <div class="modal" style="width:min(760px,100%)">
      <div id="detailBody"></div>
      <button class="btn btn-ghost btn-block" style="margin-top:12px" onclick="document.getElementById('detailModal').classList.remove('open')">إغلاق</button>
    </div>
  </div>

  <div class="toast" id="toast"></div>

  <script src="config.js"></script>
  <script src="app.js"></script>
</body>
</html>


======================================================================
FILE: electronics-store/frontend/admin.html
======================================================================

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>الداش بورد | تِك ستور</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <header class="header">
    <div class="container header-inner">
      <a class="logo" href="index.html">تِك <span>ستور</span> ⚡</a>
      <b>لوحة التحكم</b>
      <nav class="nav-links" style="margin-right:auto">
        <a class="btn btn-ghost" href="index.html">المتجر</a>
        <button class="btn btn-ghost" onclick="logout()">خروج</button>
      </nav>
    </div>
  </header>

  <main class="container">
    <div class="tabs">
      <button class="tab active" onclick="showTab('dash',this)">📊 الداش بورد</button>
      <button class="tab" onclick="showTab('products',this)">📦 المنتجات</button>
      <button class="tab" onclick="showTab('orders',this)">🧾 الطلبات</button>
      <button class="tab" onclick="showTab('home',this)">🏠 أقسام الرئيسية</button>
    </div>

    <!-- الداش بورد -->
    <section id="tab-dash">
      <h2>🧪 جزء 1: تجربة العميل <small style="color:var(--muted);font-size:14px">(عدد الزيارات + الإضافة للسلة — من قاعدة البيانات)</small></h2>
      <div class="stats-grid" id="cxStats"></div>
      <div class="panel"><h3>الزيارات اليومية (آخر 14 يوم)</h3><div id="visitsChart"></div></div>
      <div class="panel"><h3>الأكثر إضافة للسلة</h3><div id="topAdded"></div></div>

      <h2>🏪 جزء 2: تشغيل الاستور <small style="color:var(--muted);font-size:14px">(المبيعات + الإلغاءات — من جدول الطلبات)</small></h2>
      <div class="stats-grid" id="storeStats"></div>
      <div class="panel"><h3>الإيراد اليومي (آخر 14 يوم)</h3><div id="revenueChart"></div></div>
      <div class="panel"><h3>الأكثر مبيعاً</h3><div id="topSelling"></div></div>
      <div class="panel"><h3>⚠️ مخزون منخفض</h3><div id="lowStock"></div></div>
    </section>

    <!-- المنتجات -->
    <section id="tab-products" style="display:none">
      <h2>إدارة المنتجات — إضافة / تعديل السعر والصور والمواصفات</h2>
      <div class="panel">
        <h3 id="pFormTitle">➕ إضافة منتج جديد</h3>
        <div class="admin-form">
          <input id="pName" placeholder="اسم المنتج *" />
          <input id="pPrice" type="number" placeholder="السعر *" />
          <input id="pOld" type="number" placeholder="السعر قبل الخصم" />
          <input id="pImage" placeholder="رابط الصورة URL" />
          <select id="pCat">
            <option value="mobiles">📱 موبايلات</option>
            <option value="laptops">💻 لابتوبات</option>
            <option value="audio">🎧 صوتيات</option>
            <option value="tv">📺 شاشات</option>
            <option value="gaming">🎮 ألعاب</option>
            <option value="accessories">⌚ إكسسوارات</option>
          </select>
          <input id="pBrand" placeholder="الماركة" />
          <input id="pStock" type="number" placeholder="المخزون" />
          <input id="pSpecs" placeholder='المواصفات: الشاشة=6.7 بوصة, الرام=8GB' />
          <input id="pDesc" placeholder="الوصف" />
          <label style="font-size:13px"><input type="checkbox" id="pFeat" /> مميز ⭐</label>
        </div>
        <div style="display:flex;gap:8px;margin-top:10px">
          <button class="btn" id="pSaveBtn" onclick="saveProduct()">حفظ 💾</button>
          <button class="btn btn-ghost" onclick="resetProductForm()">إلغاء</button>
        </div>
      </div>
      <div class="panel"><h3>كل المنتجات</h3><div style="overflow-x:auto"><table class="data" id="productsTable"></table></div></div>
    </section>

    <!-- الطلبات -->
    <section id="tab-orders" style="display:none">
      <h2>الطلبات والمبيعات</h2>
      <div class="panel"><div id="ordersList"></div></div>
    </section>

    <!-- الرئيسية -->
    <section id="tab-home" style="display:none">
      <h2>أقسام الصفحة الرئيسية القابلة للتعديل</h2>
      <div id="sectionsList"></div>
    </section>
  </main>

  <div class="toast" id="toast"></div>
  <script src="config.js"></script>
  <script src="admin.js"></script>
</body>
</html>


======================================================================
FILE: electronics-store/frontend/login.html
======================================================================

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>تسجيل الدخول | تِك ستور</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="container">
    <div class="login-card">
      <a class="logo" href="index.html" style="text-decoration:none">تِك <span>ستور</span> ⚡</a>
      <div class="tabs">
        <button class="tab active" id="tabLogin" onclick="switchTab('login')">تسجيل الدخول</button>
        <button class="tab" id="tabReg" onclick="switchTab('reg')">حساب جديد</button>
      </div>
      <div class="form-grid" id="loginForm">
        <label>البريد الإلكتروني<input id="lEmail" type="email" placeholder="you@mail.com" /></label>
        <label>كلمة المرور<input id="lPass" type="password" placeholder="••••••" /></label>
        <button class="btn btn-big btn-block" onclick="doLogin()">دخول 🚀</button>
      </div>
      <div class="form-grid" id="regForm" style="display:none">
        <label>الاسم<input id="rName" placeholder="اسمك بالكامل" /></label>
        <label>البريد الإلكتروني<input id="rEmail" type="email" placeholder="you@mail.com" /></label>
        <label>كلمة المرور (6 أحرف على الأقل)<input id="rPass" type="password" placeholder="••••••" /></label>
        <button class="btn btn-big btn-block" onclick="doRegister()">إنشاء الحساب ✨</button>
      </div>
      <div class="hint">🔑 حساب الأدمن التجريبي:<br><b dir="ltr">admin@store.com / admin123</b></div>
      <p style="text-align:center"><a href="index.html">→ الرجوع للمتجر</a></p>
    </div>
  </div>
  <div class="toast" id="toast"></div>
  <script src="config.js"></script>
  <script>
    const API = window.API_BASE || "http://localhost:8000";
    const $ = (id) => document.getElementById(id);
    function toast(m) { const t = $("toast"); t.textContent = m; t.classList.add("show"); setTimeout(() => t.classList.remove("show"), 2600); }
    function switchTab(which) {
      $("loginForm").style.display = which === "login" ? "grid" : "none";
      $("regForm").style.display = which === "reg" ? "grid" : "none";
      $("tabLogin").classList.toggle("active", which === "login");
      $("tabReg").classList.toggle("active", which === "reg");
    }
    function saveAndGo(d) {
      localStorage.setItem("token", d.access_token);
      localStorage.setItem("user", JSON.stringify(d.user));
      toast("أهلاً " + d.user.name + " 👋");
      setTimeout(() => location.href = d.user.is_admin ? "admin.html" : "index.html", 700);
    }
    async function doLogin() {
      const r = await fetch(`${API}/api/auth/login`, { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: $("lEmail").value.trim(), password: $("lPass").value }) });
      const d = await r.json();
      if (!r.ok) return toast(d.detail || "فشل الدخول");
      saveAndGo(d);
    }
    async function doRegister() {
      const r = await fetch(`${API}/api/auth/register`, { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: $("rName").value.trim(), email: $("rEmail").value.trim(), password: $("rPass").value }) });
      const d = await r.json();
      if (!r.ok) return toast(d.detail || "فشل إنشاء الحساب");
      saveAndGo(d);
    }
  </script>
</body>
</html>


======================================================================
FILE: electronics-store/frontend/styles.css
======================================================================

:root {
  --bg: #f4f6fb;
  --card: #ffffff;
  --text: #0f172a;
  --muted: #64748b;
  --primary: #1d4ed8;
  --primary-dark: #1e40af;
  --accent: #f59e0b;
  --green: #16a34a;
  --red: #dc2626;
  --border: #e2e8f0;
  --radius: 16px;
  --shadow: 0 8px 30px rgba(15, 23, 42, 0.08);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: "Segoe UI", Tahoma, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
}
img { max-width: 100%; display: block; }
a { color: inherit; }
.container { width: min(1200px, 92%); margin: 0 auto; }

/* الهيدر */
.header {
  position: sticky; top: 0; z-index: 50;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
}
.header-inner {
  display: flex; align-items: center; gap: 16px;
  padding: 12px 0;
}
.logo { font-size: 22px; font-weight: 800; color: var(--primary); text-decoration: none; }
.logo span { color: var(--accent); }
.searchbar { flex: 1; display: flex; gap: 8px; }
.searchbar input {
  flex: 1; padding: 11px 14px; border: 1.5px solid var(--border);
  border-radius: 12px; font-size: 15px; background: #fff;
}
.searchbar input:focus { outline: none; border-color: var(--primary); }
.btn {
  border: none; cursor: pointer; border-radius: 12px;
  padding: 11px 20px; font-size: 15px; font-weight: 700;
  background: var(--primary); color: #fff;
  transition: transform .08s ease, background .2s;
  text-decoration: none; display: inline-block; text-align: center;
}
.btn:hover { background: var(--primary-dark); }
.btn:active { transform: scale(0.97); }
.btn-ghost { background: #eef2ff; color: var(--primary); }
.btn-ghost:hover { background: #e0e7ff; }
.btn-green { background: var(--green); }
.btn-block { width: 100%; }
.btn-big { padding: 15px 26px; font-size: 18px; border-radius: 14px; }
.btn:disabled { opacity: .55; cursor: not-allowed; }
.icon-btn {
  position: relative; background: #eef2ff; border: none;
  border-radius: 12px; padding: 10px 14px; cursor: pointer; font-size: 18px;
}
.cart-count {
  position: absolute; top: -8px; left: -8px;
  background: var(--red); color: #fff; font-size: 12px; font-weight: 800;
  min-width: 22px; height: 22px; border-radius: 999px;
  display: flex; align-items: center; justify-content: center; padding: 0 5px;
}
.nav-links { display: flex; gap: 10px; align-items: center; }

/* الهيرو */
.hero {
  margin: 22px 0; border-radius: 22px; overflow: hidden;
  background: linear-gradient(120deg, #0f172a 30%, #1d4ed8 100%);
  color: #fff; display: grid; grid-template-columns: 1.1fr 1fr;
  min-height: 300px; box-shadow: var(--shadow);
}
.hero-text { padding: 44px 36px; }
.hero-text .badge {
  display: inline-block; background: var(--accent); color: #111;
  font-weight: 800; font-size: 13px; padding: 5px 14px; border-radius: 999px; margin-bottom: 12px;
}
.hero-text h1 { margin: 0 0 10px; font-size: 34px; line-height: 1.4; }
.hero-text p { color: #cbd5e1; margin: 0 0 22px; }
.hero-img img { width: 100%; height: 100%; object-fit: cover; min-height: 300px; }
.ship-strip {
  background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46;
  border-radius: 14px; padding: 12px 18px; margin-bottom: 18px; font-weight: 700;
}

/* الفلاتر */
.filters {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 16px;
  display: flex; flex-wrap: wrap; gap: 10px; align-items: end; margin-bottom: 18px;
  box-shadow: var(--shadow);
}
.filter-group { display: flex; flex-direction: column; gap: 6px; min-width: 150px; flex: 1; }
.filter-group label { font-size: 13px; color: var(--muted); font-weight: 700; }
.filter-group select, .filter-group input {
  padding: 10px 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 14px; background: #fff;
}
.section-title { margin: 26px 0 6px; font-size: 24px; }
.section-sub { color: var(--muted); margin: 0 0 16px; }

/* شبكة المنتجات */
.grid {
  display: grid; gap: 18px;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
}
.card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); overflow: hidden;
  display: flex; flex-direction: column; box-shadow: var(--shadow);
  transition: transform .15s ease;
}
.card:hover { transform: translateY(-4px); }
.card-img { position: relative; aspect-ratio: 4/3; background: #f1f5f9; overflow: hidden; }
.card-img img { width: 100%; height: 100%; object-fit: cover; }
.discount {
  position: absolute; top: 10px; right: 10px;
  background: var(--red); color: #fff; font-size: 13px; font-weight: 800;
  padding: 3px 12px; border-radius: 999px;
}
.card-body { padding: 14px 15px 16px; display: flex; flex-direction: column; gap: 8px; flex: 1; }
.card-cat { font-size: 12px; color: var(--muted); font-weight: 700; }
.card-name { font-weight: 800; font-size: 16px; margin: 0; min-height: 52px; }
.card-rating { color: var(--accent); font-size: 14px; font-weight: 700; }
.card-rating small { color: var(--muted); font-weight: 400; }
.card-specs { font-size: 12.5px; color: var(--muted); }
.price-row { display: flex; align-items: baseline; gap: 10px; margin-top: auto; }
.price { font-size: 21px; font-weight: 800; color: var(--primary); }
.old-price { color: var(--muted); text-decoration: line-through; font-size: 14px; }
.stock-low { color: var(--red); font-size: 13px; font-weight: 700; }
.stock-ok { color: var(--green); font-size: 13px; }

/* السلة */
.drawer-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,.45);
  opacity: 0; pointer-events: none; transition: opacity .2s; z-index: 90;
}
.drawer-overlay.open { opacity: 1; pointer-events: auto; }
.drawer {
  position: fixed; top: 0; bottom: 0; left: 0; width: min(420px, 94vw);
  background: #fff; z-index: 100; padding: 20px;
  transform: translateX(-105%); transition: transform .25s ease;
  display: flex; flex-direction: column; gap: 12px; overflow-y: auto;
}
.drawer.open { transform: translateX(0); }
.cart-item { display: flex; gap: 10px; border: 1px solid var(--border); border-radius: 12px; padding: 8px; align-items: center; }
.cart-item img { width: 70px; height: 70px; object-fit: cover; border-radius: 8px; }
.qty-ctrl { display: flex; gap: 8px; align-items: center; }
.qty-ctrl button { width: 28px; height: 28px; border-radius: 8px; border: 1px solid var(--border); background: #f8fafc; cursor: pointer; font-weight: 800; }
.cart-total { font-size: 18px; font-weight: 800; display: flex; justify-content: space-between; }

/* المودال */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,.5); z-index: 120;
  display: none; align-items: center; justify-content: center; padding: 16px;
}
.modal-overlay.open { display: flex; }
.modal { background: #fff; border-radius: 18px; padding: 24px; width: min(560px, 100%); max-height: 92vh; overflow-y: auto; }
.modal h2 { margin-top: 0; }
.form-grid { display: grid; gap: 12px; }
.form-grid label { font-size: 14px; font-weight: 700; display: grid; gap: 6px; }
.form-grid input, .form-grid textarea, .form-grid select {
  padding: 11px 13px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 15px; font-family: inherit;
}
.toast {
  position: fixed; bottom: 22px; right: 50%; transform: translateX(50%);
  background: #0f172a; color: #fff; padding: 12px 22px; border-radius: 12px;
  font-weight: 700; z-index: 200; display: none; box-shadow: var(--shadow);
}
.toast.show { display: block; }
.empty { text-align: center; color: var(--muted); padding: 50px 10px; }
.footer { margin: 40px 0 0; padding: 26px 0; border-top: 1px solid var(--border); color: var(--muted); text-align: center; }

/* تفاصيل المنتج */
.product-detail { display: grid; grid-template-columns: 1fr 1fr; gap: 26px; background: #fff; border-radius: 20px; padding: 26px; box-shadow: var(--shadow); margin-top: 20px; }
.product-detail img { border-radius: 16px; width: 100%; aspect-ratio: 4/3; object-fit: cover; }
.specs-table { width: 100%; border-collapse: collapse; margin-top: 12px; }
.specs-table td { border: 1px solid var(--border); padding: 9px 12px; font-size: 14px; }
.specs-table td:first-child { background: #f8fafc; font-weight: 700; width: 35%; }

/* الداش بورد */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 14px; margin: 14px 0 22px; }
.stat { background: #fff; border: 1px solid var(--border); border-radius: 14px; padding: 16px; box-shadow: var(--shadow); }
.stat .label { font-size: 13px; color: var(--muted); font-weight: 700; }
.stat .value { font-size: 26px; font-weight: 800; margin-top: 4px; }
.stat.blue .value { color: var(--primary); }
.stat.green .value { color: var(--green); }
.stat.red .value { color: var(--red); }
.stat.orange .value { color: #ea580c; }
.panel { background: #fff; border: 1px solid var(--border); border-radius: 14px; padding: 18px; margin-bottom: 18px; box-shadow: var(--shadow); }
.panel h3 { margin: 0 0 12px; }
table.data { width: 100%; border-collapse: collapse; font-size: 14px; }
table.data th, table.data td { border-bottom: 1px solid var(--border); padding: 9px 8px; text-align: right; }
table.data th { color: var(--muted); font-size: 13px; }
.badge-status { padding: 3px 12px; border-radius: 999px; font-size: 12.5px; font-weight: 800; }
.st-pending { background: #fef3c7; color: #92400e; }
.st-confirmed { background: #dbeafe; color: #1e40af; }
.st-shipped { background: #e0e7ff; color: #3730a3; }
.st-delivered { background: #dcfce7; color: #166534; }
.st-cancelled { background: #fee2e2; color: #991b1b; }
.tabs { display: flex; gap: 8px; margin: 18px 0; flex-wrap: wrap; }
.tab { border: 1.5px solid var(--border); background: #fff; padding: 9px 18px; border-radius: 999px; cursor: pointer; font-weight: 700; }
.tab.active { background: var(--primary); color: #fff; border-color: var(--primary); }
.admin-form { display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 10px; }
.admin-form input, .admin-form select, .admin-form textarea { padding: 10px 12px; border: 1.5px solid var(--border); border-radius: 10px; font-size: 14px; font-family: inherit; }
.bar-row { display: flex; align-items: center; gap: 10px; margin: 6px 0; font-size: 13px; }
.bar { height: 10px; background: #e2e8f0; border-radius: 99px; flex: 1; overflow: hidden; }
.bar > div { height: 100%; background: var(--primary); border-radius: 99px; }

.login-card { max-width: 430px; margin: 60px auto; background: #fff; border-radius: 20px; padding: 30px; box-shadow: var(--shadow); border: 1px solid var(--border); }
.hint { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; border-radius: 10px; padding: 10px 14px; font-size: 14px; margin-top: 14px; }

@media (max-width: 800px) {
  .hero { grid-template-columns: 1fr; }
  .hero-img img { min-height: 200px; max-height: 240px; }
  .product-detail { grid-template-columns: 1fr; }
  .header-inner { flex-wrap: wrap; }
  .searchbar { order: 3; flex-basis: 100%; }
}


======================================================================
FILE: electronics-store/frontend/config.js
======================================================================

/* إعدادات المتجر — تُقرأ من .env.local مع قيم افتراضية آمنة.
   ملاحظة: app.js و admin.js يستخدمان window.ENV بعد تحميله،
   لذا config.js يُحمّل synchronously قبل أي fetch (انظر init في app.js). */
window.ENV = {
  API_BASE: "http://localhost:8000",
  STORE_NAME: "تِك ستور",
  FREE_SHIPPING_LIMIT: 5000,
  SHIPPING_FEE: 60,
};
window.API_BASE = window.ENV.API_BASE;

(function loadDotEnv() {
  function parse(text) {
    const out = {};
    text.split("\n").forEach((line) => {
      const clean = line.trim();
      if (!clean || clean.startsWith("#")) return;
      const i = clean.indexOf("=");
      if (i > 0) out[clean.slice(0, i).trim()] = clean.slice(i + 1).trim();
    });
    return out;
  }
  function apply(vars) {
    if (vars.VITE_API_BASE) window.ENV.API_BASE = vars.VITE_API_BASE.replace(/\/$/, "");
    if (vars.VITE_STORE_NAME) window.ENV.STORE_NAME = vars.VITE_STORE_NAME;
    if (vars.VITE_FREE_SHIPPING_LIMIT) window.ENV.FREE_SHIPPING_LIMIT = Number(vars.VITE_FREE_SHIPPING_LIMIT) || 5000;
    if (vars.VITE_SHIPPING_FEE) window.ENV.SHIPPING_FEE = Number(vars.VITE_SHIPPING_FEE) || 0;
    window.API_BASE = window.ENV.API_BASE; // للتوافق مع الكود الحالي
  }
  try {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", ".env.local", false); // تحميل متزامن قبل app.js
    xhr.send(null);
    if (xhr.status === 200) apply(parse(xhr.responseText));
  } catch (e) { /* القيم الافتراضية تكفي */ }
})();


======================================================================
FILE: electronics-store/frontend/app.js
======================================================================

/* منطق المتجر: منتجات سريعة + بحث وفلاتر + سلة + شراء كضيف + تتبع من API */
const API = window.API_BASE || "http://localhost:8000";
const CATS_AR = { mobiles: "📱 موبايلات", laptops: "💻 لابتوبات", audio: "🎧 صوتيات", tv: "📺 شاشات", gaming: "🎮 ألعاب", accessories: "⌚ إكسسوارات" };

let PRODUCTS = [];
let cart = JSON.parse(localStorage.getItem("cart") || "[]");
let sessionId = localStorage.getItem("sid") || ("s" + Math.random().toString(36).slice(2) + Date.now().toString(36));
localStorage.setItem("sid", sessionId);

const $ = (id) => document.getElementById(id);
const fmt = (n) => Number(n || 0).toLocaleString("ar-EG") + " ج.م";

function toast(msg) {
  const t = $("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2600);
}

async function trackVisit() {
  try {
    await fetch(`${API}/api/dashboard/track/visit`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ page: "home", session_id: sessionId }),
    });
  } catch (e) { /* يعمل المتجر حتى لو الإحصائيات تعطلت */ }
}

async function trackCart(productId) {
  try {
    await fetch(`${API}/api/dashboard/track/cart`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product_id: productId, event_type: "add", session_id: sessionId }),
    });
  } catch (e) {}
}

/* أقسام الصفحة الرئيسية القابلة للتعديل من الداش بورد */
async function loadHomepage() {
  try {
    const r = await fetch(`${API}/api/homepage?visible_only=true`);
    const sections = await r.json();
    const byKey = Object.fromEntries(sections.map((s) => [s.key, s]));
    if (byKey.hero) {
      if (byKey.hero.title) $("heroTitle").textContent = byKey.hero.title;
      if (byKey.hero.subtitle) $("heroSubtitle").textContent = byKey.hero.subtitle;
      if (byKey.hero.image_url) $("heroImg").src = byKey.hero.image_url;
      if (byKey.hero.content?.button_text) $("heroBtn").textContent = byKey.hero.content.button_text + " 🛍️";
      if (byKey.hero.content?.badge) $("heroBadge").textContent = byKey.hero.content.badge;
      $("heroSection").style.display = byKey.hero.is_visible === false ? "none" : "";
    }
    if (byKey.banner_shipping) {
      $("shipStrip").textContent = `🚚 ${byKey.banner_shipping.title} — ${byKey.banner_shipping.subtitle}`;
    }
    if (byKey.featured_title) {
      if (byKey.featured_title.title) $("featuredTitle").textContent = byKey.featured_title.title;
      if (byKey.featured_title.subtitle) $("featuredSub").textContent = byKey.featured_title.subtitle;
    }
  } catch (e) { /* قيم افتراضية من HTML */ }
}

async function loadMeta() {
  try {
    const r = await fetch(`${API}/api/products/categories`);
    const data = await r.json();
    const catSel = $("fCategory"), brandSel = $("fBrand");
    (data.categories || []).forEach((c) => {
      const n = data.counts?.[c] ? ` (${data.counts[c]})` : "";
      catSel.insertAdjacentHTML("beforeend", `<option value="${c}">${CATS_AR[c] || c}${n}</option>`);
    });
    (data.brands || []).forEach((b) => {
      brandSel.insertAdjacentHTML("beforeend", `<option value="${b}">${b}</option>`);
    });
    const hashCat = new URLSearchParams(location.hash.slice(1)).get("cat");
    if (hashCat) catSel.value = hashCat;
  } catch (e) {}
}

async function loadProducts() {
  const grid = $("grid");
  grid.innerHTML = "<div class='empty'>جاري تحميل المنتجات... ⏳</div>";
  const q = new URLSearchParams({
    search: $("searchInput").value.trim(),
    category: $("fCategory").value,
    brand: $("fBrand").value,
    min_price: $("fMin").value || 0,
    max_price: $("fMax").value || 0,
    sort: $("fSort").value,
    limit: 60,
  });
  try {
    const r = await fetch(`${API}/api/products?${q}`);
    PRODUCTS = await r.json();
  } catch (e) {
    grid.innerHTML = "<div class='empty'>تعذر الاتصال بالسيرفر — تأكد أن الباك إند يعمل على المنفذ 8000 ⚠️</div>";
    return;
  }
  $("emptyState").style.display = PRODUCTS.length ? "none" : "block";
  grid.innerHTML = PRODUCTS.map(cardHTML).join("");
}

function cardHTML(p) {
  const disc = p.old_price && p.old_price > p.price ? Math.round((1 - p.price / p.old_price) * 100) : 0;
  const specs = Object.entries(p.specs || {}).slice(0, 2).map(([k, v]) => `${k}: ${v}`).join(" • ");
  return `
  <article class="card">
    <div class="card-img" onclick="showDetail(${p.id})" style="cursor:pointer">
      ${disc ? `<span class="discount">-${disc}%</span>` : ""}
      <img src="${p.image_url || "https://via.placeholder.com/600x450?text=No+Image"}" alt="${p.name}" loading="lazy" />
    </div>
    <div class="card-body">
      <span class="card-cat">${CATS_AR[p.category] || p.category} • ${p.brand || ""}</span>
      <h3 class="card-name">${p.name}</h3>
      <div class="card-rating">★ ${p.rating} <small>(${p.reviews_count} تقييم)</small></div>
      ${specs ? `<div class="card-specs">${specs}</div>` : ""}
      <div class="price-row"><span class="price">${fmt(p.price)}</span>${p.old_price ? `<span class="old-price">${fmt(p.old_price)}</span>` : ""}</div>
      ${p.stock <= 8 ? `<span class="stock-low">⚠️ باقي ${p.stock} فقط!</span>` : `<span class="stock-ok">✅ متوفر</span>`}
      <div style="display:flex;gap:8px;margin-top:6px">
        <button class="btn btn-green" style="flex:1" onclick="addToCart(${p.id})">اشترِ الآن 🛒</button>
        <button class="btn btn-ghost" onclick="showDetail(${p.id})">التفاصيل</button>
      </div>
    </div>
  </article>`;
}

function applyFilters() { loadProducts(); }

function addToCart(id) {
  const p = PRODUCTS.find((x) => x.id === id);
  if (!p) return;
  const line = cart.find((x) => x.product_id === id);
  if (line) {
    if (line.qty >= p.stock) return toast("وصلت للحد المتاح من المخزون");
    line.qty++;
  } else cart.push({ product_id: id, qty: 1 });
  localStorage.setItem("cart", JSON.stringify(cart));
  renderCart();
  trackCart(id);
  toast(`اتضافت للسلة: ${p.name} ✅`);
  toggleCart(true);
}

function changeQty(id, d) {
  const line = cart.find((x) => x.product_id === id);
  if (!line) return;
  line.qty += d;
  if (line.qty <= 0) cart = cart.filter((x) => x.product_id !== id);
  localStorage.setItem("cart", JSON.stringify(cart));
  renderCart();
}

function cartDetailed() {
  return cart.map((l) => ({ ...l, product: PRODUCTS.find((p) => p.id === l.product_id) })).filter((x) => x.product);
}

function cartSubtotal() {
  return cartDetailed().reduce((s, x) => s + x.product.price * x.qty, 0);
}

function renderCart() {
  const items = cartDetailed();
  const count = items.reduce((s, x) => s + x.qty, 0);
  $("cartCount").textContent = count;
  $("cartItems").innerHTML = items.length ? items.map((x) => `
    <div class="cart-item">
      <img src="${x.product.image_url}" alt="" />
      <div style="flex:1">
        <div style="font-weight:800;font-size:14px">${x.product.name}</div>
        <div style="color:var(--primary);font-weight:800">${fmt(x.product.price)}</div>
        <div class="qty-ctrl"><button onclick="changeQty(${x.product_id},-1)">−</button><b>${x.qty}</b><button onclick="changeQty(${x.product_id},1)">+</button></div>
      </div>
    </div>`).join("") : "<div class='empty'>سلتك فاضية — اختار حاجة تعجبك 😍</div>";
  $("cartTotal").textContent = fmt(cartSubtotal());
}

function toggleCart(open) {
  $("cartDrawer").classList.toggle("open", open);
  $("cartOverlay").classList.toggle("open", open);
}

function openCheckout() {
  if (!cart.length) return toast("السلة فاضية — ضيف منتج الأول");
  const ENV = window.ENV || {};
  const sub = cartSubtotal();
  const limit = ENV.FREE_SHIPPING_LIMIT || 5000;
  const fee = ENV.SHIPPING_FEE ?? 60;
  const ship = sub >= limit ? 0 : fee;
  $("checkoutTotal").textContent = fmt(sub + ship) + (ship === 0 ? " (شحن مجاني 🎉)" : "");
  $("orderSuccess").innerHTML = "";
  $("checkoutModal").classList.add("open");
}
function closeCheckout() { $("checkoutModal").classList.remove("open"); }

async function confirmOrder() {
  const name = $("cName").value.trim(), phone = $("cPhone").value.trim(), address = $("cAddress").value.trim();
  if (name.length < 2) return toast("اكتب الاسم بالكامل");
  if (phone.length < 6) return toast("اكتب رقم موبايل صحيح");
  if (address.length < 4) return toast("اكتب العنوان بالتفصيل");
  $("confirmBtn").disabled = true;
  try {
    const r = await fetch(`${API}/api/orders`, {
      method: "POST", headers: { "Content-Type": "application/json", ...(token() ? { Authorization: "Bearer " + token() } : {}) },
      body: JSON.stringify({
        customer_name: name, phone, address,
        email: $("cEmail").value.trim() || null,
        payment_method: $("cPay").value, notes: $("cNotes").value.trim(),
        items: cart.map((l) => ({ product_id: l.product_id, quantity: l.qty })),
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || "فشل إنشاء الطلب");
    cart = [];
    localStorage.setItem("cart", JSON.stringify(cart));
    renderCart();
    $("orderSuccess").innerHTML = `<div class="hint">🎉 تم استلام طلبك بنجاح!<br>رقم الطلب: <b dir="ltr">${data.order_number}</b><br>الإجمالي: <b>${fmt(data.total)}</b> — الدفع عند الاستلام<br><button class="btn" style="margin-top:10px" onclick="closeCheckout();toggleCart(false)">تمام ✅</button></div>`;
    toast("طلبك اتسجل بنجاح 🎉");
  } catch (e) { toast(e.message); }
  $("confirmBtn").disabled = false;
}

async function showDetail(id) {
  let p = PRODUCTS.find((x) => x.id === id);
  try {
    const r = await fetch(`${API}/api/products/${id}`);
    if (r.ok) p = await r.json();
  } catch (e) {}
  if (!p) return;
  const rows = Object.entries(p.specs || {}).map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join("");
  $("detailBody").innerHTML = `
    <div class="product-detail" style="margin:0;box-shadow:none;padding:0">
      <img src="${p.image_url}" alt="${p.name}" />
      <div>
        <span class="card-cat">${CATS_AR[p.category] || p.category} • ${p.brand}</span>
        <h2 style="margin:6px 0">${p.name}</h2>
        <div class="card-rating">★ ${p.rating} <small>(${p.reviews_count} تقييم)</small></div>
        <p style="color:var(--muted)">${p.description}</p>
        <div class="price-row"><span class="price" style="font-size:28px">${fmt(p.price)}</span>${p.old_price ? `<span class="old-price">${fmt(p.old_price)}</span>` : ""}</div>
        <button class="btn btn-green btn-big btn-block" style="margin-top:12px" onclick="addToCart(${p.id});document.getElementById('detailModal').classList.remove('open')">اشترِ الآن 🛒</button>
        ${rows ? `<table class="specs-table">${rows}</table>` : ""}
      </div>
    </div>`;
  $("detailModal").classList.add("open");
}

async function trackOrders() {
  const phone = $("trackPhone").value.trim();
  if (!phone) return toast("دخل رقم الموبايل الأول");
  const box = $("myOrders");
  box.innerHTML = "جاري البحث... ⏳";
  try {
    const r = await fetch(`${API}/api/orders?phone=${encodeURIComponent(phone)}`);
    const orders = await r.json();
    if (!orders.length) { box.innerHTML = "<div class='empty'>لا توجد طلبات بهذا الرقم</div>"; return; }
    box.innerHTML = orders.map((o) => `
      <div class="panel">
        <b dir="ltr">${o.order_number}</b> — <span class="badge-status st-${o.status}">${statusAr(o.status)}</span>
        <div style="font-size:14px;color:var(--muted)">${o.items.map((i) => `${i.product_name} × ${i.quantity}`).join("، ")} — الإجمالي: <b style="color:var(--primary)">${fmt(o.total)}</b></div>
        ${o.status === "pending" || o.status === "confirmed" ? `<button class="btn btn-ghost" style="margin-top:8px" onclick="cancelOrder(${o.id})">إلغاء الطلب</button>` : ""}
      </div>`).join("");
  } catch (e) { box.innerHTML = "<div class='empty'>تعذر الاتصال بالسيرفر</div>"; }
}

async function cancelOrder(id) {
  if (!confirm("متأكد من إلغاء الطلب؟")) return;
  const r = await fetch(`${API}/api/orders/${id}/cancel`, { method: "PATCH" });
  if (r.ok) { toast("تم إلغاء الطلب"); trackOrders(); }
  else toast("تعذر الإلغاء");
}

function statusAr(s) {
  return { pending: "قيد المراجعة", confirmed: "مؤكد", shipped: "تم الشحن", delivered: "تم التوصيل", cancelled: "ملغي" }[s] || s;
}
function token() { return localStorage.getItem("token"); }

function refreshAuthUI() {
  const t = token();
  $("loginLink").style.display = t ? "none" : "";
  $("adminLink").style.display = t ? "" : "none";
  if (t) {
    fetch(`${API}/api/auth/me`, { headers: { Authorization: "Bearer " + t } })
      .then((r) => (r.ok ? r.json() : null))
      .then((u) => { if (u?.is_admin) $("adminLink").style.display = ""; });
  }
}

$("searchInput").addEventListener("keydown", (e) => { if (e.key === "Enter") applyFilters(); });

(async function init() {
  refreshAuthUI();
  await loadHomepage();
  await loadMeta();
  await loadProducts();
  renderCart();
  trackVisit();
})();


======================================================================
FILE: electronics-store/frontend/admin.js
======================================================================

/* الداش بورد: جزأين + إدارة منتجات + طلبات + أقسام الرئيسية */
const API = window.API_BASE || "http://localhost:8000";
const $ = (id) => document.getElementById(id);
const fmt = (n) => Number(n || 0).toLocaleString("ar-EG") + " ج.م";
let editingId = null;

function toast(m) { const t = $("toast"); t.textContent = m; t.classList.add("show"); setTimeout(() => t.classList.remove("show"), 2600); }
function token() { return localStorage.getItem("token"); }
function headers() { return { "Content-Type": "application/json", Authorization: "Bearer " + token() }; }
function logout() { localStorage.removeItem("token"); localStorage.removeItem("user"); location.href = "index.html"; }
function showTab(name, btn) {
  ["dash", "products", "orders", "home"].forEach((t) => ($("tab-" + t).style.display = t === name ? "" : "none"));
  document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
}

async function guard() {
  if (!token()) { location.href = "login.html"; return false; }
  const r = await fetch(`${API}/api/auth/me`, { headers: { Authorization: "Bearer " + token() } });
  if (!r.ok) { location.href = "login.html"; return false; }
  const u = await r.json();
  if (!u.is_admin) { toast("هذه الصفحة للإدارة فقط"); setTimeout(() => (location.href = "index.html"), 800); return false; }
  return true;
}

function stat(label, value, cls) {
  return `<div class="stat ${cls || ""}"><div class="label">${label}</div><div class="value">${value}</div></div>`;
}
function barChart(rows, labelKey, valKey, color) {
  const max = Math.max(1, ...rows.map((r) => r[valKey]));
  return rows.map((r) => `
    <div class="bar-row"><span style="min-width:70px">${r[labelKey].slice(5)}</span>
    <div class="bar"><div style="width:${Math.round((r[valKey] / max) * 100)}%;background:${color}"></div></div>
    <b>${r[valKey].toLocaleString("ar-EG")}</b></div>`).join("");
}

async function loadDashboard() {
  const cxR = await fetch(`${API}/api/dashboard/customer-experience`, { headers: headers() });
  const stR = await fetch(`${API}/api/dashboard/store`, { headers: headers() });
  if (!cxR.ok || !stR.ok) return toast("تعذر تحميل الداش بورد");
  const cx = await cxR.json(), st = await stR.json();

  $("cxStats").innerHTML =
    stat("👁️ إجمالي الزيارات", cx.total_visits.toLocaleString("ar-EG"), "blue") +
    stat("📅 زيارات اليوم", cx.visits_today.toLocaleString("ar-EG"), "blue") +
    stat("🛒 إضافة للسلة (كلي)", cx.cart_adds_total.toLocaleString("ar-EG"), "orange") +
    stat("🛒 إضافة اليوم", cx.cart_adds_today.toLocaleString("ar-EG"), "orange") +
    stat("📈 معدل الإضافة للسلة", cx.add_to_cart_rate_percent + "%", "green") +
    stat("👥 جلسات فريدة", (cx.unique_sessions || 0).toLocaleString("ar-EG"), "");
  $("visitsChart").innerHTML = barChart(cx.visits_last_14_days, "date", "visits", "#1d4ed8");
  $("topAdded").innerHTML = cx.top_added_products.length
    ? `<table class="data"><tr><th>المنتج</th><th>مرات الإضافة</th></tr>${cx.top_added_products.map((p) => `<tr><td>${p.name}</td><td>${p.adds}</td></tr>`).join("")}</table>`
    : "لا توجد بيانات بعد — تصفح المتجر واضف منتجات للسلة";

  $("storeStats").innerHTML =
    stat("💰 إجمالي المبيعات", fmt(st.total_sales), "green") +
    stat("📅 مبيعات اليوم", fmt(st.sales_today), "green") +
    stat("🧾 عدد الطلبات", st.orders_count.toLocaleString("ar-EG"), "blue") +
    stat("📦 طلبات اليوم", st.orders_today.toLocaleString("ar-EG"), "blue") +
    stat("❌ الملغي", st.cancelled_count.toLocaleString("ar-EG"), "red") +
    stat("⚠️ معدل الإلغاء", st.cancel_rate_percent + "%", "red");
  $("revenueChart").innerHTML = barChart(st.revenue_last_14_days, "date", "revenue", "#16a34a");
  $("topSelling").innerHTML = st.top_selling_products.length
    ? `<table class="data"><tr><th>المنتج</th><th>الكمية</th><th>الإيراد</th></tr>${st.top_selling_products.map((p) => `<tr><td>${p.name}</td><td>${p.quantity}</td><td>${fmt(p.revenue)}</td></tr>`).join("")}</table>`
    : "لا توجد مبيعات بعد";
  $("lowStock").innerHTML = st.low_stock.length
    ? `<table class="data"><tr><th>المنتج</th><th>المخزون</th></tr>${st.low_stock.map((p) => `<tr><td>${p.name}</td><td style="color:var(--red);font-weight:800">${p.stock}</td></tr>`).join("")}</table>`
    : "المخزون بحالة جيدة ✅";
}

/* المنتجات */
function parseSpecs(text) {
  const out = {};
  (text || "").split(/[,،\n]/).forEach((pair) => {
    const i = pair.indexOf("=");
    if (i > 0) out[pair.slice(0, i).trim()] = pair.slice(i + 1).trim();
  });
  return out;
}

async function loadProducts() {
  const r = await fetch(`${API}/api/products?limit=200&include_inactive=true`);
  const list = await r.json();
  $("productsTable").innerHTML = `<tr><th>المنتج</th><th>الفئة</th><th>السعر</th><th>المخزون</th><th>إجراءات</th></tr>` +
    list.map((p) => `<tr>
      <td><b>${p.name}</b><br><small style="color:var(--muted)">${p.is_active ? "ظاهر ✅" : "مخفي 🚫"}</small></td>
      <td>${p.category}</td><td><b>${fmt(p.price)}</b></td><td>${p.stock}</td>
      <td style="white-space:nowrap">
        <button class="btn btn-ghost" onclick="editProduct(${p.id})">تعديل</button>
        <button class="btn btn-ghost" onclick="deleteProduct(${p.id})">إخفاء</button>
      </td></tr>`).join("");
  window._allProducts = list;
}

function editProduct(id) {
  const p = window._allProducts.find((x) => x.id === id);
  if (!p) return;
  editingId = id;
  $("pFormTitle").textContent = "✏️ تعديل: " + p.name;
  $("pName").value = p.name; $("pPrice").value = p.price; $("pOld").value = p.old_price || "";
  $("pImage").value = p.image_url; $("pCat").value = p.category; $("pBrand").value = p.brand;
  $("pStock").value = p.stock; $("pDesc").value = p.description; $("pFeat").checked = p.is_featured;
  $("pSpecs").value = Object.entries(p.specs || {}).map(([k, v]) => `${k}=${v}`).join(", ");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function resetProductForm() {
  editingId = null;
  ["pName", "pPrice", "pOld", "pImage", "pBrand", "pStock", "pSpecs", "pDesc"].forEach((i) => ($(i).value = ""));
  $("pFeat").checked = false;
  $("pFormTitle").textContent = "➕ إضافة منتج جديد";
}

async function saveProduct() {
  const body = {
    name: $("pName").value.trim(),
    price: Number($("pPrice").value),
    old_price: $("pOld").value ? Number($("pOld").value) : null,
    image_url: $("pImage").value.trim(),
    category: $("pCat").value, brand: $("pBrand").value.trim(),
    stock: $("pStock").value === "" ? 50 : Number($("pStock").value),
    specs: parseSpecs($("pSpecs").value),
    description: $("pDesc").value.trim(),
    is_featured: $("pFeat").checked,
  };
  if (!body.name || !(body.price > 0)) return toast("اكتب الاسم والسعر");
  const url = editingId ? `${API}/api/products/${editingId}` : `${API}/api/products`;
  const r = await fetch(url, { method: editingId ? "PUT" : "POST", headers: headers(), body: JSON.stringify(body) });
  const d = await r.json();
  if (!r.ok) return toast(d.detail || "فشل الحفظ");
  toast(editingId ? "تم التعديل ✅" : "تمت الإضافة ✅");
  resetProductForm(); loadProducts();
}

async function deleteProduct(id) {
  if (!confirm("إخفاء هذا المنتج من المتجر؟")) return;
  await fetch(`${API}/api/products/${id}`, { method: "DELETE", headers: headers() });
  toast("تم الإخفاء"); loadProducts();
}

/* الطلبات */
function statusAr(s) {
  return { pending: "قيد المراجعة", confirmed: "مؤكد", shipped: "تم الشحن", delivered: "تم التوصيل", cancelled: "ملغي" }[s] || s;
}
async function loadOrders() {
  const r = await fetch(`${API}/api/orders`, { headers: headers() });
  const list = await r.json();
  $("ordersList").innerHTML = list.length ? `<table class="data">
    <tr><th>رقم الطلب</th><th>العميل</th><th>الإجمالي</th><th>الحالة</th><th>تغيير</th></tr>
    ${list.map((o) => `<tr>
      <td dir="ltr"><b>${o.order_number}</b><br><small>${o.phone}</small></td>
      <td>${o.customer_name}</td><td><b>${fmt(o.total)}</b></td>
      <td><span class="badge-status st-${o.status}">${statusAr(o.status)}</span></td>
      <td><select onchange="setStatus(${o.id},this.value)">
        ${["pending", "confirmed", "shipped", "delivered", "cancelled"].map((s) => `<option value="${s}" ${o.status === s ? "selected" : ""}>${statusAr(s)}</option>`).join("")}
      </select></td></tr>`).join("")}</table>` : "لا توجد طلبات بعد";
}
async function setStatus(id, status) {
  const r = await fetch(`${API}/api/orders/${id}/status`, { method: "PATCH", headers: headers(), body: JSON.stringify({ status }) });
  if (r.ok) { toast("تم تحديث الحالة ✅"); loadDashboard(); } else toast("فشل التحديث");
}

/* أقسام الرئيسية */
async function loadSections() {
  const r = await fetch(`${API}/api/homepage`);
  const list = await r.json();
  $("sectionsList").innerHTML = list.map((s) => `
    <div class="panel">
      <h3>🔹 ${s.key} ${s.is_visible ? "👁️" : "🚫"}</h3>
      <div class="admin-form">
        <input id="t-${s.key}" value="${(s.title || "").replace(/"/g, "&quot;")}" placeholder="العنوان" />
        <input id="s-${s.key}" value="${(s.subtitle || "").replace(/"/g, "&quot;")}" placeholder="الوصف" />
        <input id="i-${s.key}" value="${(s.image_url || "").replace(/"/g, "&quot;")}" placeholder="رابط الصورة" />
        <label style="font-size:13px"><input type="checkbox" id="v-${s.key}" ${s.is_visible ? "checked" : ""} /> ظاهر</label>
      </div>
      <button class="btn" style="margin-top:10px" onclick="saveSection('${s.key}')">حفظ القسم 💾</button>
    </div>`).join("");
}
async function saveSection(key) {
  const r = await fetch(`${API}/api/homepage/${key}`, {
    method: "PUT", headers: headers(),
    body: JSON.stringify({ title: $("t-" + key).value, subtitle: $("s-" + key).value, image_url: $("i-" + key).value, is_visible: $("v-" + key).checked }),
  });
  if (r.ok) toast("تم حفظ القسم ✅"); else toast("فشل الحفظ");
}

(async function init() {
  if (!(await guard())) return;
  await loadDashboard();
  await loadProducts();
  await loadOrders();
  await loadSections();
})();


======================================================================
FILE: electronics-store/frontend/.env.local
======================================================================

# إعدادات الفرونت إند — انسخ القيم حسب بيئتك
# رابط الباك إند (بدون / في الآخر)
VITE_API_BASE=http://localhost:8000
# اسم المتجر
VITE_STORE_NAME=تِك ستور
# حد الشحن المجاني (جنيه)
VITE_FREE_SHIPPING_LIMIT=5000
# رسوم الشحن (جنيه)
VITE_SHIPPING_FEE=60
# Supabase (المفتاح العام فقط — آمن للفرونت إند)
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=sb_publishable_RuMPEqMCHEUvvYDqN5w0ug_YG4cZbdc


