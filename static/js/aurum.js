/* =====================================================
   AURUM FINE DINING — Main JavaScript
   ===================================================== */

'use strict';

/* ── LOADER ──────────────────────────────────────────── */
window.addEventListener('load', () => {
  setTimeout(() => document.getElementById('loader')?.classList.add('gone'), 1800);
});

/* ── NAVBAR ──────────────────────────────────────────── */
(function initNav() {
  const nav = document.getElementById('nav');
  const fc  = document.getElementById('float-cta');
  if (!nav) return;

  const onScroll = () => {
    nav.classList.toggle('stuck', scrollY > 60);
    fc?.classList.toggle('on', scrollY > 500);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

/* ── MOBILE DRAWER ───────────────────────────────────── */
const ham     = document.getElementById('ham');
const drawer  = document.getElementById('drawer');
const overlay = document.getElementById('overlay');

function openDrawer() {
  ham?.classList.add('open');
  drawer?.classList.add('open');
  overlay?.classList.add('show');
  document.body.style.overflow = 'hidden';
}
function closeDrawer() {
  ham?.classList.remove('open');
  drawer?.classList.remove('open');
  overlay?.classList.remove('show');
  document.body.style.overflow = '';
}
ham?.addEventListener('click', () =>
  drawer?.classList.contains('open') ? closeDrawer() : openDrawer()
);
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDrawer(); });

/* ── HERO SLIDER ─────────────────────────────────────── */
(function initHero() {
  const slides = [...document.querySelectorAll('.hs')];
  const dots   = [...document.querySelectorAll('.hd')];
  if (!slides.length) return;

  let cur = 0, timer;

  function go(n) {
    slides[cur].classList.remove('on');
    dots[cur]?.classList.remove('on');
    cur = (n + slides.length) % slides.length;
    slides[cur].classList.add('on');
    dots[cur]?.classList.add('on');
  }

  function start() { timer = setInterval(() => go(cur + 1), 7000); }

  dots.forEach(d => d.addEventListener('click', () => {
    clearInterval(timer);
    go(+d.dataset.s);
    start();
  }));

  start();
})();

/* ── SCROLL REVEAL ───────────────────────────────────── */
(function initReveal() {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('on');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -50px 0px' });

  window._rv_observer = obs;
  document.querySelectorAll('.rv').forEach(el => obs.observe(el));
})();

/* ── LIGHTBOX ────────────────────────────────────────── */
const lb    = document.getElementById('lb');
const lbImg = document.getElementById('lb-img');

function openLB(el) {
  const src = el.querySelector('img')?.src?.replace(/w=\d+/, 'w=1400') || '';
  if (!src || !lb || !lbImg) return;
  lbImg.src = src;
  lb.classList.add('on');
  document.body.style.overflow = 'hidden';
}
function closeLB() {
  lb?.classList.remove('on');
  document.body.style.overflow = '';
}
lb?.addEventListener('click', e => { if (e.target === lb) closeLB(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLB(); });

/* ── TOAST ───────────────────────────────────────────── */
let toastTimer;
function showToast(msg, duration = 4500) {
  const t = document.getElementById('toast');
  if (!t) return;
  clearTimeout(toastTimer);
  t.textContent = msg;
  t.classList.add('on');
  toastTimer = setTimeout(() => t.classList.remove('on'), duration);
}

/* ── NEWSLETTER (AJAX) ───────────────────────────────── */
function handleNL() {
  const inp = document.getElementById('nl-inp');
  if (!inp) return;
  const email = inp.value.trim();
  if (!email || !email.includes('@')) {
    showToast('Please enter a valid email address.');
    inp.focus();
    return;
  }

  const btn = inp.nextElementSibling;
  const orig = btn.textContent;
  btn.textContent = '…'; btn.disabled = true;

  const body = JSON.stringify({ email });
  const url  = document.querySelector('meta[name="nl-url"]')?.content || '/api/newsletter/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
      'X-Requested-With': 'XMLHttpRequest',
    },
    body,
  })
    .then(r => r.json())
    .then(d => {
      showToast((d.success ? '✓ ' : '⚠ ') + d.message);
      if (d.success) inp.value = '';
    })
    .catch(() => showToast('Something went wrong. Please try again.'))
    .finally(() => { btn.textContent = orig; btn.disabled = false; });
}

/* ── DJANGO MESSAGES → TOAST ─────────────────────────── */
document.querySelectorAll('.django-msg').forEach(el => {
  setTimeout(() => showToast(el.dataset.msg), 400);
});

/* ── RESERVATION DATE MIN ────────────────────────────── */
(function setMinDate() {
  document.querySelectorAll('input[type="date"]').forEach(inp => {
    const d = new Date();
    d.setDate(d.getDate() + 1);
    inp.min = d.toISOString().split('T')[0];
  });
})();

/* ── SMOOTH SCROLL FOR ANCHOR LINKS ─────────────────── */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

/* ── GALLERY FILTER (client-side) ────────────────────── */
(function initGalleryFilter() {
  const tabs = document.querySelectorAll('.menu-tabs .mt[href]');
  tabs.forEach(tab => {
    tab.addEventListener('click', e => {
      // Allow default navigation — server renders filtered results
    });
  });
})();

/* ── MENU SEARCH CLEAR BUTTON ────────────────────────── */
const searchInp = document.getElementById('menu-search');
const clearBtn  = document.getElementById('search-clear');
if (searchInp && clearBtn) {
  searchInp.addEventListener('input', () => {
    clearBtn.style.display = searchInp.value ? 'block' : 'none';
  });
}

/* ── PARALLAX HERO ───────────────────────────────────── */
(function initParallax() {
  const hero = document.querySelector('.page-hero-img');
  if (!hero) return;
  window.addEventListener('scroll', () => {
    const y = scrollY * 0.35;
    hero.style.transform = `translateY(${y}px)`;
  }, { passive: true });
})();

/* ── CURSOR GLOW (subtle) ────────────────────────────── */
(function initCursor() {
  if (window.matchMedia('(pointer: coarse)').matches) return; // skip mobile
  const glow = document.createElement('div');
  glow.style.cssText = `
    position:fixed;width:300px;height:300px;border-radius:50%;
    background:radial-gradient(circle,rgba(201,169,110,.06) 0%,transparent 70%);
    pointer-events:none;z-index:0;transform:translate(-50%,-50%);
    transition:opacity .4s;
  `;
  document.body.appendChild(glow);
  let mx = 0, my = 0, gx = 0, gy = 0;
  document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; }, { passive: true });
  (function animate() {
    gx += (mx - gx) * 0.08;
    gy += (my - gy) * 0.08;
    glow.style.left = gx + 'px';
    glow.style.top  = gy + 'px';
    requestAnimationFrame(animate);
  })();
  document.addEventListener('mouseleave', () => glow.style.opacity = '0');
  document.addEventListener('mouseenter', () => glow.style.opacity = '1');
})();

/* ── UTILITY: GET CSRF COOKIE ────────────────────────── */
function getCookie(name) {
  const v = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  return v ? v.pop() : '';
}

/* ── INTERSECTION-TRIGGERED COUNTER ANIMATION ────────── */
(function initCounters() {
  const counters = document.querySelectorAll('.ast-n, .cs-num');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el  = e.target;
      const raw = el.textContent.replace(/[^0-9]/g, '');
      const end = parseInt(raw, 10);
      if (!end) return;
      const suffix = el.textContent.replace(/[0-9]/g, '');
      let cur = 0;
      const step = Math.ceil(end / 50);
      const t = setInterval(() => {
        cur = Math.min(cur + step, end);
        el.textContent = cur + suffix;
        if (cur >= end) clearInterval(t);
      }, 24);
      obs.unobserve(el);
    });
  }, { threshold: 0.5 });
  counters.forEach(c => obs.observe(c));
})();
