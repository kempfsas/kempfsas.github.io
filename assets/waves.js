/* Flowing lines – procedurally drawn, gently animated, reacting to the pointer.
   Usage: <canvas class="waves" data-lines="56" data-from="0.4"></canvas> inside a position:relative section. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canvases = document.querySelectorAll('canvas.waves');
  if (!canvases.length) return;

  function setup(cv) {
    var ctx = cv.getContext('2d');
    var N = +cv.dataset.lines || 56;      // number of lines
    var FROM = +cv.dataset.from || 0.4;    // lines fade in from this fraction of the width
    var AMP = +cv.dataset.amp || 0.22;     // amplitude relative to height
    var OP = +cv.dataset.opacity || 1;     // global opacity multiplier
    // Funnel: wie schmal das Baendel am rechten Ende zusammenlaeuft.
    // 1 = kein Funnel (parallele Linien), 0.15 = enger Hals.
    var NECK = cv.dataset.funnel !== undefined ? +cv.dataset.funnel : 1;
    var state = { w: 0, h: 0, dpr: 1, t: Math.random() * 100, mx: -1, my: -1, tx: -1, ty: -1, lines: [] };

    function resize() {
      var fixed = cv.hasAttribute('data-fixed');
      var r = fixed ? {width: window.innerWidth, height: window.innerHeight} : cv.parentElement.getBoundingClientRect();
      // Der vollflaechige Hintergrund wird bewusst in CSS-Pixeln gezeichnet:
      // in Geraetepixeln waere die Fuellflaeche fast doppelt so gross, und die
      // weichen Linien gewinnen dadurch optisch praktisch nichts.
      state.dpr = fixed ? 1 : Math.min(window.devicePixelRatio || 1, 2);
      state.w = r.width; state.h = r.height;
      cv.width = Math.round(state.w * state.dpr); cv.height = Math.round(state.h * state.dpr);
      cv.style.width = state.w + 'px'; cv.style.height = state.h + 'px';
      ctx.setTransform(state.dpr, 0, 0, state.dpr, 0, 0);
      state.lines = [];
      for (var i = 0; i < N; i++) {
        var u = i / (N - 1);
        var fam = i % 2;                        // two interleaved families that cross each other
        state.lines.push({
          y: 0.06 + u * 0.88,                  // base position (fraction of height)
          k: 1.9 + 0.5 * Math.sin(u * 2.4),     // wave frequency – close neighbours => ribbon feel
          ph: u * 1.6 + fam * 2.6,              // small phase drift between neighbours
          sp: 0.18 + 0.12 * u,                  // speed
          a: (0.7 + 0.3 * Math.sin(u * 3.1)) * (fam ? -1 : 1) // amplitude, mirrored per family
        });
      }
    }

    function color(u) { // cyan -> violet -> pink
      var c1 = [125, 224, 238], c2 = [176, 139, 238], c3 = [240, 155, 217];
      var a = u < 0.5 ? c1 : c2, b = u < 0.5 ? c2 : c3, f = u < 0.5 ? u * 2 : (u - 0.5) * 2;
      return 'rgb(' + Math.round(a[0] + (b[0] - a[0]) * f) + ',' + Math.round(a[1] + (b[1] - a[1]) * f) + ',' + Math.round(a[2] + (b[2] - a[2]) * f) + ')';
    }

    function draw() {
      var w = state.w, h = state.h, t = state.t;
      ctx.clearRect(0, 0, w, h);
      // pointer easing
      if (state.tx >= 0) { state.mx += (state.tx - state.mx) * 0.06; state.my += (state.ty - state.my) * 0.06; }
      var steps = 44, x0 = w * FROM, span = w - x0;
      var funnel = NECK < 1;
      var px = state.mx >= 0 ? (state.mx / w - 0.5) : 0, py = state.my >= 0 ? (state.my / h - 0.5) : 0;
      var grad = ctx.createLinearGradient(x0, 0, w, 0);
      grad.addColorStop(0, color(0).replace('rgb(', 'rgba(').replace(')', ',0)'));
      grad.addColorStop(0.28, color(0.15)); grad.addColorStop(0.6, color(0.55)); grad.addColorStop(1, color(1));
      ctx.lineWidth = 1; ctx.strokeStyle = grad;
      for (var i = 0; i < state.lines.length; i++) {
        var L = state.lines[i];
        ctx.beginPath();
        for (var s = 0; s <= steps; s++) {
          var p = s / steps;                 // 0..1 along the visible span
          var x = x0 + p * span;
          // main wave + slow secondary swell
          // Zusammenlaufen zur Mitte: taper geht von 1 (links, volle Breite)
          // auf NECK (rechts, Hals). Leicht kubisch, damit die Verjuengung
          // vorne sanft beginnt und hinten deutlich wird - ein linearer
          // Verlauf sieht aus wie ein Dreieck, nicht wie ein Trichter.
          var taper = funnel ? NECK + (1 - NECK) * Math.pow(1 - p, 1.7) : 1;
          var base = funnel ? (0.5 + (L.y - 0.5) * taper) * h : L.y * h;
          var y = base
            + Math.sin(p * L.k * 3.1 + L.ph + t * L.sp + px * 0.5) * AMP * h * L.a * Math.sin(p * 3.14) * taper
            + Math.sin(p * 2.2 + t * 0.12 + L.ph * 0.3) * 0.05 * h * taper;
          // pointer influence: the whole field drifts very slightly with the cursor (no local bulge)
          y += py * 10 * (0.5 + L.y);
          if (s === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        // fade in from the left, vary opacity per line
        ctx.globalAlpha = (0.22 + 0.3 * Math.abs(Math.sin(i * 0.21 + t * 0.25))) * OP;
        ctx.stroke();
      }
      ctx.globalAlpha = 1;
    }

    var prev = 0;
    function frame(ts) {
      requestAnimationFrame(frame);
      if (document.hidden) return;              // im Hintergrund gar nicht rechnen
      if (ts - prev < 32) return;               // ~30 fps statt 60
      prev = ts;
      state.t += 0.016;                         // halbe Bildrate, doppelter Schritt
      draw();
    }

    var rt;
    window.addEventListener('resize', function () {
      clearTimeout(rt); rt = setTimeout(function () { resize(); draw(); }, 150);
    });
    var host = cv.hasAttribute('data-fixed') ? window : cv.parentElement;
    host.addEventListener('pointermove', function (e) {
      var r = cv.getBoundingClientRect(); state.tx = e.clientX - r.left; state.ty = e.clientY - r.top;
    });
    host.addEventListener(cv.hasAttribute('data-fixed') ? 'pointerout' : 'pointerleave', function (e) {
      if (e.relatedTarget === null || !cv.hasAttribute('data-fixed')) { state.tx = -1; state.ty = -1; state.mx = -1; state.my = -1; }
    });
    resize(); draw();
    if (!reduce) requestAnimationFrame(frame);
  }
  for (var i = 0; i < canvases.length; i++) setup(canvases[i]);
})();
