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
