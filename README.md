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
blog/                       Insights: index.html + 5 Beiträge
content/work/*.md           Texte der Projektseiten (Quelle für work/)
content/insights/*.md       Texte der Insights-Beiträge (Quelle für blog/)
assets/style.css            gesamtes Styling (Farben in :root, --accent ist das Blau)
assets/waves.js             animierte Wellenlinien im Hintergrund
assets/fonts/               Figtree (Open Font License)
assets/img/                 Projektbilder und Fotos
build.py                    erzeugt index.html, work/ und blog/ aus content/*.md
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

1. Platzhalter in eckigen Klammern füllen — in den Texten stehen sie als `[[…]]`:
   `grep -rn '\[\[' content`, auf den fertigen Seiten `grep -rn 'class="placeholder"' index.html work blog`.
   Betrifft vor allem Resultate mit Zahlen, Kunde/Branche.
2. Bildfreigaben der Arbeitgeber und Kunden prüfen.
3. Blog-Beiträge in eigene Worte bringen (aktuell Entwürfe).
4. **`content/insights/building-a-channel-from-zero.md`**: Die Zahlen stammen vom
   öffentlichen TikTok-Profil (Stand September 2026) – vor dem Livegang aktualisieren,
   inklusive Durchschnitt und Anteil der zwei stärksten Posts im Abschnitt "What came of it".
5. **Der CV liegt bewusst nicht im Repo.** Er enthaelt die private Handynummer und
   waere auf GitHub Pages oeffentlich. Master: `material/05-originale/`. Auf der
   Seite steht stattdessen "Full CV on request". Soll er doch online, vorher die
   Telefonnummer aus dem PDF entfernen - und zwar wirklich entfernen, nicht
   schwarz ueberdecken: unter einer Flaeche bleibt der Text extrahierbar.
6. Domain registrieren und im LinkedIn-Banner die Domain anpassen.

## Anpassen

- Farben und Abstände: `:root` in `assets/style.css`.
- Texte der Projekte und Insights: die Markdown-Datei in `content/work/` bzw.
  `content/insights/` bearbeiten, dann `python3 build.py` ausführen. Die HTML-Dateien
  in `work/` und `blog/` sind erzeugt — dort nicht von Hand ändern, der nächste
  Build überschreibt sie. Beim Push baut GitHub Actions ohnehin neu.
- Neues Projekt / neuer Beitrag: Markdown-Datei anlegen (am einfachsten eine
  bestehende kopieren). Der Dateiname wird zur URL, `order:` bestimmt die Reihenfolge.
  Bilder nach `assets/img/`.
- Startseite (Hero, Kennzahlen, About, Kontakt) und das Layout stehen weiter in `build.py`.

### Markdown-Format

```markdown
---
order: 1
date: 2026-10                     # nur bei Insights
kicker: Paid social
title: Titel der Seite
teaser: Kurztext für die Übersicht  # bei Projekten: summary
---

Erster Absatz = Lead (der grosse Einleitungstext).

## Zwischenüberschrift

Absatz mit **fett**, *kursiv* und [Link](https://example.com).

- Listenpunkt

> Merksatz, wird als hervorgehobene Box dargestellt.

[[Platzhalter]] wird blau markiert, bis der echte Inhalt drinsteht.
```

Projektseiten: jede `##`-Überschrift wird eine Spalte, der Abschnitt
`## What I took from it` wird der Merksatz am Ende. Kopffelder dort: `summary`,
`facts` (Liste `  - Label: Wert`), `media` (`grid`, `grid two`, `grid three`,
`phones`), optional `media_tone: blue`, `images` (kommagetrennt).

## material/ — bewusst nicht im Git

`material/` enthält Schlachtplan, Motivationsschreiben, Originaldokumente,
LinkedIn-Banner und die Design-Canvas-Quellen aus dem Gesamtpaket. Das Repo ist
öffentlich, diese Unterlagen gehören nicht ins Netz — deshalb steht der Ordner
in `.gitignore` und bleibt nur lokal. Die Dateien sind vorhanden, nur eben
unversioniert; `material/GESAMTPAKET-README.md` beschreibt, was worin liegt.
