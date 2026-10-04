"""Generates index.html, work/*.html and blog/*.html from content/*.md. Run: python3 build.py"""
import hashlib
import pathlib
import re
import struct


def ver(rel):
    """Inhalts-Hash als Query an CSS und JS. Ohne den liefert jeder Cache nach
    einer Aenderung noch die alte Datei aus - lokal wie auf GitHub Pages."""
    f = ROOT / rel
    if not f.exists():
        return rel
    h = hashlib.sha1(f.read_bytes()).hexdigest()[:8]
    return f"{rel}?v={h}"

ROOT = pathlib.Path(__file__).parent


def image_size(path):
    """(breite, hoehe) eines JPEG oder PNG, ohne Zusatzbibliothek."""
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    i = 2
    while i < len(data):
        marker, length = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + length
    raise SystemExit(f"{path}: Bildgroesse nicht lesbar")
PH = lambda t: f'<span class="placeholder">[{t}]</span>'

# Texte der Projekte und Insights liegen als Markdown in content/work/ und
# content/insights/ - eine Datei pro Seite, der Dateiname ist der URL-Slug.
# Kopf zwischen den ---Zeilen: einfache "schluessel: wert"-Zeilen, Listen mit
# "  - " eingerueckt. [[Text]] wird zum markierten Platzhalter.
CONTENT = ROOT / "content"


def inline(t):
    """Inline-Markdown: **fett**, *kursiv*, [Text](url), [[Platzhalter]]."""
    t = re.sub(r"&(?!#?\w+;)", "&amp;", t)
    def link(m):
        ext = ' target="_blank" rel="noopener"' if m[2].startswith("http") else ""
        return f'<a href="{m[2]}"{ext}>{m[1]}</a>'
    t = re.sub(r"\[([^\[\]]+)\]\(([^)\s]+)\)", link, t)
    t = re.sub(r"\[\[(.+?)\]\]", lambda m: PH(m[1]), t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"<em>\1</em>", t)
    return t


def markdown(text):
    """Block-Markdown: ## Ueberschrift, Absaetze, - Listen, > Merksatz (als
    hervorgehobene Box). Bloecke, die mit < beginnen, gehen als HTML durch."""
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.strip().split("\n")
        while lines and lines[0].startswith("#"):
            level = len(lines[0]) - len(lines[0].lstrip("#"))
            out.append(f"<h{level}>{inline(lines.pop(0)[level:].strip())}</h{level}>")
        if not lines:
            continue
        if lines[0].startswith("<"):
            out.append(re.sub(r"\[\[(.+?)\]\]", lambda m: PH(m[1]), "\n".join(lines)))
        elif all(l.startswith("- ") for l in lines):
            out.append("<ul>\n" + "\n".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "\n</ul>")
        elif lines[0].startswith(">"):
            out.append(f'<div class="box"><p>{inline(" ".join(l.lstrip("> ").strip() for l in lines))}</p></div>')
        else:
            out.append(f"<p>{inline(' '.join(l.strip() for l in lines))}</p>")
    return "\n".join(out)


def read_md(path):
    """Liefert (kopf, rumpf). Der Kopf ist ein dict aus Strings und Listen."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise SystemExit(f"{path}: Kopf zwischen --- fehlt")
    meta, key = {}, None
    for line in m[1].split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in " \t" and line.strip().startswith("- "):
            meta[key].append(line.strip()[2:].strip())
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        meta[key] = value if value else []
    return meta, m[2]


def split_sections(body):
    """Text vor der ersten ##-Ueberschrift und die (Ueberschrift, Text)-Paare danach."""
    parts = re.split(r"^## +(.+)$", body.strip(), flags=re.M)
    return parts[0].strip(), [(h.strip(), t.strip()) for h, t in zip(parts[1::2], parts[2::2])]


TAKEAWAY = "What I took from it"


def load_project(path):
    meta, body = read_md(path)
    lead, sections = split_sections(body)
    take = [t for h, t in sections if h == TAKEAWAY]
    # "|" trennt Bildreihen (nur fuer media: full), "," die Bilder einer Reihe.
    rows = [[f.strip() for f in r.split(",") if f.strip()] for r in meta.get("images", "").split("|")]
    rows = [r for r in rows if r]
    files = [f for r in rows for f in r]
    # Enthaelt ein Abschnitt Bilder (![alt](datei.jpg), eine Zeile je Bild),
    # wird die Seite in Abschnitte mit eigenen Bildern gegliedert statt in Spalten.
    IMG = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)\s*$", re.M)
    cases = []
    if any(IMG.search(t) for h, t in sections if h != TAKEAWAY):
        cases = [(inline(h), markdown(IMG.sub("", t)), [(f, a) for a, f in IMG.findall(t)])
                 for h, t in sections if h != TAKEAWAY]
    return dict(
        slug=path.stem, order=int(meta.get("order", 999)),
        kicker=inline(meta["kicker"]), title=inline(meta["title"]),
        summary=inline(meta["summary"]), lead=inline(lead),
        facts=[tuple(inline(x.strip()) for x in f.split(":", 1)) for f in meta.get("facts", [])],
        media=(meta["media"], meta.get("media_tone", ""), files) if meta.get("media") else None,
        rows=rows, results=meta.get("results") == "true",
        cols=[] if cases else [(inline(h), inline(t)) for h, t in sections if h != TAKEAWAY],
        cases=cases, takeaway=inline(take[0]) if take else "")


def load_post(path):
    meta, body = read_md(path)
    lead, rest = re.split(r"\n\s*\n", body.strip() + "\n\n", maxsplit=1)
    return dict(
        slug=path.stem, order=int(meta.get("order", 999)), date=meta["date"],
        kicker=inline(meta["kicker"]), title=inline(meta["title"]),
        teaser=inline(meta["teaser"]), lead=inline(" ".join(lead.split("\n"))),
        body="\n" + markdown(rest) + "\n",
        embeds=[tuple(x.strip() for x in e.split("|")) for e in meta.get("embeds", [])],
        clips=[tuple(x.strip() for x in c.split("|")) for c in meta.get("clips", [])])


def load_all(folder, loader):
    items = [loader(f) for f in sorted((CONTENT / folder).glob("*.md"))]
    return sorted(items, key=lambda p: (p["order"], p["slug"]))


PROJECTS = load_all("work", load_project)

def head(title, depth):
    a = "../" if depth else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Saskia Kempf – Digital Marketing Manager in Zurich. Web, performance and content marketing: WordPress, Google Ads, Meta, SEO and short-form video.">
<link rel="stylesheet" href="{a}{ver("assets/style.css")}">
</head>
<body>
<canvas class="waves bg" data-fixed data-lines="90" data-funnel="0.14" data-from="0.05" data-amp="0.24" data-opacity="0.8" aria-hidden="true"></canvas>
<header class="site-header"><div class="wrap">
<a class="brand" href="{a}index.html">Saskia Kempf</a>
<button class="nav-toggle" aria-expanded="false" aria-controls="nav" onclick="var n=document.getElementById('nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))">Menu</button>
<nav class="nav" id="nav">
<a href="{a}index.html#work">Work</a>
<a href="{a}index.html#about">About</a>
<a href="{a}blog/index.html">Insights</a>
<a href="{a}index.html#contact">Contact</a>
<a class="btn dark" href="{a}index.html#contact">Get in touch</a>
</nav>
</div></header>
"""

def foot(depth, scripts=()):
    a = "../" if depth else ""
    extra = "".join(f'\n<script src="{a}{ver("assets/" + s)}"></script>' for s in scripts)
    return f"""<footer><div class="wrap"><span>© 2026 Saskia Kempf</span><span>Zurich, Switzerland · German / English</span></div></footer>
<script src="{a}{ver("assets/waves.js")}"></script>
<script src="{a}{ver("assets/motion.js")}"></script>{extra}
</body>
</html>
"""

def card(p):
    m = p["media"]
    def img(f, cls=""):
        c = ' class="%s"' % cls if cls else ""
        return '<img src="assets/img/%s" alt=""%s>' % (f, c)
    if p["slug"] == "paid-social": media = '<div class="media grid2">' + "".join('<div class="cell">' + img(f) + '</div>' for f in m[2]) + "</div>"
    elif p["slug"] == "tiktok-top-ads": media = '<div class="media">' + "".join(img(f, "phone") for f in m[2]) + "</div>"

    elif p["slug"] == "landing-page": media = '<div class="media">' + img("p1_landing.jpg", "browser") + "</div>"
    elif p["slug"] == "linkedin-content": media = '<div class="media grid3">' + "".join('<div class="cell">' + img(f) + '</div>' for f in m[2]) + "</div>"
    elif p["slug"] == "video-content": media = '<div class="media">' + "".join(img(f, "phone") for f in m[2][:2]) + "</div>"
    else: media = '<div class="media pair">' + "".join(img(f) for f in m[2]) + "</div>"
    return f"""<a class="card reveal" href="work/{p['slug']}.html">{media}
<div class="kicker">{p['kicker']}</div><h3>{p['title']}</h3><p>{p['summary']}</p></a>"""

# Lebenslauf und Qualifikationen als Daten statt als HTML-Klumpen. Jede Position
# hat Zeitraum, Rolle und Arbeitgeber getrennt; zuvor steckten die beiden
# ABC-Design-Stellen in einer einzigen Zeile, durch "·" verkettet, in der nicht
# erkennbar war, was Rolle und was Arbeitgeber ist.
CAREER = [
 ("Dec 2024 – now",      "Marketing &amp; Communication Specialist", "Compass Group (Schweiz) AG", "Zurich, CH"),
 ("Apr 2023 – Dec 2024", "Digital Marketing Manager",                "Schwarzwaldbruder GmbH",     "Tiengen, DE"),
 ("Jan 2022 – Apr 2023", "Marketing Manager, moji brand",            "ABC Design GmbH",            "Albbruck, DE"),
 ("Apr 2021 – Apr 2023", "Content Manager",                          "ABC Design GmbH",            "Albbruck, DE"),
 ("Oct 2019 – Apr 2021", "Working student, Account Management",      "Visual Statements GmbH",     "Freiburg, DE"),
]

EDUCATION = [
 ("2026",        "UX/UI Design",                  "Onlineschule für Gestaltung"),
 ("2017 – 2021", "B.A. Media Concept and Design", "Hochschule Furtwangen, DE"),
 ("2018 – 2019", "Practical semester, online and social media editorial", "Europa-Park, Rust, DE"),
]

FOCUS = ["Google Ads &amp; Meta Ads", "Websites &amp; landing pages", "SEO &amp; content",
         "KPI &amp; performance analysis", "Short-form video", "UX/UI design"]

TOOLS = ["WordPress (Elementor)", "Google Ads", "Meta Business Manager", "GA4",
         "Adobe Creative Cloud", "Figma", "Canva", "CapCut", "HubSpot"]

def about_section():
    LANGUAGES = [("German", "native"), ("English", "C1"), ("French", "A2"), ("Spanish", "A1")]
    career = "".join(
        f'<li><time>{when}</time><div class="what"><span class="role">{role}</span>'
        f'<span class="org">{org}<span class="place"> · {place}</span></span></div></li>'
        for when, role, org, place in CAREER)
    edu = "".join(
        f'<li><time>{when}</time><div class="what"><span class="role">{what}</span>'
        f'<span class="org">{where}</span></div></li>'
        for when, what, where in EDUCATION)
    focus = "".join(f'<li class="chip">{c}</li>' for c in FOCUS)
    tools = "".join(f'<li>{c}</li>' for c in TOOLS)
    langs = "".join(f'<li><span class="lang">{n}</span><span class="lvl">{l}</span></li>' for n, l in LANGUAGES)
    return f"""<section class="section about reveal" id="about"><div class="wrap">
<div class="about-main">
<h2>About</h2>
<p class="lead-in">My strength is the link between web and performance: I build the page, think through the user journey, and then make sure the right people arrive there through Google Ads, Meta or SEO – and that I can measure what happened.</p>
<h3>Career</h3>
<ol class="cv">{career}</ol>
<h3>Education</h3>
<ol class="cv">{edu}</ol>
<h3>Outside work</h3>
<p class="aside-note">I build and run my own road cycling channel on Instagram and TikTok – my own niche, my own formats, and a testing ground for short-form ideas without a brief. <a href="blog/building-a-channel-from-zero.html">How I went about it →</a></p>
</div>
<div class="about-side">
<section class="block"><h3>Focus areas</h3><ul class="tags">{focus}</ul></section>
<section class="block"><h3>Tools</h3><ul class="inline-list">{tools}</ul></section>
<section class="block"><h3>Languages</h3><ul class="lang-list">{langs}</ul></section>
<section class="block"><h3>Based in</h3><p>Near Zurich. Working in Switzerland since December 2024, open to roles in the Zurich area.</p></section>
</div>
</div></section>"""


def index():
    g = PROJECTS[0]
    cards = "\n".join(card(p) for p in PROJECTS[1:])
    return head("Saskia Kempf – Digital Marketing Manager, Zurich", 0) + f"""
<section class="hero"><div class="wrap">
<div>
<div class="eyebrow">Digital Marketing Manager · Zurich</div>
<h1>Websites that convert. Campaigns that prove it.</h1>
<p class="lead muted">Six years in web, performance and content marketing. I build and optimise WordPress sites, run Google and Meta campaigns, and design the content that feeds them – with a Media Design background and UX/UI training behind it.</p>
<div class="pipes">Web<span>|</span>Digital Marketing<span>|</span>Social Media<span>|</span>UX/UI<span>|</span>Performance</div>
<div class="actions"><a class="btn primary" href="#work">See my work</a><a class="btn" href="#contact">Get in touch</a></div>
</div>
<div class="photo-tile"><img src="assets/img/hero.jpg" alt="Saskia Kempf"></div>
</div></section>

<section class="stats reveal"><div class="wrap"><div class="grid">
<div class="cell"><div class="n">6+ yrs</div><div class="l">Web, performance &amp; content marketing</div></div>
<div class="cell"><div class="n">13.9 %</div><div class="l">CTR on a 3-month Google Ads Search campaign</div></div>
<div class="cell"><div class="n">2× Top Ads</div><div class="l">Featured in the TikTok Creative Center</div></div>
<div class="cell"><div class="n">DE · CH</div><div class="l">Brands in hospitality, e-commerce and B2B</div></div>
</div></div></section>

<section class="section" id="work"><div class="wrap">
<div class="section-head"><h2>Selected work</h2></div>
<a class="featured reveal" href="work/{g['slug']}.html">
<div class="text">
<div class="tags"><span class="chip">Google Ads</span><span class="chip">Lead generation</span><span class="chip">Case study</span></div>
<h3>{g['title']}</h3><p>{g['summary']}</p><span class="more">Read the case study →</span>
</div>
<div class="nums">
<div><div class="n">15'574</div><div class="l">Impressions</div></div>
<div><div class="n">2'166</div><div class="l">Clicks</div></div>
<div><div class="n hi">13.91 %</div><div class="l">CTR</div></div>
<div><div class="n">CHF 1.35</div><div class="l">CPC</div></div>
</div></a>
<div class="work-grid">
{cards}
</div>
</div></section>

""" + about_section() + """

<section class="section teaser"><div class="wrap">
<div class="section-head"><h2>Insights</h2><a href="blog/index.html" class="muted" style="font-weight:500">All posts →</a></div>
<div class="post-list">
""" + "\n".join(post_card(p, 0) for p in POSTS) + """
</div>
</div></section>

<section class="section contact reveal" id="contact"><div class="wrap">
<div>
<h2>Let's build the next digital chapter.</h2>
<p class="lead muted">Open to Digital, Web and Performance Marketing roles in the Zurich area. Happy to walk you through any of the projects above.</p>
<div class="actions">
<a class="btn primary" href="mailto:saskia.kmpf@gmail.com">saskia.kmpf@gmail.com</a>
<a class="btn" href="https://www.linkedin.com/in/saskiakempf" target="_blank" rel="noopener">LinkedIn</a>
</div>
<p class="cv-note muted">Full CV on request – just drop me a line.</p>
</div>
<img src="assets/img/contact.jpg" alt="">
</div></section>
""" + foot(0)

# Web-Fassungen der Clips aus dem Drive-Ordner. Master liegen in material/videos
# (nicht versioniert), erzeugt mit dem Encoder in scratchpad/encode2.py.
VIDEOS = list(range(1, 13))
DRIVE_FOLDER = "https://drive.google.com/drive/folders/1-2eR9gPsE5PjhS9vxOIZrPALVPO6YB1_?usp=sharing"

def video_gallery(depth=1):
    a = "../" if depth else ""
    items = "".join(
        f'<figure><video src="{a}assets/video/video-{n}.mp4" poster="{a}assets/video/video-{n}.jpg"'
        f' muted loop playsinline preload="none" aria-label="Short-form video {n}"></video></figure>'
        for n in VIDEOS)
    return (f'<div class="video-grid reveal">{items}</div>'
            '<p class="video-note">Clips play muted while in view – click one for sound and controls. '
            f'<a href="{DRIVE_FOLDER}" target="_blank" rel="noopener">Originals in full resolution</a></p>')


def full_img(f, alt=""):
    """Screenshot ungeschnitten. In einer .row waechst jedes Bild im Verhaeltnis
    seines Seitenverhaeltnisses (--ar), dadurch sind alle gleich hoch."""
    w, h = image_size(ROOT / "assets" / "img" / f)
    return f'<img src="../assets/img/{f}" alt="{alt}" width="{w}" height="{h}" style="--ar:{w / h:.4f}" loading="lazy">'


def full_row(items):
    """Eine Reihe gleich hoher Screenshots, items = [(datei, alt)]. Die Reihe wird
    so begrenzt, dass kein Bild ueber seine Originalgroesse hinaus (unscharf) waechst."""
    sizes = [image_size(ROOT / "assets" / "img" / f) for f, _ in items]
    height = min(h for w, h in sizes)
    width = round(height * sum(w / h for w, h in sizes)) + 20 * (len(items) - 1)
    imgs = "".join(full_img(f, a) for f, a in items)
    return f'<div class="row" style="max-width:{width}px">{imgs}</div>'


def project(p, nxt, num):
    facts = "".join(f'<div><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in p["facts"])
    cols = "".join(f'<div class="col{" a" if i==1 else ""}"><h2>{h}</h2><p>{t}</p></div>' for i, (h, t) in enumerate(p["cols"]))
    if p["results"]:
        media = """<div class="results reveal">
<div class="label">Results at a glance</div>
<div class="nums">
<div><div class="n">15'574</div><div class="l">Impressions</div></div>
<div><div class="n">2'166</div><div class="l">Clicks</div></div>
<div><div class="n hi">13.91 %</div><div class="l">CTR</div></div>
<div><div class="n">CHF 1.35</div><div class="l">Avg. CPC</div></div>
<div><div class="n">19</div><div class="l">Leads</div></div>
</div>
<div class="split">
<div><div class="label" style="margin-bottom:4px">Lead split by campaign</div>
<div class="bars"><div class="bar">12<i style="height:72px"></i></div><div class="bar b">7<i style="height:42px"></i></div></div>
<div class="bar-labels"><span>Offer (region &amp; food)</span><span>Target audience</span></div></div>
<div><div class="label" style="margin-bottom:8px">In context</div>
<p>Google Search benchmark for Restaurants &amp; Food: 6.83 % CTR at USD 2.05 CPC (<a href="https://localiq.com/blog/search-advertising-benchmarks/" target="_blank" rel="noopener">LocaliQ 2026</a>, US data). This campaign reached twice that CTR at CHF 1.35 per click.</p></div>
</div></div>"""
    else:
        kind, tone, files = p["media"]
        if kind == "full":
            imgs = "".join(full_row([(f, "") for f in r]) for r in p["rows"])
        else:
            imgs = "".join(f'<img src="../assets/img/{f}" alt="">' for f in files)
        media = f'<div class="hero-media reveal {kind} {tone}">{imgs}</div>'
    if p["slug"] == "video-content":
        media = video_gallery(1)
    body = f'<div class="cols reveal">{cols}</div>'
    if p["cases"]:
        media = ""
        body = "".join(
            f'<section class="case reveal"><div class="case-text"><h2>{h}</h2>{t}</div>'
            + (f'<div class="hero-media full {p["media"][1] if p["media"] else ""}">{full_row(imgs)}</div>' if imgs else "")
            + '</section>'
            for h, t, imgs in p["cases"])
    return head(f"{p['title']} – Saskia Kempf", 1) + f"""
<section class="project-hero"><div class="wrap">
<a href="../index.html#work" class="muted" style="text-decoration:none;font-weight:500">← All work</a>
<div class="pnum">Project {num:02d}</div>
<div class="eyebrow" style="margin-top:8px">{p['kicker']}</div>
<h1>{p['title']}</h1>
<p class="lead muted">{p['lead']}</p>
<div class="facts">{facts}</div>
{media}
{body}
<div class="takeaway reveal"><div class="eyebrow">What I took from it</div><p>{p['takeaway']}</p></div>
<a class="next" href="{nxt['slug']}.html"><span><div class="k">Next project</div><div class="t">{nxt['title']}</div></span><span class="arrow">→</span></a>
</div></section>
""" + foot(1, ("video.js",) if p["slug"] == "video-content" else ())


POSTS = load_all("insights", load_post)

def post_card(p, depth):
    a = "../" if depth else ""
    return f"""<a class="post reveal" href="{a}blog/{p['slug']}.html"><div class="meta">{p['kicker']}</div><h3>{p['title']}</h3><p>{p['teaser']}</p><span class="date">{p['date']}</span></a>"""

def blog_index():
    cards = "\n".join(post_card(p, 1) for p in POSTS)
    return head("Insights – Saskia Kempf", 1) + f"""
<section class="blog-head"><div class="wrap">
<div class="eyebrow">Insights</div>
<h1>Notes from the work</h1>
<p class="lead muted">Short, practical pieces on what actually moved the numbers – from paid social and Google Ads to landing pages. Written from my own projects, not from theory.</p>
</div></section>
<section><div class="wrap"><div class="post-list">
{cards}
</div></div></section>
""" + foot(1)

def post_embeds(p):
    """Zwei-Klick-Einbettungen. Es wird zunaechst nur eine eigene Vorschaukarte
    gerendert; der iframe entsteht erst beim Klick (assets/embed.js). Dadurch
    geht bis dahin kein Request an TikTok oder Meta und es werden keine fremden
    Cookies gesetzt. Eintraege: (plattform, id, titel, kennzahl)."""
    embeds = p.get("embeds") or []
    if not embeds:
        return ""
    karten = "".join(
        f'<figure class="embed-card" data-embed="{plat}" data-id="{eid}" data-title="{titel}">'
        f'<button class="embed-load" type="button" aria-label="Play &quot;{titel}&quot; – loads from {plat}">'
        f'<img src="../assets/video/social/{thumb}" alt="" loading="lazy" width="440" height="782">'
        f'<span class="embed-badge">{kennzahl}</span>'
        f'<span class="embed-play" aria-hidden="true"></span>'
        f'<span class="embed-foot"><span class="embed-title">{titel}</span>'
        f'<span class="embed-hint">Plays from {plat} – not contacted until you tap</span></span>'
        f'</button></figure>'
        for plat, eid, titel, kennzahl, thumb in embeds)
    return f'<div class="embed-grid">{karten}</div>'


def post_clips(p):
    """Kleine Clip-Galerie im Beitrag. Quelle sind Saskias eigene Kanaele, darum
    selbst ausgeliefert statt per Instagram-/TikTok-Embed: die Seite kommt so
    weiterhin ohne einen einzigen externen Request und ohne Cookies Dritter aus.
    Solange keine Dateien hinterlegt sind, rendert der Block nichts."""
    clips = p.get("clips") or []
    if not clips:
        return ""
    items = "".join(
        f'<figure><video src="../assets/video/social/{name}.mp4"'
        f' poster="../assets/video/social/{name}.jpg"'
        f' muted loop playsinline preload="none" aria-label="{cap}"></video>'
        f'<figcaption>{cap}</figcaption></figure>'
        for name, cap in clips)
    return f'<div class="video-grid in-article">{items}</div>'


def post_page(p, i):
    prev = POSTS[i-1] if i > 0 else None
    nxt = POSTS[i+1] if i < len(POSTS)-1 else None
    back = '<div class="back">' + (f'<a href="{prev["slug"]}.html">← {prev["title"]}</a>' if prev else '<span></span>') + (f'<a href="{nxt["slug"]}.html">{nxt["title"]} →</a>' if nxt else '<a href="index.html">All insights →</a>') + '</div>'
    return head(f"{p['title']} – Saskia Kempf", 1) + f"""
<article class="article">
<a href="index.html" class="muted" style="text-decoration:none;font-weight:500">← All insights</a>
<div class="meta" style="margin-top:28px">{p['kicker']}</div>
<h1>{p['title']}</h1>
<div class="date">{p['date']} · Saskia Kempf</div>
<p class="lead">{p['lead']}</p>
{p['body']}
{post_embeds(p)}
{post_clips(p)}
{back}
</article>
""" + foot(1, tuple(s for s, k in (("video.js", "clips"), ("embed.js", "embeds")) if p.get(k)))

(ROOT / "blog").mkdir(exist_ok=True)
(ROOT / "blog" / "index.html").write_text(blog_index(), encoding="utf-8")
for i, p in enumerate(POSTS):
    (ROOT / "blog" / f"{p['slug']}.html").write_text(post_page(p, i), encoding="utf-8")

(ROOT / "index.html").write_text(index(), encoding="utf-8")
for i, p in enumerate(PROJECTS):
    (ROOT / "work" / f"{p['slug']}.html").write_text(project(p, PROJECTS[(i + 1) % len(PROJECTS)], i + 1), encoding="utf-8")
print("built", 2 + len(PROJECTS) + len(POSTS), "pages")
