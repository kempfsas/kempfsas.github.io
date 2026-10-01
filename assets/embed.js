/* Zwei-Klick-Einbettung fuer TikTok und Instagram.

   Warum nicht direkt einbetten: beide Plattformen setzen beim Laden Cookies und
   uebertragen die IP des Besuchers an ByteDance bzw. Meta - ungefragt. Die Seite
   kommt sonst ohne einen einzigen externen Request aus. Darum wird der iframe
   erst erzeugt, wenn jemand die Vorschaukarte bewusst anklickt. */
(function () {
  var karten = document.querySelectorAll('.embed-card');
  if (!karten.length) return;

  function laden(card) {
    var typ = card.dataset.embed, id = card.dataset.id;
    var src = typ === 'tiktok'
      ? 'https://www.tiktok.com/embed/v2/' + id
      : 'https://www.instagram.com/reel/' + id + '/embed';
    var f = document.createElement('iframe');
    f.src = src;
    f.title = card.dataset.title || 'Eingebetteter Beitrag';
    f.loading = 'lazy';
    f.allow = 'encrypted-media; picture-in-picture';
    f.referrerPolicy = 'no-referrer-when-downgrade';
    f.setAttribute('allowfullscreen', '');
    card.textContent = '';
    card.classList.add('loaded');
    card.appendChild(f);
  }

  karten.forEach(function (card) {
    var btn = card.querySelector('.embed-load');
    if (!btn) return;
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      laden(card);
    });
  });
})();
