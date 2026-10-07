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
