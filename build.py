"""Generates index.html and work/*.html. Run: python3 build.py"""
import pathlib
import hashlib


def ver(rel):
    """Inhalts-Hash als Query an CSS und JS. Ohne den liefert jeder Cache nach
    einer Aenderung noch die alte Datei aus - lokal wie auf GitHub Pages."""
    f = ROOT / rel
    if not f.exists():
        return rel
    h = hashlib.sha1(f.read_bytes()).hexdigest()[:8]
    return f"{rel}?v={h}"

ROOT = pathlib.Path(__file__).parent
PH = lambda t: f'<span class="placeholder">[{t}]</span>'
# Stichtag der Social-Zahlen im Beitrag. Beim Aktualisieren hier und im
# Ergebnisblock die Werte anpassen - Reichweitenzahlen veralten schnell.
SOCIAL_ASOF = "September 2026"

PROJECTS = [
 dict(slug="google-ads", kicker="Google Ads · Lead generation", title="Search campaigns that turned clicks into qualified leads",
  summary="Setup, structure and continuous optimisation of Google Ads Search over three months – keyword clusters, negative keywords, search term cleaning and ad testing.",
  lead="A three-month lead generation campaign: I set up the account structure, wrote the ads, and cleaned the search terms week by week to keep spend on the queries that actually convert.",
  facts=[("My role","Setup, structure, ad copy, optimisation, reporting"),("Client",PH("Client or industry")),("Duration","3 months"),("Goal","Generate leads via Google Ads Search")],
  media=None, results=True,
  cols=[("Setup","Keyword clusters by intent, match types chosen per cluster, a negative keyword list from day one, and ad extensions to lift the click-through rate."),
        ("Optimisation","Weekly search term analysis, ad copy tests, and continuous relevance and quality work. Wasted spend was cut by excluding queries that clicked but never converted."),
        ("Outcome","Relevant search queries identified, wasted spend reduced, and lead quality improved. The offer-led campaign delivered almost twice the leads of the audience-led one.")],
  takeaway="A clear account structure and consistent search term cleaning do more for lead quality than any single ad. Offers tied to a concrete need beat broad audience targeting."),
 dict(slug="paid-social", kicker="Meta Ads · Creative testing", title="Paid social creatives with a sales objective",
  summary="Hook, benefit and proof variations, A/B tests and scaling of winning creatives. "+PH("Result in numbers: ROAS, CPA or CTR uplift"),
  lead="Performance-driven Meta ads for an e-commerce brand: I developed the concept, wrote the copy, designed the creatives and built the variations the campaign was tested with.",
  facts=[("My role","Concept, copy, design, creative variations"),("Client",PH("Client or industry")),("Channels","Facebook & Instagram"),("Goal","Sales")],
  media=("grid","",["ad1.jpg","ad2.jpg","ad3.jpg","ad4.jpg"]), results=False,
  cols=[("Execution","Hook variations, benefit and proof variations, audiences and placements, and format adaptations for feed and stories."),
        ("Testing","Iterations based on performance signals, A/B tests, and scaling of the winning variations."),
        ("Outcome","Best-performing creatives identified, scaled, and developed into further variations. "+PH("ROAS / CPA / CTR result"))],
  takeaway="Scroll-stopping hooks with a clear everyday situation or pain point were crucial for performance – more than any visual polish."),
 dict(slug="tiktok-top-ads", kicker="TikTok Ads · UGC", title="Two campaigns featured as TikTok Top Ads",
  summary="Concept, copy, editing, setup and optimisation. Content that felt like organic UGC performed best and was selected for the Creative Center.",
  lead="Performance-driven TikTok ads with a sales focus. Two of the campaigns were featured as Top Ads in the TikTok Creative Center – TikTok's own showcase of high-performing ads.",
  facts=[("My role","Concept, copywriting, editing, ad setup, optimisation"),("Client",PH("Client or industry")),("Format","9:16 short-form video"),("Goal","Sales")],
  media=("phones","dark",["tiktok1.jpg","vid1.jpg"]), results=False,
  cols=[("Execution","Hook variations, clear benefits, fast-paced cuts and iterative testing of openings and CTAs."),
        ("Result","Featured in the TikTok Creative Center as Top Ads – twice. "+PH("Views, CTR or conversion numbers")),
        ("Videos",'The ads and further clips are on the <a href="video-content.html">short-form video page</a>.')],
  takeaway="Content that felt like organic UGC performed best. The less it looked like an ad, the better it sold."),
 dict(slug="landing-page", kicker="WordPress · Landing page", title="Landing page built for lead generation",
  summary="Concept, structure, copy and implementation in WordPress and Elementor, with a clear user flow and mobile-first readability. "+PH("Conversion or lead result"),
  lead="A landing page to support lead generation: I defined the structure and user journey, wrote the content and built the page in WordPress with Elementor.",
  facts=[("My role","Concept, structure, copy, implementation"),("Client",PH("Client or industry")),("Stack","WordPress, Elementor"),("Goal","Lead generation")],
  media=("grid two","blue",["p1_landing.jpg"]), results=False,
  cols=[("UX focus","Clear layout, intuitive navigation and mobile readability – one message per section, one unambiguous call to action."),
        ("Execution","Sections, content, visual hierarchy, QA and updates after launch."),
        ("Outcome","Landing page launched with an optimised structure and user flow. "+PH("Conversion rate, leads or time on page"))],
  takeaway="A clear structure and unambiguous CTAs do more for the user journey than any single design element."),
 dict(slug="linkedin-content", kicker="LinkedIn · B2B & employer branding", title="Editorial planning and design for LinkedIn",
  summary="Editorial calendar, mixed formats, hook structure and reusable templates for a consistent presence. "+PH("Reach or follower growth"),
  lead="Content planning and design for LinkedIn with a focus on employer branding and B2B visibility – from the editorial calendar to publishing.",
  facts=[("My role","Topic planning, copywriting, design, publishing"),("Client",PH("Client or industry")),("Formats","Carousels, single posts, job posts"),("Goal","Visibility & positioning")],
  media=("grid three","",["li1.jpg","li2.jpg","li3.jpg"]), results=False,
  cols=[("Execution","Editorial calendar, a mix of formats, a clear hook structure and design templates that the team can reuse."),
        ("Result","A consistent LinkedIn presence and reusable templates. "+PH("Impressions, engagement rate or follower growth")),
        ("Also","I lead LinkedIn workshops on personal branding and communication for colleagues.")],
  takeaway="A consistent mix of formats improves recognition and reveals which topics and hooks actually drive performance."),
 dict(slug="video-content", kicker="Video · Instagram & TikTok", title="Short-form video from script to edit",
  summary="UGC-style content, on-camera Reels in 9:16, subtitles and clear CTAs – for organic and paid use.",
  lead="Video content for Instagram and TikTok focused on sales, leads and growth: concept, scripting, filming and editing, plus coordination on set.",
  facts=[("My role","Concept, scripting, filming, editing, coordination"),("Client",PH("Client or industry")),("Formats","UGC-style, on-camera, Reels 9:16"),("Tools","CapCut, Adobe Premiere")],
  media=("phones","",["vid1.jpg","vid2.jpg","tiktok1.jpg"]), results=False,
  cols=[("Execution","Scroll-stopping opening, a clear message, subtitles, a call to action and variations for testing."),
        ("Result","A best-of reel and individual formats for organic and paid use. "+PH("Views or engagement numbers")),
        ("Videos","Twelve clips are embedded below – concept, filming and edit by me.")],
  takeaway="Short videos with a clear message in the first few seconds perform best. Everything after that is editing."),
 dict(slug="ux-ui", kicker="UX/UI · Figma · Training projects", title="Responsive blog and calculator interfaces",
  summary="Two concept projects from my UX/UI training: information hierarchy, user flow and responsive adaptation from desktop to mobile.",
  lead="Two concept projects from my UX/UI Design training (2026): a responsive blog layout and an electricity cost calculator. Both designed in Figma, from structure to mobile adaptation.",
  facts=[("My role","Concept, structure, UX/UI design, responsive adaptation"),("Context","UX/UI Design training"),("Tool","Figma"),("Year","2026")],
  media=("grid two","blue",["p2_blog.jpg","p3_calc.jpg"]), results=False,
  cols=[("Blog UX & editorial design","Hero section, article overview, categories, newsletter and footer – with a clear hierarchy, readability and a consistent experience across devices."),
        ("Electricity calculator","Clear input fields, easy-to-understand results and a seamless mobile experience: input flow, results display and visual hierarchy."),
        ("Why it matters","The training sharpened how I look at every landing page: hierarchy first, then copy, then the visual layer.")],
  takeaway="Responsive design is not about scaling down. It is about consciously adapting content, proportions and hierarchy to each screen."),
]

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
    if p["slug"] == "paid-social": media = '<div class="media grid2">' + "".join(img(f) for f in m[2]) + "</div>"
    elif p["slug"] == "tiktok-top-ads": media = '<div class="media dark">' + "".join(img(f, "phone") for f in m[2]) + "</div>"
    elif p["slug"] == "landing-page": media = '<div class="media blue">' + img("p1_landing.jpg", "browser") + "</div>"
    elif p["slug"] == "linkedin-content": media = '<div class="media grid3">' + "".join(img(f) for f in m[2]) + "</div>"
    elif p["slug"] == "video-content": media = '<div class="media">' + "".join(img(f, "phone") for f in m[2][:2]) + "</div>"
    else: media = '<div class="media blue pair">' + "".join(img(f) for f in m[2]) + "</div>"
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
 ("2026",        "UX/UI Design",                  "Further training"),
 ("2017 – 2021", "B.A. Media Concept and Design", "Hochschule Furtwangen, DE"),
 ("2018 – 2019", "Practical semester, online and social media editorial", "Europa-Park, Rust, DE"),
]

FOCUS = ["Google Ads &amp; Meta Ads", "Websites &amp; landing pages", "SEO &amp; content",
         "KPI &amp; performance analysis", "Short-form video", "UX/UI design"]

TOOLS = ["WordPress (Elementor)", "Google Ads", "Meta Business Manager", "GA4",
         "Adobe Creative Cloud", "Figma", "Canva", "CapCut", "HubSpot"]

def about_section():
    LANGUAGES = [("German", "native"), ("English", PH("C1")), ("French", PH("level")), ("Spanish", PH("level"))]
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
<div class="section-head"><h2>Selected work</h2><span class="muted">Performance · Web · Content</span></div>
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
<p>""" + PH("Industry benchmark CTR for comparison") + " · " + PH("Cost per lead and what a lead is worth") + " · " + PH("How CTR / CPC developed from month 1 to 3") + """</p></div>
</div></div>"""
    else:
        kind, tone, files = p["media"]
        imgs = "".join(f'<img src="../assets/img/{f}" alt="">' for f in files)
        media = f'<div class="hero-media reveal {kind} {tone}">{imgs}</div>'
    if p["slug"] == "video-content":
        media = video_gallery(1)
    return head(f"{p['title']} – Saskia Kempf", 1) + f"""
<section class="project-hero"><div class="wrap">
<a href="../index.html#work" class="muted" style="text-decoration:none;font-weight:500">← All work</a>
<div class="pnum">Project {num:02d}</div>
<div class="eyebrow" style="margin-top:8px">{p['kicker']}</div>
<h1>{p['title']}</h1>
<p class="lead muted">{p['lead']}</p>
<div class="facts">{facts}</div>
{media}
<div class="cols reveal">{cols}</div>
<div class="takeaway reveal"><div class="eyebrow">What I took from it</div><p>{p['takeaway']}</p></div>
<a class="next" href="{nxt['slug']}.html"><span><div class="k">Next project</div><div class="t">{nxt['title']}</div></span><span class="arrow">→</span></a>
</div></section>
""" + foot(1, ("video.js",) if p["slug"] == "video-content" else ())


POSTS = [
 dict(slug="tiktok-top-ads-learnings", date="2026-09", kicker="Paid social",
  title="What two TikTok Top Ads taught me about performance creative",
  teaser="The ads that performed best were the ones that looked least like ads. Three things I now do differently.",
  lead="Two of my TikTok campaigns were featured as Top Ads in the TikTok Creative Center. Looking back, the winners had less to do with production value than with the first two seconds.",
  body="""
<h2>The setup</h2>
<p>Both campaigns had a sales objective and ran with several creative variations: different hooks, different benefit angles, different pacing. I wrote, filmed and cut most of them myself, and iterated weekly based on the performance signals.</p>
<h2>What actually worked</h2>
<ul>
<li><b>UGC beats polish.</b> The videos that felt like a real person talking to the camera outperformed everything with a "produced" look. Same product, same offer – different trust.</li>
<li><b>The hook is the ad.</b> If the first two seconds did not name a concrete everyday situation or a pain point, the rest of the video did not matter. Watch time dropped before the benefit was even mentioned.</li>
<li><b>Cut faster than feels comfortable.</b> Every version with quicker cuts and fewer words held attention longer. What felt rushed in the edit was right in the feed.</li>
</ul>
<div class="box"><p>Content that felt like organic UGC performed best – and those were the two ads TikTok picked as Top Ads.</p></div>
<h2>What I do differently now</h2>
<p>I start every short-form concept with a list of hooks, not with a storyboard. I test at least three openings per message before I touch anything else. And I keep one "too raw" version in every test set, because that is often the one that wins.</p>
<p>[Optional: add the campaign's numbers here – views, CTR or conversion rate – if the client agrees.]</p>
"""),
 dict(slug="search-term-cleaning", date="2026-08", kicker="Google Ads",
  title="Search term cleaning: why structure beats clever ad copy",
  teaser="On a three-month lead campaign, the biggest gains did not come from new ads. They came from what I excluded.",
  lead="When a Google Ads campaign underperforms, the reflex is to rewrite the ads. On a three-month lead generation campaign I learned that the account structure and the negative keyword list decide more than any headline.",
  body="""
<h2>The situation</h2>
<p>The goal was to generate leads via Google Ads Search. I set up the account from scratch: keyword clusters by intent, match types chosen per cluster, extensions on every ad group, and a negative keyword list from day one.</p>
<h2>What the search terms showed</h2>
<p>After the first week, the search term report told the real story. A meaningful share of clicks came from queries that were related to the offer but never converted: comparison searches, job seekers, people looking for something we did not sell. They cost the same per click as the good ones.</p>
<ul>
<li>Weekly search term review, every single week – not "when there is time".</li>
<li>Every non-converting query pattern went straight into the negative list.</li>
<li>Match types were tightened where broad matching brought volume but no leads.</li>
</ul>
<h2>The result</h2>
<p>Over three months the campaign delivered a 13.91 % CTR at an average CPC of CHF 1.35, with 19 qualified leads. More importantly, the offer-led campaign generated almost twice the leads of the audience-led one – a direct effect of matching the ad to a concrete need instead of a broad target group.</p>
<div class="box"><p>A clear account structure and consistent search term cleaning do more for lead quality than any single ad.</p></div>
<p>[Optional: add the industry benchmark and cost per lead for context.]</p>
"""),
 dict(slug="landing-page-user-journey", date="2026-07", kicker="Web & UX",
  title="One message per section: how I structure a landing page",
  teaser="Before I open WordPress, I write the page as a list of decisions the visitor has to make. The layout follows from that.",
  lead="A landing page is not a shorter website. It is a single path from a promise to one action. Here is the structure I use before I build anything in WordPress and Elementor.",
  body="""
<h2>Start with the user journey, not the sections</h2>
<p>I write down what the visitor needs to know, in the order they need to know it: What is this? Is it for me? Why should I trust it? What happens next? Every section on the page answers exactly one of these questions – and nothing else.</p>
<h2>My checklist</h2>
<ul>
<li><b>One CTA, repeated.</b> The same call to action above the fold, after the benefits and at the end. Different wording, same destination.</li>
<li><b>Mobile first, literally.</b> I build the mobile view first in Elementor. If the hierarchy works on a phone, the desktop version is easy. The reverse is never true.</li>
<li><b>Headlines carry the argument.</b> Someone who only reads the headlines should still understand the offer. Body text is for those who want more.</li>
<li><b>QA before launch, tracking before QA.</b> Conversion events are set up and tested before the page goes live, otherwise the first weeks of data are lost.</li>
</ul>
<div class="box"><p>A clear structure and unambiguous CTAs do more for the user journey than any single design element.</p></div>
<h2>Why the UX/UI training changed this</h2>
<p>My UX/UI training in 2026 sharpened one habit: hierarchy first, then copy, then the visual layer. It sounds obvious, but most landing pages I see are built in the opposite order.</p>
<p>[Optional: add the conversion rate or lead numbers from the landing page project.]</p>
"""),
 dict(slug="building-a-channel-from-zero", date="2026-10", kicker="Organic & content",
  embeds=[("tiktok", "7646032640209980705", "Jedes Mal so", "78'700 views", "tt-7646032640209980705.jpg"),
          ("tiktok", "7636122744475700513", "Kurz wie ein Profi f\u00fchlen", "44'900 views", "tt-7636122744475700513.jpg"),
          ("tiktok", "7624939783181159713", "Was sind eure Essentials?", "12'500 views", "tt-7624939783181159713.jpg")],
  title="Building a channel from zero, with no budget and no brief",
  teaser=PH("One sentence: the thing you learned that a paid campaign could never have taught you"),
  lead=PH("Two or three sentences: what you started, when, and the one constraint that shaped every decision - no media budget, no client, no existing audience"),
  body="""
<h2>Why I started it</h2>
<p>""" + PH("What made you start a road cycling channel next to the job. The honest reason, not the CV reason") + """</p>
<p>""" + PH("What the constraint actually meant in practice: no budget to buy reach, no brief to follow, no brand to hide behind") + """</p>

<h2>Choosing the angle</h2>
<p>""" + PH("The positioning decision and why. Your bio says beginner, small steps, honest fails - in a niche where most accounts show peak performance. Why that direction, and what you expected it to do") + """</p>
<p>""" + PH("What you decided NOT to do, and why. The rejected options say as much as the chosen one") + """</p>

<h2>What I tested</h2>
<ul>
<li>""" + PH("Format: what you tried, on which platform, and what the signal was") + """</li>
<li>""" + PH("Hooks: which openings held attention and which died in the first seconds") + """</li>
<li>""" + PH("Rhythm: how often you post, and what changed when you changed that") + """</li>
</ul>
<p>""" + PH("One thing that clearly failed. This is the most useful paragraph in the whole post - keep it concrete") + """</p>

<div class="box"><p>""" + PH("The one sentence you would keep if the rest were deleted") + """</p></div>

<h2>What came of it</h2>
<div class="results">
<div class="label">TikTok · """ + SOCIAL_ASOF + """</div>
<div class="nums">
<div><div class="n">191'181</div><div class="l">Views across 27 posts</div></div>
<div><div class="n hi">78'700</div><div class="l">Best performing post</div></div>
<div><div class="n">390</div><div class="l">Followers</div></div>
<div><div class="n">CHF 0</div><div class="l">Media budget</div></div>
</div>
</div>
<p class="figure-note">Figures read from the public profile on """ + SOCIAL_ASOF + """ – check and update them before publishing. The three strongest posts:
<a href="https://www.tiktok.com/@skiavelo/video/7646032640209980705" target="_blank" rel="noopener">78.7K</a> ·
<a href="https://www.tiktok.com/@skiavelo/video/7636122744475700513" target="_blank" rel="noopener">44.9K</a> ·
<a href="https://www.tiktok.com/@skiavelo/video/7624939783181159713" target="_blank" rel="noopener">12.5K</a></p>
<p>""" + PH("The honest reading of those numbers. Two posts carry most of the views - what was different about them, and what happens on a normal day") + """</p>

<h2>What it gives back to client work</h2>
<p>""" + PH("The transfer. What running your own channel changed about how you brief, test or judge content for clients. This is the paragraph a hiring manager reads") + """</p>
"""),
]

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
