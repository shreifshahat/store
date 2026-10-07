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
