/* Mohsin Haematology Academy — site-wide cookie consent banner.
   No analytics is loaded by default. Mailchimp signup is the only third-party
   integration; this banner gives visitors a single route to the Privacy Notice.
   The banner self-injects on every page that includes this script and remembers
   acknowledgement via a first-party cookie. Once acknowledged, never re-shown. */
(function () {
  var KEY = "mha_cookie_ack";

  function isAcked() {
    return document.cookie.split("; ").some(function (r) {
      return r.indexOf(KEY + "=") === 0;
    });
  }

  function ack() {
    var oneYear = 60 * 60 * 24 * 365;
    document.cookie = KEY + "=1; max-age=" + oneYear + "; path=/; SameSite=Lax" +
      (location.protocol === "https:" ? "; Secure" : "");
  }

  if (isAcked()) return;

  function init() {
    var banner = document.createElement("div");
    banner.id = "mha-cookie-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-live", "polite");
    banner.setAttribute("aria-label", "Cookie consent");
    banner.style.cssText =
      "position:fixed;left:1rem;right:1rem;bottom:1rem;max-width:720px;" +
      "margin:0 auto;background:#ffffff;color:#1a1a1e;border:1px solid #e6e1dd;" +
      "border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,0.08);" +
      "padding:1rem 1.25rem;z-index:9999;" +
      "font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;font-size:0.9rem;";
    banner.innerHTML =
      '<div style="display:flex;flex-wrap:wrap;gap:0.75rem;align-items:center;justify-content:space-between;">' +
      '<p style="margin:0;flex:1 1 320px;">' +
      'We use a small number of cookies to keep the site working. The Academy newsletter is sent via Mailchimp, ' +
      'which may set cookies when you submit the signup form. See our ' +
      '<a href="/legal/privacy/" style="color:#7a1f2b;">Privacy Notice</a>.' +
      '</p>' +
      '<button id="mha-cookie-ack" type="button" style="' +
      'border:1px solid #7a1f2b;background:#7a1f2b;color:#ffffff;' +
      'padding:0.5rem 0.9rem;border-radius:8px;cursor:pointer;' +
      'font-family:inherit;font-size:0.9rem;font-weight:600;">OK, got it</button>' +
      '</div>';
    document.body.appendChild(banner);
    document.getElementById("mha-cookie-ack").addEventListener("click", function () {
      ack();
      banner.remove();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
