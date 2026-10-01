/* Bewegung beim Scrollen: Zahlen zaehlen hoch, Abschnitte blenden ein,
   Header wird kompakter.

   Grundsatz: der Inhalt ist ohne JavaScript vollstaendig sichtbar. Erst dieses
   Script setzt .js-motion auf <html>, und nur darunter greifen die
   Versteck-Regeln im CSS. Scheitert das Script oder ist prefers-reduced-motion
   gesetzt, bleibt die Seite eine ganz normale, vollstaendige Seite. */
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var io = 'IntersectionObserver' in window;
  if (reduce || !io) return;
  root.classList.add('js-motion');

  /* --- Abschnitte einblenden --- */
  var revealer = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      revealer.unobserve(e.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { revealer.observe(el); });

  /* --- Zahlen hochzaehlen ---
     Die Werte stehen als fertiger Text da ("15'574", "CHF 1.35", "13.91 %",
     "6+ yrs"). Wir loesen die erste Zahl heraus, behalten Vor- und Nachtext
     sowie Tausendertrenner und Nachkommastellen bei. Wo keine Zahl steht
     ("DE · CH"), passiert nichts. */
  function parse(text) {
    var m = /(\d[\d'’.,]*)/.exec(text);
    if (!m) return null;
    var raw = m[1];
    var sep = /['’]/.test(raw) ? raw.match(/['’]/)[0] : '';
    var norm = raw.replace(/['’]/g, '');
    var dot = norm.lastIndexOf('.');
    var decimals = dot > -1 ? norm.length - dot - 1 : 0;
    var value = parseFloat(norm.replace(/,/g, ''));
    if (!isFinite(value)) return null;
    return {
      value: value, decimals: decimals, sep: sep,
      before: text.slice(0, m.index), after: text.slice(m.index + raw.length)
    };
  }

  function group(s, sep) {
    if (!sep) return s;
    var parts = s.split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, sep);
    return parts.join('.');
  }

  function animate(el, p) {
    var t0 = null, dur = 1100;
    function step(ts) {
      if (t0 === null) t0 = ts;
      var k = Math.min((ts - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - k, 3);          // schnell an, weich aus
      var v = (p.value * eased).toFixed(p.decimals);
      el.textContent = p.before + group(v, p.sep) + p.after;
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  var counter = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      counter.unobserve(e.target);
      var p = parse(e.target.textContent.trim());
      if (!p) return;
      // Platz reservieren, damit das Layout beim Zaehlen nicht springt
      e.target.style.minWidth = e.target.getBoundingClientRect().width + 'px';
      e.target.style.display = 'inline-block';
      animate(e.target, p);
    });
  }, { threshold: 0.6 });
  document.querySelectorAll('.stats .n, .featured .n, .results .n').forEach(function (el) {
    counter.observe(el);
  });

  /* --- Header kompakter beim Scrollen ---
     Die Hoehe haengt an --header-h; das mobile Menu haengt ebenfalls daran
     und bleibt dadurch buendig. */
  var header = document.querySelector('.site-header');
  if (header) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        header.classList.toggle('scrolled', window.scrollY > 40);
        ticking = false;
      });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
})();
