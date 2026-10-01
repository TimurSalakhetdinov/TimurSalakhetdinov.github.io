(function () {
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  if (!navToggle || !navLinks) return;
  const toggleLabel = navToggle.querySelector('.nav-toggle-label');
  const closeText = navToggle.getAttribute('data-close-text') || 'Close';
  const menuText = navToggle.getAttribute('data-menu-text') || 'Menu';

  function setMenuState(open) {
    navToggle.setAttribute('aria-expanded', String(open));
    navLinks.classList.toggle('is-open', open);
    if (toggleLabel) toggleLabel.textContent = open ? closeText : menuText;
  }

  navToggle.addEventListener('click', () => {
    setMenuState(navToggle.getAttribute('aria-expanded') !== 'true');
  });

  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => setMenuState(false));
  });

  document.addEventListener('click', (e) => {
    if (!navToggle.contains(e.target) && !navLinks.contains(e.target) && navToggle.getAttribute('aria-expanded') === 'true') {
      setMenuState(false);
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navToggle.getAttribute('aria-expanded') === 'true') {
      setMenuState(false);
      navToggle.focus();
    }
  });
})();
