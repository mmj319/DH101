/**
 * Light / Dark Mode Toggle System
 * Handles theme persistence in localStorage, system preference detection,
 * and synchronized toggle buttons across the site.
 */
(function () {
  'use strict';

  var THEME_KEY = 'maddie_space_theme';

  function getPreferredTheme() {
    try {
      var saved = localStorage.getItem(THEME_KEY);
      if (saved === 'dark' || saved === 'light') {
        return saved;
      }
    } catch (e) {}

    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }

  function updateToggleButtons(theme) {
    var isDark = theme === 'dark';
    var buttons = document.querySelectorAll('.theme-toggle');
    buttons.forEach(function (btn) {
      btn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
      btn.setAttribute('title', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
      btn.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');

      var icon = btn.querySelector('.theme-toggle-icon');
      var text = btn.querySelector('.theme-toggle-text');
      if (icon) icon.textContent = isDark ? '☀️' : '🌙';
      if (text) text.textContent = isDark ? 'Light' : 'Dark';
    });
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    updateToggleButtons(theme);
  }

  window.toggleTheme = function () {
    var current = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
    var next = current === 'dark' ? 'light' : 'dark';
    try {
      localStorage.setItem(THEME_KEY, next);
    } catch (e) {}
    applyTheme(next);
  };

  // Listen to system OS theme changes if user has not set an explicit override
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
      var hasExplicitOverride = false;
      try {
        hasExplicitOverride = !!localStorage.getItem(THEME_KEY);
      } catch (err) {}

      if (!hasExplicitOverride) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }

  // Setup buttons on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    var current = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
    updateToggleButtons(current);

    document.querySelectorAll('.theme-toggle').forEach(function (btn) {
      btn.removeEventListener('click', window.toggleTheme);
      btn.addEventListener('click', window.toggleTheme);
    });
  }
})();

