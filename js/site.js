/* rushitnshah.com — site.js */

const root = document.documentElement;
const btn  = document.getElementById('theme-toggle');
const icon = document.getElementById('toggle-icon');

function applyTheme(theme) {
  root.setAttribute('data-theme', theme);
  icon.className = theme === 'dark' ? 'fa fa-sun-o' : 'fa fa-moon-o';
  localStorage.setItem('theme', theme);
}

// Restore saved preference, otherwise respect OS setting
const saved = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
applyTheme(saved || (prefersDark ? 'dark' : 'light'));

btn.addEventListener('click', () => {
  applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const t = document.querySelector(a.getAttribute('href'));
    if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); }
  });
});

// Nav shadow on scroll
const nav = document.querySelector('nav');
window.addEventListener('scroll', () => {
  nav.style.boxShadow = window.scrollY > 10 ? 'var(--nav-shadow)' : 'none';
}, { passive: true });
