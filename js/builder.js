(function () {
  "use strict";
  var C = window.LAAJ || {};
  var P = window.LAAJ_PACKAGES;
  if (!P) return;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var STORE = "laaj-package-v1";

  var money = function (n) {
    return new Intl.NumberFormat("en-US", { style: "currency", currency: P.currency || "USD", maximumFractionDigits: 0 }).format(n);
  };
  var byId = function (list, id) {
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return list[0];
  };
  var el = function (tag, attrs, text) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (text != null) e.textContent = text;
    return e;
  };

  /* ---------- State ---------- */
  var uid = 0;
  var freshState = function () {
    return {
      events: P.events.defaults.map(function (d) {
        return { id: ++uid, type: d.type, name: "", hours: d.hours, photo: d.photo, film: d.film };
      }),
      choices: {}
    };
  };
  var state;
  try { state = JSON.parse(localStorage.getItem(STORE)); } catch (e) { state = null; }
  if (!state || !Array.isArray(state.events) || !state.choices) state = freshState();
  state.events.forEach(function (ev) { ev.id = ++uid; });
  var save = function () { try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) { /* storage unavailable */ } };

  var has = function (kind) {
    return state.events.some(function (ev) { return ev[kind] && ev[kind] !== "none"; });
  };

  /* ---------- Events ---------- */
  var list = $("#event-list");
  var addBtn = $("#add-event");

  var select = function (id, label, options, value, onChange) {
    var wrap = el("div", { "class": "b-field" });
    wrap.appendChild(el("label", { "for": id }, label));
    var s = el("select", { id: id });
    options.forEach(function (o) {
      var opt = el("option", { value: o.value }, o.text);
      if (String(o.value) === String(value)) opt.selected = true;
      s.appendChild(opt);
    });
    s.addEventListener("change", function () { onChange(s.value); });
    wrap.appendChild(s);
    return wrap;
  };

  var renderEvents = function () {
    list.textContent = "";
    state.events.forEach(function (ev, i) {
      var card = el("div", { "class": "b-event" });
      var head = el("div", { "class": "b-event__head" });
      head.appendChild(el("span", { "class": "b-event__num" }, "Event " + (i + 1)));
      if (state.events.length > 1) {
        var rm = el("button", { type: "button", "class": "b-event__remove", "aria-label": "Remove event " + (i + 1) }, "Remove");
        rm.addEventListener("click", function () {
          state.events = state.events.filter(function (x) { return x.id !== ev.id; });
          update(true);
        });
        head.appendChild(rm);
      }
      card.appendChild(head);

      var row1 = el("div", { "class": "b-row b-row--event" });
      row1.appendChild(select("ev-type-" + ev.id, "Event", P.events.types.map(function (t) { return { value: t, text: t }; }), ev.type, function (v) { ev.type = v; update(); }));
      var nameField = el("div", { "class": "b-field" });
      nameField.appendChild(el("label", { "for": "ev-name-" + ev.id }, "Name it (optional)"));
      var name = el("input", { id: "ev-name-" + ev.id, type: "text", maxlength: "40", placeholder: "e.g. Welcome dinner" });
      name.value = ev.name || "";
      name.addEventListener("input", function () { ev.name = name.value; update(); });
      nameField.appendChild(name);
      row1.appendChild(nameField);
      row1.appendChild(select("ev-hours-" + ev.id, "Hours", P.events.hours.map(function (h) { return { value: h, text: h + " hours" }; }), ev.hours, function (v) { ev.hours = Number(v); update(); }));
      card.appendChild(row1);

      var row2 = el("div", { "class": "b-row" });
      row2.appendChild(select("ev-photo-" + ev.id, "Photography", P.events.photo.map(function (o) {
        return { value: o.id, text: o.perHour ? o.label + " · " + money(o.perHour) + "/hr" : o.label };
      }), ev.photo, function (v) { ev.photo = v; update(); }));
      row2.appendChild(select("ev-film-" + ev.id, "Film", P.events.film.map(function (o) {
        return { value: o.id, text: o.perHour ? o.label + " · " + money(o.perHour) + "/hr" : o.label };
      }), ev.film, function (v) { ev.film = v; update(); }));
      card.appendChild(row2);

      var price = el("p", { "class": "b-event__price", "data-event-price": ev.id });
      card.appendChild(price);
      list.appendChild(card);
    });
    addBtn.hidden = state.events.length >= P.events.max;
  };

  addBtn.addEventListener("click", function () {
    var last = state.events[state.events.length - 1] || P.events.defaults[0];
    state.events.push({ id: ++uid, type: "Other event", name: "", hours: 4, photo: last.photo || "lead", film: last.film || "none" });
    update(true);
    var cards = $$(".b-event", list);
    var sel = cards.length && $("select", cards[cards.length - 1]);
    if (sel) sel.focus();
  });

  var eventPrice = function (ev) {
    return ev.hours * (byId(P.events.photo, ev.photo).perHour + byId(P.events.film, ev.film).perHour);
  };

  /* ---------- Deliverable sections ---------- */
  var sectionsHost = $("#b-sections");
  P.sections.forEach(function (sec) {
    var s = el("section", { "class": "b-section", id: "b-" + sec.id, "aria-labelledby": "b-" + sec.id + "-title" });
    var head = el("div", { "class": "b-section__head" });
    head.appendChild(el("h2", { id: "b-" + sec.id + "-title" }, sec.title));
    if (sec.intro) head.appendChild(el("p", null, sec.intro));
    s.appendChild(head);
    if (sec.requires) s.appendChild(el("p", { "class": "b-locked", "data-locked": sec.requires, hidden: "" },
      sec.requires === "film" ? "Add film coverage to at least one event to choose films." : "Add photography to at least one event to choose these."));
    var grid = el("div", { "class": "b-items" });
    sec.items.forEach(function (item) {
      var idx = state.choices[item.id] || 0;
      grid.appendChild(select("opt-" + item.id, item.label, item.options.map(function (o, i) {
        var tag = o.price ? " · " + money(o.price) : (i > 0 ? " · " + (o.note || "Included") : "");
        return { value: i, text: o.label + tag };
      }), idx, function (v) { state.choices[item.id] = Number(v); update(); }));
    });
    s.appendChild(grid);
    sectionsHost.appendChild(s);
  });

  /* ---------- Totals ---------- */
  var lines = function () {
    var out = [];
    state.events.forEach(function (ev, i) {
      var photo = byId(P.events.photo, ev.photo), film = byId(P.events.film, ev.film);
      var parts = [];
      if (photo.id !== "none") parts.push(photo.label);
      if (film.id !== "none") parts.push(film.label);
      out.push({
        group: "Events",
        label: (ev.name ? ev.name + " (" + ev.type + ")" : ev.type),
        detail: parts.length ? ev.hours + " hours · " + parts.join(" + ") : "No coverage chosen yet",
        price: eventPrice(ev),
        eventId: ev.id
      });
    });
    P.sections.forEach(function (sec) {
      var locked = sec.requires && !has(sec.requires);
      sec.items.forEach(function (item) {
        var i = state.choices[item.id] || 0;
        var o = item.options[i];
        if (locked || i === 0) return;
        out.push({ group: sec.title, label: item.label, detail: o.label, price: o.price, priceNote: o.price ? "" : (o.note || "Included") });
      });
    });
    return out;
  };
  var total = function (ls) { return ls.reduce(function (s, l) { return s + (l.price || 0); }, 0); };

  var summaryLines = $("#summary-lines");
  var update = function (rerender) {
    if (rerender) renderEvents();
    var ls = lines(), t = total(ls);

    $$("[data-event-price]").forEach(function (p) {
      var ev = state.events.filter(function (x) { return String(x.id) === p.getAttribute("data-event-price"); })[0];
      if (!ev) return;
      var price = eventPrice(ev);
      p.textContent = price ? money(price) + " for this event" : "Choose photography or film for this event";
      p.classList.toggle("is-empty", !price);
    });
    P.sections.forEach(function (sec) {
      if (!sec.requires) return;
      var locked = !has(sec.requires);
      var s = $("#b-" + sec.id);
      $(".b-locked", s).hidden = !locked;
      $$("select", s).forEach(function (x) { x.disabled = locked; });
      s.classList.toggle("is-locked", locked);
    });

    summaryLines.textContent = "";
    ls.forEach(function (l) {
      var li = el("li", { "class": "b-line" });
      var txt = el("div");
      txt.appendChild(el("span", { "class": "b-line__label" }, l.label));
      txt.appendChild(el("span", { "class": "b-line__detail" }, l.detail));
      li.appendChild(txt);
      li.appendChild(el("span", { "class": "b-line__price" }, l.price ? money(l.price) : (l.priceNote || "—")));
      summaryLines.appendChild(li);
    });
    $("#summary-total").textContent = money(t);
    $("#bar-total").textContent = money(t);
    $("#summary-note").textContent = P.estimateNote;
    save();
  };

  $("#reset-package").addEventListener("click", function () {
    state = freshState();
    sectionsHost.querySelectorAll("select").forEach(function (s) { s.value = "0"; });
    update(true);
    window.scrollTo({ top: $("#b-events").offsetTop - 90, behavior: "smooth" });
  });

  /* ---------- Finalize ---------- */
  var form = $("#package-form");
  var err = $("#package-error");
  var dateInput = $("#p-date"), flex = $("#p-date-flex");
  dateInput.min = new Date().toISOString().slice(0, 10);
  flex.addEventListener("change", function () { dateInput.disabled = flex.checked; });
  $$("input, select, textarea", form).forEach(function (f) {
    f.addEventListener("input", function () { f.classList.remove("is-invalid"); });
  });

  var params = new URLSearchParams(location.search);
  ["utm_source", "utm_medium", "utm_campaign", "gclid", "fbclid"].forEach(function (k) {
    if (params.get(k)) { var i = el("input", { type: "hidden", name: k }); i.value = params.get(k); form.appendChild(i); }
  });

  var reference = function () {
    var d = new Date(), pad = function (n) { return String(n).padStart(2, "0"); };
    var chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789", r = "";
    for (var i = 0; i < 4; i++) r += chars[Math.floor(Math.random() * chars.length)];
    return "LS-" + String(d.getFullYear()).slice(2) + pad(d.getMonth() + 1) + pad(d.getDate()) + "-" + r;
  };

  var asText = function (ref, fd, ls, t) {
    var out = ["Laaj Studios package " + ref, ""];
    var group = "";
    ls.forEach(function (l) {
      if (l.group !== group) { group = l.group; out.push(group.toUpperCase()); }
      out.push("- " + l.label + ": " + l.detail + " — " + (l.price ? money(l.price) : (l.priceNote || "")));
    });
    out.push("", "Estimated investment: " + money(t), "", "Client: " + fd.get("name") + (fd.get("partner") ? " & " + fd.get("partner") : ""));
    out.push("Email: " + fd.get("email"), "Phone: " + fd.get("phone") + " (prefers " + fd.get("contact_pref") + ")");
    out.push("Wedding date: " + (fd.get("date_flexible") ? "Not set yet" : (fd.get("wedding_date") || "Not given")));
    if (fd.get("venue")) out.push("Venue: " + fd.get("venue"));
    if (fd.get("guests")) out.push("Guests: " + fd.get("guests"));
    if (fd.get("notes")) out.push("Notes: " + fd.get("notes"));
    return out.join("\n");
  };

  var showCopy = function (ref, fd, ls, t, sent) {
    $("#copy-ref").textContent = ref;
    $("#copy-date").textContent = new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
    var dl = $("#copy-client"); dl.textContent = "";
    [["Couple", fd.get("name") + (fd.get("partner") ? " & " + fd.get("partner") : "")],
     ["Wedding date", fd.get("date_flexible") ? "Not set yet" : (fd.get("wedding_date") ? new Date(fd.get("wedding_date") + "T12:00").toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" }) : "Not given")],
     ["Venue", fd.get("venue") || "—"],
     ["Contact", fd.get("email") + " · " + fd.get("phone")]].forEach(function (r) {
      dl.appendChild(el("dt", null, r[0])); dl.appendChild(el("dd", null, r[1]));
    });
    var tb = $("#copy-lines"); tb.textContent = "";
    var group = "";
    ls.forEach(function (l) {
      if (l.group !== group) { group = l.group; var gr = el("tr", { "class": "b-copy__group" }); gr.appendChild(el("th", { colspan: "2", scope: "colgroup" }, group)); tb.appendChild(gr); }
      var tr = el("tr");
      var td = el("td"); td.appendChild(el("strong", null, l.label)); td.appendChild(el("span", null, l.detail));
      tr.appendChild(td);
      tr.appendChild(el("td", null, l.price ? money(l.price) : (l.priceNote || "—")));
      tb.appendChild(tr);
    });
    $("#copy-total").textContent = money(t);
    $("#copy-note").textContent = P.estimateNote;
    $("#done-status").textContent = sent
      ? "Thank you. Your package is with us and we'll reply within 24 hours. Here is your copy to keep."
      : "Your email app should have opened with your package written out. Please press send. Here is your copy to keep.";
    var wa = $("#done-whatsapp");
    if (C.whatsapp) wa.href = "https://wa.me/" + C.whatsapp + "?text=" + encodeURIComponent("Hello Laaj Studios! I just built my package on your website. Reference " + ref + ", estimate " + money(t) + ".");
    else wa.hidden = true;
    $("#copy-summary").onclick = function () {
      var text = asText(ref, fd, ls, t), b = this;
      var done = function () { b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy summary"; }, 2000); };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () { window.prompt("Copy your summary:", text); });
    };
    if (sent && window.gtag) window.gtag("event", "generate_lead", { event_category: "package_builder", value: t });
    if (sent && window.fbq) window.fbq("track", "Lead", { value: t, currency: P.currency || "USD" });
    document.body.classList.add("is-done");
    $("#done").hidden = false;
    window.scrollTo(0, 0);
    $("#done").focus({ preventScroll: true });
  };

  $("#print-copy").addEventListener("click", function () { window.print(); });
  $("#edit-package").addEventListener("click", function () {
    $("#done").hidden = true;
    document.body.classList.remove("is-done");
    $("#details").scrollIntoView();
  });

  var fail = function (msg) { err.textContent = msg; err.hidden = false; };

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    err.hidden = true;
    var bad = null;
    $$("[required]", form).forEach(function (f) {
      var ok = f.checkValidity();
      f.classList.toggle("is-invalid", !ok);
      if (!ok && !bad) bad = f;
    });
    if (bad) { bad.focus(); return fail("Please add your name, email and phone so we can send your proposal."); }
    if (!state.events.some(function (ev) { return eventPrice(ev) > 0; })) {
      $("#b-events").scrollIntoView();
      return fail("Choose photography or film for at least one event.");
    }

    var fd = new FormData(form);
    if (fd.get("_gotcha")) return;
    var ls = lines(), t = total(ls), ref = reference();
    var summary = asText(ref, fd, ls, t);
    fd.append("_subject", "Package " + ref + " · " + fd.get("name") + " · " + money(t));
    fd.append("reference", ref);
    fd.append("estimated_total", money(t));
    fd.append("package", summary);
    fd.append("package_data", JSON.stringify({ reference: ref, total: t, events: state.events, choices: state.choices, lines: ls }));

    var btn = $(".b-submit", form);
    if (C.formEndpoint) {
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(C.formEndpoint, { method: "POST", body: fd, headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error(r.status); showCopy(ref, fd, ls, t, true); })
        .catch(function () {
          fail("We couldn't send your package just now. Please try again, or message us on WhatsApp.");
        })
        .then(function () { btn.disabled = false; btn.textContent = "Finalize my package"; });
    } else {
      location.href = "mailto:" + (C.email || "") + "?subject=" + encodeURIComponent("Package " + ref) + "&body=" + encodeURIComponent(summary);
      showCopy(ref, fd, ls, t, false);
    }
  });

  update(true);
})();
