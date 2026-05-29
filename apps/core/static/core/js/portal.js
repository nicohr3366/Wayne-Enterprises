document.addEventListener('DOMContentLoaded', function () {

  document.querySelectorAll('.division-card').forEach(function (card, i) {
    card.style.opacity    = '0';
    card.style.transform  = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease, border-color 0.3s ease, background 0.3s ease';

    setTimeout(function () {
      card.style.opacity   = card.classList.contains('coming-soon') ? '0.45' : '1';
      card.style.transform = 'translateY(0)';
    }, 1200 + i * 80);
  });

  var grid = document.getElementById('grid');
  if (grid) {
    var activeApps = (grid.dataset.active || '').split(',').map(function (a) {
      return a.trim();
    });

    activeApps.forEach(function (appName) {
      if (!appName) return;
      var card = document.querySelector('[data-app="' + appName + '"]');
      if (!card) return;

      card.classList.remove('coming-soon');

      var url = card.dataset.url;
      if (url) card.setAttribute('href', url);

      var badge = card.querySelector('.card-badge');
      if (badge) {
        badge.textContent = 'Activo';
        badge.className   = 'card-badge badge-live';
      }
    });
  }

  var clockEl = document.getElementById('gotham-clock');
  if (clockEl) {
    function updateClock() {
      var now    = new Date();
      var offset = -5;
      var utc    = now.getTime() + now.getTimezoneOffset() * 60000;
      var gotham = new Date(utc + 3600000 * offset);
      var h      = String(gotham.getHours()).padStart(2, '0');
      var m      = String(gotham.getMinutes()).padStart(2, '0');
      var s      = String(gotham.getSeconds()).padStart(2, '0');
      clockEl.textContent = h + ':' + m + ':' + s + ' GTC';
    }
    updateClock();
    setInterval(updateClock, 1000);
  }

});