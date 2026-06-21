(() => {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // --- THEME TOGGLE ----------------------------------------------
  const themeToggle = document.querySelector('.theme-toggle');
  const applyTheme = (t) => {
    document.documentElement.setAttribute('data-theme', t);
    themeToggle?.setAttribute('aria-label', t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    themeToggle?.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false');
  };
  applyTheme(document.documentElement.getAttribute('data-theme') || 'light');
  themeToggle?.addEventListener('click', () => {
    const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem('cc-theme', next); } catch (e) {}
  });

  // --- NAV --------------------------------------------------------
  const nav = document.querySelector('.nav');
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelectorAll('.nav-links a');

  if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }

  navLinks.forEach((a) => {
    a.addEventListener('click', () => {
      if (nav?.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        navToggle?.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav?.classList.contains('is-open')) {
      nav.classList.remove('is-open');
      navToggle?.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
  });

  // active link
  const path = window.location.pathname.split('/').pop() || 'index.html';
  navLinks.forEach((a) => {
    const href = a.getAttribute('href') || '';
    const last = href.split('/').pop();
    if (last === path) a.classList.add('is-active');
  });

  // scrolled state
  const onScroll = () => {
    if (!nav) return;
    nav.classList.toggle('is-scrolled', window.scrollY > 24);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // --- HERO LETTER CASCADE ---------------------------------------
  const heroTitle = document.querySelector('.hero-title');
  if (heroTitle && !prefersReduced) {
    const words = heroTitle.querySelectorAll('.word');
    words.forEach((w, i) => { w.style.transitionDelay = (i * 90) + 'ms'; });
    requestAnimationFrame(() => {
      requestAnimationFrame(() => heroTitle.classList.add('is-revealed'));
    });
  } else if (heroTitle) {
    heroTitle.classList.add('is-revealed');
  }

  // --- REVEAL ON SCROLL ------------------------------------------
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length && 'IntersectionObserver' in window && !prefersReduced) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -10% 0px' });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-visible'));
  }

  // --- CONTACT FORM ----------------------------------------------
  const form = document.querySelector('[data-form="contact"]');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = form.querySelector('[name="name"]')?.value.trim();
      const email = form.querySelector('[name="email"]')?.value.trim();
      const message = form.querySelector('[name="message"]')?.value.trim();
      if (!name || !email || !message) return;
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return;
      const success = form.querySelector('.form-success');
      form.reset();
      if (success) {
        success.classList.add('show');
        setTimeout(() => success.classList.remove('show'), 6000);
      }
    });
  }

  // --- PODCAST EMAIL CAPTURE -------------------------------------
  const subForm = document.querySelector('[data-form="subscribe"]');
  if (subForm) {
    subForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = subForm.querySelector('[name="email"]')?.value.trim();
      if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return;
      const success = subForm.querySelector('.form-success');
      subForm.reset();
      if (success) {
        success.classList.add('show');
        setTimeout(() => success.classList.remove('show'), 6000);
      }
    });
  }

  // --- SMOOTH ANCHOR SCROLL --------------------------------------
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (!id || id.length < 2) return;
      const t = document.querySelector(id);
      if (!t) return;
      e.preventDefault();
      t.scrollIntoView({ behavior: prefersReduced ? 'auto' : 'smooth', block: 'start' });
    });
  });
})();
