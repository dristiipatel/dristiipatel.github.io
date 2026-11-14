// Load this in <head> so the saved theme is applied before the page paints.
(function () {
  var r = document.documentElement;
  try { var s = localStorage.getItem('theme'); if (s) r.setAttribute('data-theme', s); } catch (e) {}
  document.addEventListener('DOMContentLoaded', function () {
    var b = document.getElementById('theme');
    if (!b) return;
    b.addEventListener('click', function () {
      var t = r.getAttribute('data-theme');
      var dark = t ? t === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
      var n = dark ? 'light' : 'dark';
      r.setAttribute('data-theme', n);
      try { localStorage.setItem('theme', n); } catch (e) {}
    });
  });
})();
