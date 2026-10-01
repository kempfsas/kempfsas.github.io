/* Videogalerie.

   Zwei Dinge kosten hier Leistung, und beide werden bewusst begrenzt:
   - Laden: preload="none" im Markup, geladen wird erst kurz vor dem Abspielen.
   - Dekodieren: jedes laufende Video belegt einen Decoder. Darum laeuft immer
     nur der sichtbarste Clip, nicht alle sichtbaren gleichzeitig. */
(function () {
  var vids = [].slice.call(document.querySelectorAll('.video-grid video'));
  if (!vids.length) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Klick: Ton an, von vorn, Steuerung einblenden. Gilt auch ohne Autoplay.
  vids.forEach(function (v) {
    v.addEventListener('click', function () {
      if (v.muted) { v.muted = false; v.currentTime = 0; v.controls = true; v.play().catch(function () {}); }
    });
  });

  if (reduce || !('IntersectionObserver' in window)) return; // Poster genuegt

  var ratio = new WeakMap();
  var aktiv = null;
  var geplant = false;

  function waehlen() {
    geplant = false;
    var best = null, bestR = 0;
    vids.forEach(function (v) {
      var r = ratio.get(v) || 0;
      if (r > bestR) { bestR = r; best = v; }
    });
    if (best === aktiv) return;
    // Laufenden Clip anhalten, sofern der Betrachter ihn nicht per Klick uebernommen hat
    if (aktiv && aktiv.muted) aktiv.pause();
    aktiv = best;
    if (!aktiv) return;
    if (aktiv.preload === 'none') aktiv.preload = 'auto';
    aktiv.play().catch(function () {});   // Autoplay kann blockiert sein
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { ratio.set(e.target, e.isIntersecting ? e.intersectionRatio : 0); });
    if (!geplant) { geplant = true; requestAnimationFrame(waehlen); }
  }, { threshold: [0, 0.25, 0.5, 0.75, 1] });

  vids.forEach(function (v) { io.observe(v); });
})();
