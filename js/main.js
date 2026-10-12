(function () {
  "use strict";
  var C = window.LAAJ || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var waLink = function (text) {
    return "https://wa.me/" + (C.whatsapp || "") + (text ? "?text=" + encodeURIComponent(text) : "");
  };

  /* ---------- Fill contact details from config ---------- */
  $$("[data-cfg]").forEach(function (el) {
    var v = C[el.getAttribute("data-cfg")];
    if (v) el.textContent = v;
  });
  var hrefs = {
    mailto: C.email && "mailto:" + C.email,
    tel: C.phoneE164 && "tel:" + C.phoneE164,
    sms: C.phoneE164 && "sms:" + C.phoneE164,
    whatsapp: C.whatsapp && waLink("Assalam o Alaikum Laaj Studios! I'd like to check availability for our wedding."),
    filmUrl: C.filmUrl,
    instagram: C.instagram
  };
  $$("[data-cfg-href]").forEach(function (el) {
    var v = hrefs[el.getAttribute("data-cfg-href")];
    if (v) { el.href = v; el.hidden = false; }
    else if (el.hasAttribute("hidden") || el.getAttribute("data-cfg-href") === "filmUrl" || el.getAttribute("data-cfg-href") === "instagram") el.hidden = true;
  });
  var y = $("#year"); if (y) y.textContent = new Date().getFullYear();

  /* ---------- Testimonials ---------- */
  var words = $("#words");
  if (words && C.testimonials && C.testimonials.length) {
    var list = $(".words__list", words);
    C.testimonials.forEach(function (t) {
      var q = document.createElement("blockquote");
      var p = document.createElement("p"); p.textContent = t.quote;
      var c = document.createElement("cite");
      var n = document.createElement("strong"); n.textContent = t.names;
      c.appendChild(n); if (t.event) c.appendChild(document.createTextNode(t.event));
      if (t.placeholder) {
        var tag = document.createElement("span");
        tag.className = "words__tag"; tag.textContent = "Placeholder";
        q.appendChild(tag);
      }
      q.appendChild(p); q.appendChild(c); list.appendChild(q);
    });
    words.hidden = false;
  }

  /* ---------- Lightbox ---------- */
  var lb = $("#lightbox");
  if (lb && typeof lb.showModal === "function") {
    var lbImg = $("img", lb);
    $$(".gallery__item").forEach(function (b) {
      b.addEventListener("click", function () {
        var img = $("img", b);
        lbImg.src = b.getAttribute("data-full"); lbImg.alt = img.alt;
        lb.showModal();
      });
    });
    lb.addEventListener("click", function () { lb.close(); });
  }

  /* ---------- Multi-step enquiry ---------- */
  var form = $("#enquiry-form");
  if (!form) return;
  var steps = $$(".form__step", form);
  var bars = $$(".form__progress li", form);
  var err = $(".form__error", form);
  var current = 0;

  // Keep campaign info so you can see which ads and posts bring enquiries.
  var params = new URLSearchParams(location.search);
  ["utm_source", "utm_medium", "utm_campaign", "gclid", "fbclid"].forEach(function (k) {
    if (params.get(k)) {
      var i = document.createElement("input");
      i.type = "hidden"; i.name = k; i.value = params.get(k); form.appendChild(i);
    }
  });

  var dateInput = $("#f-date"), flex = $("#f-date-flex");
  if (dateInput) dateInput.min = new Date().toISOString().slice(0, 10);
  if (flex) flex.addEventListener("change", function () {
    dateInput.disabled = flex.checked; dateInput.required = !flex.checked;
    dateInput.classList.remove("is-invalid");
  });

  function showError(msg) { err.textContent = msg; err.hidden = !msg; }

  function validate(step) {
    var ok = true;
    $$("input[required], select[required], textarea[required]", step).forEach(function (f) {
      if (f.disabled || f.type === "radio") return;
      var bad = !f.checkValidity();
      f.classList.toggle("is-invalid", bad);
      if (bad && ok) { f.focus(); ok = false; }
    });
    if (!ok) showError("Please complete the highlighted fields to continue.");
    else showError("");
    return ok;
  }

  function go(i) {
    steps[current].classList.remove("is-active");
    current = i;
    steps[current].classList.add("is-active");
    bars.forEach(function (b, n) {
      b.classList.toggle("is-active", n === current);
      b.classList.toggle("is-done", n < current);
    });
    var first = $("input:not([type=hidden]):not([type=checkbox]):not([type=radio]), select", steps[current]);
    if (first && window.innerWidth > 640) first.focus({ preventScroll: true });
  }

  $$("[data-next]", form).forEach(function (b) {
    b.addEventListener("click", function () { if (validate(steps[current])) go(current + 1); });
  });
  $$("[data-back]", form).forEach(function (b) {
    b.addEventListener("click", function () { showError(""); go(current - 1); });
  });
  $$("input, select, textarea", form).forEach(function (f) {
    f.addEventListener("input", function () { f.classList.remove("is-invalid"); });
  });

  function summary(fd) {
    var events = fd.getAll("events").join(", ") || "Not decided";
    var date = fd.get("date_flexible") ? "Not set yet" : (fd.get("wedding_date") || "Not set");
    return [
      "Wedding enquiry: " + fd.get("name") + (fd.get("partner") ? " & " + fd.get("partner") : ""),
      "Date: " + date,
      "Events: " + events,
      "Venue/city: " + (fd.get("venue") || "-"),
      "Guests: " + (fd.get("guests") || "-"),
      "Coverage: " + (fd.get("coverage") || "-"),
      "Budget: " + (fd.get("budget") || "-"),
      "Email: " + fd.get("email"),
      "Phone: " + fd.get("phone") + " (prefers " + fd.get("contact_pref") + ")",
      "Found us via: " + (fd.get("source") || "-"),
      fd.get("message") ? "Notes: " + fd.get("message") : ""
    ].filter(Boolean).join("\n");
  }

  function finish(fd, sentOnline) {
    steps.forEach(function (s) { s.classList.remove("is-active"); });
    $(".form__progress", form).hidden = true;
    var done = $(".form__done", form);
    if (!sentOnline) {
      $(".form__done-title", done).textContent = "Almost there. Please send the email.";
      $(".form__done-text", done).textContent = "Your email app should have opened with your enquiry written out. If it didn't, message us on WhatsApp or email " + (C.email || "us") + ".";
    }
    var wa = $("[data-whatsapp-summary]", done);
    if (C.whatsapp) wa.href = waLink("Assalam o Alaikum! I just sent an enquiry on your website.\n\n" + summary(fd));
    else wa.hidden = true;
    done.hidden = false;
    done.focus();
    if (window.gtag) window.gtag("event", "generate_lead", { event_category: "enquiry" });
    if (window.fbq) window.fbq("track", "Lead");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!validate(steps[current])) return;
    var fd = new FormData(form);
    if (fd.get("_gotcha")) return;
    var btn = $("button[type=submit]", form);

    if (C.formEndpoint) {
      btn.disabled = true; btn.textContent = "Sending…";
      fd.append("_subject", "New wedding enquiry: " + fd.get("name"));
      fd.append("summary", summary(fd));
      fetch(C.formEndpoint, { method: "POST", body: fd, headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error(r.status); finish(fd, true); })
        .catch(function () {
          btn.disabled = false; btn.textContent = "Check my date";
          showError("We couldn't send that just now. Please try again, or message us on WhatsApp.");
        });
    } else {
      location.href = "mailto:" + (C.email || "") + "?subject=" + encodeURIComponent("Wedding enquiry: " + fd.get("name")) + "&body=" + encodeURIComponent(summary(fd));
      finish(fd, false);
    }
  });
})();
