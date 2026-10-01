# kempfsas.github.io — Portfolio Saskia Kempf

Statisches Portfolio (HTML/CSS, keine Abhängigkeiten) für
**Saskia Kempf – Digital Marketing Manager, Zürich**.
Die Seiten liegen im Repo-Root, damit GitHub Pages sie direkt unter
`https://kempfsas.github.io/` ausliefert.

## Struktur

```
index.html                  Startseite (Hero, Kennzahlen, Projekte, About, Kontakt)
404.html                    Fehlerseite im Seitenstil
work/                       7 Projektseiten (google-ads, paid-social, tiktok-top-ads,
                            landing-page, linkedin-content, video-content, ux-ui)
blog/                       Insights: index.html + 3 Beiträge
assets/style.css            gesamtes Styling (Farben in :root, --accent ist das Blau)
assets/waves.js             animierte Wellenlinien im Hintergrund
assets/fonts/               Figtree (Open Font License)
assets/img/                 Projektbilder und Fotos
build.py                    optional: erzeugt die HTML-Seiten aus den Texten im Script neu
Dockerfile, docker-compose.yml, docker/nginx.conf
                            lokales Deployment zum Ansehen und Testen
material/                   Bewerbungsunterlagen, nicht im Git (siehe unten)
```

## Lokal ansehen (Docker)

```bash
docker compose up -d --build
```

Danach im Browser: **http://localhost:8081**

Die Seitenordner sind als Volume eingebunden — Änderungen an HTML, CSS, JS oder
Bildern sind direkt nach einem Reload im Browser sichtbar, ohne Rebuild.
Caching ist im lokalen nginx abgeschaltet.

```bash
docker compose logs -f portfolio   # Zugriffe und Fehler mitlesen
docker compose down                # stoppen
```

Ohne Compose, als reines Abbild der späteren Auslieferung (ohne Live-Mount):

```bash
docker build -t kempf-portfolio .
docker run --rm -p 8081:8080 kempf-portfolio
```

Für einen schnellen Blick ohne Docker genügt auch `python3 -m http.server 8081`
im Repo-Root.

## Veröffentlichen

**GitHub Pages** ist eingerichtet: `.github/workflows/pages.yml` baut bei jedem
Push auf `master` die Seite und veröffentlicht sie unter
`https://kempfsas.github.io/`. Der Workflow kopiert nur `index.html`, `404.html`,
`assets/`, `work/` und `blog/`.

Einmalig in GitHub nötig: *Settings → Pages → Build and deployment → Source* auf
**GitHub Actions** stellen. Danach läuft das Deployment automatisch; manuell
anstossen geht über *Actions → Deploy portfolio to GitHub Pages → Run workflow*.
`.nojekyll` liegt bereits im Repo, damit Jekyll die Dateien unverändert ausliefert.

**Eigene Domain:** Domain registrieren, bei GitHub unter *Settings → Pages →
Custom domain* eintragen (legt eine `CNAME`-Datei an) und den DNS-Eintrag beim
Registrar setzen.

Alternativen ohne Git: Netlify Drop (Ordner reinziehen), Cloudflare Pages oder
normaler Webspace per FTP.

## Offene Punkte vor dem Livegang

1. Platzhalter in eckigen Klammern füllen — Suche nach `class="placeholder"`:
   `grep -rn 'class="placeholder"' index.html work blog`.
   Betrifft vor allem Resultate mit Zahlen, Kunde/Branche und die Sprachniveaus.
2. Bildfreigaben der Arbeitgeber und Kunden prüfen.
3. Blog-Beiträge in eigene Worte bringen (aktuell Entwürfe).
4. **`blog/building-a-channel-from-zero.html` ist ein reines Gerüst** — 12 Platzhalter,
   kein eigener Text. Entweder ausfüllen oder vor dem Livegang den Eintrag aus
   `POSTS` in `build.py` entfernen. Sonst steht ein halbfertiger Beitrag öffentlich.
   Wenn er fertig ist: Eintrag in `POSTS` nach oben schieben und das Datum setzen,
   damit er im Insights-Bereich vorne steht.
5. **Der CV liegt bewusst nicht im Repo.** Er enthaelt die private Handynummer und
   waere auf GitHub Pages oeffentlich. Master: `material/05-originale/`. Auf der
   Seite steht stattdessen "Full CV on request". Soll er doch online, vorher die
   Telefonnummer aus dem PDF entfernen - und zwar wirklich entfernen, nicht
   schwarz ueberdecken: unter einer Flaeche bleibt der Text extrahierbar.
6. Domain registrieren und im LinkedIn-Banner die Domain anpassen.

## Anpassen

- Farben und Abstände: `:root` in `assets/style.css`.
- Texte: direkt in den HTML-Dateien, oder in `build.py` ändern und
  `python3 build.py` ausführen (überschreibt die generierten Seiten).
- Neues Projekt: Eintrag in `PROJECTS` in `build.py`, Bilder nach `assets/img/`.

## material/ — bewusst nicht im Git

`material/` enthält Schlachtplan, Motivationsschreiben, Originaldokumente,
LinkedIn-Banner und die Design-Canvas-Quellen aus dem Gesamtpaket. Das Repo ist
öffentlich, diese Unterlagen gehören nicht ins Netz — deshalb steht der Ordner
in `.gitignore` und bleibt nur lokal. Die Dateien sind vorhanden, nur eben
unversioniert; `material/GESAMTPAKET-README.md` beschreibt, was worin liegt.
