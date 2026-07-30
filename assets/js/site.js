/* Morgan Millions — countdown, nav, scroll reveal */
(function () {
  "use strict";

  /* ---------- Countdown: Oct 6, 2027 · 6:00 PM CDT ---------- */
  var TARGET = new Date("2027-10-06T18:00:00-05:00").getTime();

  function pad(n) { return n < 10 ? "0" + n : String(n); }

  function tick() {
    var nodes = document.querySelectorAll("[data-countdown]");
    if (!nodes.length) return;
    var diff = TARGET - Date.now();
    if (diff < 0) diff = 0;
    var s = Math.floor(diff / 1000);
    var parts = {
      days: Math.floor(s / 86400),
      hours: Math.floor((s % 86400) / 3600),
      minutes: Math.floor((s % 3600) / 60),
      seconds: s % 60
    };
    Array.prototype.forEach.call(nodes, function (root) {
      Object.keys(parts).forEach(function (key) {
        var el = root.querySelector('[data-unit="' + key + '"]');
        if (!el) return;
        var val = key === "days" ? String(parts[key]) : pad(parts[key]);
        if (el.textContent !== val) el.textContent = val;
      });
    });
  }
  tick();
  setInterval(tick, 1000);

  /* ---------- Nav: solid on scroll + mobile menu ---------- */
  var nav = document.querySelector(".nav");
  var toggle = document.querySelector(".nav__toggle");
  var links = document.getElementById("nav-links");

  function onScroll() {
    if (!nav) return;
    nav.classList.toggle("nav--solid", window.scrollY > 40);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.getAttribute("data-open") === "true";
      links.setAttribute("data-open", open ? "false" : "true");
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
      document.body.style.overflow = open ? "" : "hidden";
    });
    Array.prototype.forEach.call(links.querySelectorAll("a"), function (a) {
      a.addEventListener("click", function () {
        links.setAttribute("data-open", "false");
        toggle.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      });
    });
  }

  /* ---------- Scroll reveal ---------- */
  var revealables = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealables.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    Array.prototype.forEach.call(revealables, function (el) { io.observe(el); });
  } else {
    Array.prototype.forEach.call(revealables, function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Placeholder CTAs ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-placeholder]"), function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var label = btn.getAttribute("data-placeholder");
      btn.setAttribute("data-original", btn.getAttribute("data-original") || btn.textContent);
      btn.textContent = label;
      setTimeout(function () { btn.textContent = btn.getAttribute("data-original"); }, 2200);
    });
  });

  /* ---------- Stallion editorial modal ---------- */
  var modal = document.getElementById("stallion-modal");
  if (modal) {
    var cards = document.querySelectorAll('[data-modal="stallion"]');
    var closers = modal.querySelectorAll("[data-modal-close]");
    var lastFocused = null;
    var currentSeat = null;

    function setField(sel, value, wrapSel) {
      var el = modal.querySelector(sel);
      var wrap = wrapSel ? modal.querySelector(wrapSel) : el;
      if (!el) return;
      if (value && String(value).trim().length) {
        el.textContent = value;
        if (wrap) wrap.hidden = false;
      } else {
        el.textContent = "";
        if (wrap) wrap.hidden = true;
      }
    }

    function openModal(card, opts) {
      opts = opts || {};
      if (!card) return;
      lastFocused = document.activeElement;
      currentSeat = card.getAttribute("data-seat");

      setField("[data-modal-seat]", currentSeat);
      setField("[data-modal-name]", card.getAttribute("data-name"));
      setField("[data-modal-call]", card.getAttribute("data-call"), "[data-modal-call]");
      setField("[data-modal-tagline]", card.getAttribute("data-tagline"));
      setField("[data-modal-pitch]", card.getAttribute("data-pitch"));
      setField("[data-modal-pedigree]", card.getAttribute("data-pedigree"), "[data-modal-pedigree-wrap]");
      setField("[data-modal-foaled]", card.getAttribute("data-foaled"), "[data-modal-foaled-wrap]");
      setField("[data-modal-standing]", card.getAttribute("data-standing"), "[data-modal-standing-wrap]");

      var portrait = modal.querySelector(".stallion-modal__portrait");
      var fallback = modal.querySelector("[data-modal-fallback]");
      var img = card.getAttribute("data-image");
      var pos = card.getAttribute("data-image-pos") || "center center";
      if (img && img.length) {
        portrait.style.backgroundImage = "url('" + img + "')";
        portrait.style.backgroundPosition = pos;
        portrait.classList.add("has-image");
        if (fallback) { fallback.hidden = true; fallback.setAttribute("hidden", ""); }
      } else {
        portrait.style.backgroundImage = "";
        portrait.classList.remove("has-image");
        if (fallback) { fallback.hidden = false; fallback.removeAttribute("hidden"); }
      }

      modal.hidden = false;
      // Force layout so the opacity transition fires
      void modal.offsetWidth;
      modal.setAttribute("data-open", "true");
      document.body.classList.add("modal-open");

      // Deep-link: push #seat-NN to the URL (skip if already applied on load)
      if (!opts.skipHash && currentSeat) {
        var newHash = "#seat-" + currentSeat;
        if (window.location.hash !== newHash) {
          history.pushState({ seat: currentSeat }, "", newHash);
        }
      }

      // Reset share button label when opening
      var shareLabel = modal.querySelector("[data-modal-share-label]");
      if (shareLabel) shareLabel.textContent = "Share profile";
      var shareBtn = modal.querySelector("[data-modal-share]");
      if (shareBtn) shareBtn.classList.remove("is-copied");

      // Focus the close button for keyboard users
      var close = modal.querySelector(".stallion-modal__close");
      if (close) setTimeout(function () { close.focus(); }, 60);
    }

    /* ---------- Share profile ---------- */
    var shareBtn = modal.querySelector("[data-modal-share]");
    if (shareBtn) {
      shareBtn.addEventListener("click", function () {
        if (!currentSeat) return;
        var name = (modal.querySelector("[data-modal-name]") || {}).textContent || "";
        var url = window.location.origin + window.location.pathname + "#seat-" + currentSeat;
        var shareData = {
          title: name ? name + " · Morgan Millions" : "Morgan Millions Vaulted Sire",
          text: name ? "Vaulted Sire: " + name : "Morgan Millions Vaulted Sire",
          url: url
        };
        var label = modal.querySelector("[data-modal-share-label]");

        function showCopied() {
          if (label) label.textContent = "Link copied";
          shareBtn.classList.add("is-copied");
          setTimeout(function () {
            if (label) label.textContent = "Share profile";
            shareBtn.classList.remove("is-copied");
          }, 1800);
        }

        function fallbackCopy() {
          try {
            var ta = document.createElement("textarea");
            ta.value = url;
            ta.setAttribute("readonly", "");
            ta.style.position = "absolute";
            ta.style.left = "-9999px";
            document.body.appendChild(ta);
            ta.select();
            document.execCommand("copy");
            document.body.removeChild(ta);
            showCopied();
          } catch (err) {
            if (label) label.textContent = url;
          }
        }

        if (navigator.share) {
          navigator.share(shareData).catch(function () {
            // User cancelled or unsupported — fall through to clipboard
            if (navigator.clipboard && navigator.clipboard.writeText) {
              navigator.clipboard.writeText(url).then(showCopied).catch(fallbackCopy);
            } else {
              fallbackCopy();
            }
          });
        } else if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(showCopied).catch(fallbackCopy);
        } else {
          fallbackCopy();
        }
      });
    }

    function closeModal(opts) {
      opts = opts || {};
      modal.setAttribute("data-open", "false");
      document.body.classList.remove("modal-open");
      // Wait for transition before hiding
      setTimeout(function () {
        if (modal.getAttribute("data-open") !== "true") modal.hidden = true;
      }, 380);

      // Clear the deep-link hash if it matches a seat
      if (!opts.skipHash && /^#seat-\d+/.test(window.location.hash)) {
        history.pushState("", document.title, window.location.pathname + window.location.search);
      }

      if (lastFocused && typeof lastFocused.focus === "function") {
        lastFocused.focus();
      }
      currentSeat = null;
    }

    Array.prototype.forEach.call(cards, function (card) {
      card.addEventListener("click", function (e) {
        // Ignore clicks on real links inside the card, if any
        if (e.target.closest("a")) return;
        openModal(card);
      });
      card.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          openModal(card);
        }
      });
    });

    Array.prototype.forEach.call(closers, function (el) {
      el.addEventListener("click", function () { closeModal(); });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modal.getAttribute("data-open") === "true") {
        closeModal();
      }
    });

    // Deep-link: open matching card if URL loads with #seat-NN
    function openFromHash(skipHash) {
      var m = /^#seat-(\d+)/.exec(window.location.hash);
      if (!m) return;
      var seat = m[1];
      var target = document.querySelector('[data-modal="stallion"][data-seat="' + seat + '"]');
      if (target) openModal(target, { skipHash: skipHash });
    }
    openFromHash(true);

    // Handle browser back/forward
    window.addEventListener("popstate", function () {
      var m = /^#seat-(\d+)/.exec(window.location.hash);
      if (m) {
        openFromHash(true);
      } else if (modal.getAttribute("data-open") === "true") {
        closeModal({ skipHash: true });
      }
    });
  }
})();
