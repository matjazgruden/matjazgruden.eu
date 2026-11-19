#!/usr/bin/env python3
"""Build the Media section: media.html (English), sl/mediji.html (Slovenian) and,
for each appearance with a transcript, an English and a Slovenian transcript page.

To add an appearance: add an entry to MEDIA below. For a transcript, put two text files
in tools/media/ named <slug>.sl.txt and <slug>.en.txt, one paragraph per block,
each starting with "H:" (interviewer) or "G:" (Matjaž Gruden). Then run from the
repository root:
    python3 tools/build_media.py

Recordings are linked or played from the broadcaster's own servers; nothing is hosted here.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://matjazgruden.eu"
TXT = ROOT / "tools" / "media"

MONTHS_SL = ["januarja", "februarja", "marca", "aprila", "maja", "junija", "julija",
             "avgusta", "septembra", "oktobra", "novembra", "decembra"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August",
             "September", "October", "November", "December"]

KIND = {"radio": ("Radio", "Radio"), "podcast": ("Podcast", "Podkast"), "tv": ("Television", "Televizija")}

# Newest first.
MEDIA = [
    dict(slug="2026-11-19-val202-vroci-mikrofon", path="2026/val-202-vroci-mikrofon",
         date="2026-11-19", kind="radio", minutes=47,
         outlet_en="Vroči mikrofon (“Hot Mic”), Val 202, RTV Slovenija",
         outlet_sl="Vroči mikrofon, Val 202, RTV Slovenija",
         host="Gašper Andrinek",
         title_en="“The generation that is protesting has lived its whole life in one crisis after another”",
         title_sl="»Generacija, ki protestira, že celo življenje živi v različnih krizah«",
         sum_en=("A conversation on the state of democracy in Europe. Democracy is not a weak model, but a "
                 "fragile one, and we have treated it for too long as if it would survive whatever we did to it. "
                 "Why the young people protesting across Europe are right to be angry, what the students’ victory "
                 "in Serbia means for the EU, why security for democracy is not enough without security through "
                 "democracy, what Putin is really after, and why the fate of the UN and the Council of Europe is "
                 "not someone else’s business."),
         sum_sl=("Pogovor o stanju demokracije v Evropi. Demokracija ni šibak, je pa krhek model, mi pa smo "
                 "predolgo ravnali, kot da bo preživela ne glede na to, kaj počnemo z njo. Zakaj so mladi, ki "
                 "protestirajo po Evropi, upravičeno jezni, kaj zmaga študentov v Srbiji pomeni za EU, zakaj "
                 "varnost za demokracijo ni dovolj brez varnosti skozi demokracijo, za kaj v resnici gre Putinu "
                 "in zakaj usoda OZN in Sveta Evrope ni stvar nekoga drugega."),
         listen="https://val202.rtvslo.si/podkast/vroci-mikrofon/584/175266035",
         audio="https://dts.podtrac.com/redirect.mp3/videoweb.rtvslo.si/podcast/ava_archive11/2026/11/19/MatjaGRA_SLO_LJT_11756209_22869587.mp3",
         listen_name="Val 202",
         image="assets/media/val202-2026-11-19", image_w=(600, 947), image_ratio=(947, 613),
         credit_en="Photo: Val 202 / RTV Slovenija", credit_sl="Foto: Val 202 / RTV Slovenija"),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&family=Schibsted+Grotesk:wght@400;500;600&display=swap">')


def fmt_date(d, lang):
    y, m, day = [int(x) for x in d.split("-")]
    return f"{day} {MONTHS_EN[m-1]} {y}" if lang == "en" else f"{day}. {MONTHS_SL[m-1]} {y}"


def nav(lang, up, current, alt):
    """up: relative prefix to site root; current: 'media' or ''; alt: path of the other-language page."""
    if lang == "en":
        cur = ' aria-current="page"' if current == "media" else ""
        return (f'<nav aria-label="Main"><a href="{up}index.html">Home</a><a href="{up}archive.html">Archive</a>'
                f'<a href="{up}speeches.html">Speeches</a><a href="{up}videos.html">Videos</a>'
                f'<a href="{up}media.html"{cur}>Media</a>'
                f'<a href="{up}search.html">Search</a><a href="{up}about.html">About</a>'
                f'<a class="lang" href="{up}{alt}" hreflang="sl">Slovensko</a></nav>')
    cur = ' aria-current="page"' if current == "media" else ""
    return (f'<nav aria-label="Glavni meni"><a href="{up}sl/index.html">Domov</a><a href="{up}sl/arhiv.html">Arhiv</a>'
            f'<a href="{up}sl/govori.html">Govori</a><a href="{up}sl/video.html">Video</a>'
            f'<a href="{up}sl/mediji.html"{cur}>Mediji</a>'
            f'<a href="{up}sl/iskanje.html">Iskanje</a><a href="{up}sl/o-avtorju.html">O avtorju</a>'
            f'<a class="lang" href="{up}{alt}" hreflang="en">English</a></nav>')


def shell(lang, up, title, desc, url, alt_url, nav_html, main, og_type="website"):
    e = html.escape
    other = "sl" if lang == "en" else "en"
    home = f"{up}index.html" if lang == "en" else f"{up}sl/index.html"
    feed = f"{SITE}/feed.xml" if lang == "en" else f"{SITE}/sl/feed.xml"
    locale = "en_GB" if lang == "en" else "sl_SI"
    if lang == "en":
        foot = (f'<p>© Matjaž Gruden. The columns were first published in Slovenian.</p>\n'
                f'<p class="follow"><a href="{up}subscribe.html">Follow new texts (RSS or email)</a></p>')
    else:
        foot = (f'<p>© Matjaž Gruden. Kolumne so bile prvič objavljene v slovenščini.</p>\n'
                f'<p class="follow"><a href="{up}sl/spremljanje.html">Spremljajte nova besedila (RSS ali e-pošta)</a></p>')
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)} | Matjaž Gruden</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="{other}" href="{alt_url}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)} | Matjaž Gruden">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Matjaž Gruden">
<meta property="og:image" content="{SITE}/assets/share-5.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:locale" content="{locale}">
{FONTS}
<link rel="alternate" type="application/rss+xml" title="Matjaž Gruden" href="{feed}">
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap bar">
<a class="name" href="{home}">Matjaž Gruden</a>
{nav_html}
</div></header>
<main id="main" class="wrap">
{main}
</main>
<footer class="site"><div class="wrap">
{foot}
</div></footer>
<script src="{up}assets/site.js" defer></script>
</body>
</html>
"""


def figure(m, lang, up, sizes):
    if not m.get("image"):
        return ""
    e = html.escape
    w1, w2 = m["image_w"]
    W, H = m["image_ratio"]
    src = f'{up}{m["image"]}'
    credit = m["credit_en" if lang == "en" else "credit_sl"]
    alt = "Matjaž Gruden" 
    return (f'<figure class="mfig"><img src="{src}-{w2}.jpg" srcset="{src}-{w1}.jpg {w1}w, {src}-{w2}.jpg {w2}w" '
            f'sizes="{sizes}" width="{W}" height="{H}" alt="{alt}" loading="lazy" decoding="async">'
            f'<figcaption>{e(credit)}</figcaption></figure>')


def en_url(m):
    return f"media/{m['path']}.html"


def sl_url(m):
    return f"sl/mediji/{m['path']}.html"


def has_transcript(m):
    return (TXT / f"{m['slug']}.sl.txt").exists() and (TXT / f"{m['slug']}.en.txt").exists()


def card(m, lang, up):
    e = html.escape
    en = lang == "en"
    kind = KIND[m["kind"]][0 if en else 1]
    meta = (f'{kind}<span class="sep">·</span><time datetime="{m["date"]}">{fmt_date(m["date"], lang)}</time>'
            f'<span class="sep">·</span>{m["minutes"]} min')
    if en:
        meta += '<span class="sep">·</span><span class="lang-tag">In Slovenian</span>'
    host = (f'<span class="when">{"Interviewer" if en else "Pogovor vodi"}: {e(m["host"])}</span>' if m.get("host") else "")
    links = []
    if has_transcript(m):
        if en:
            links.append(f'<a href="{up}{en_url(m)}">Read the English transcript</a>')
        else:
            links.append(f'<a href="{up}{sl_url(m)}">Preberite prepis</a>')
    links.append(f'<a href="{e(m["listen"])}">{"Listen on" if en else "Poslušajte na"} {e(m["listen_name"])}</a>')
    audio = (f'<audio class="aud" controls preload="none" src="{e(m["audio"])}"></audio>' if m.get("audio") else "")
    return (f'<li><h3 class="t">{e(m["title_en" if en else "title_sl"])}</h3>'
            f'<span class="occ">{e(m["outlet_en" if en else "outlet_sl"])}</span>'
            f'<span class="when">{meta}</span>{host}'
            f'{figure(m, lang, up, "(max-width:760px) 100vw, 38rem")}'
            f'<p class="sum">{e(m["sum_en" if en else "sum_sl"])}</p>'
            f'{audio}'
            f'<p class="vlinks">{"<span class=sep>·</span>".join(links)}</p></li>')


def index_page(lang):
    en = lang == "en"
    up = "" if en else "../"
    years = {}
    for m in MEDIA:
        years.setdefault(m["date"][:4], []).append(m)
    body = "".join(f'<section class="yr"><h2>{y}</h2><ol class="list sp vids media">'
                   + "".join(card(m, lang, up) for m in years[y]) + "</ol></section>"
                   for y in sorted(years, reverse=True))
    if en:
        title = "Media"
        desc = ("Interviews and conversations with Matjaž Gruden on radio, television and podcasts. "
                "Most are in Slovenian; each comes with an English summary, and where available a full "
                "English transcript.")
        url, alt = f"{SITE}/media.html", f"{SITE}/sl/mediji.html"
    else:
        title = "Mediji"
        desc = "Intervjuji in pogovori z Matjažem Grudnom na radiu, televiziji in v podkastih."
        url, alt = f"{SITE}/sl/mediji.html", f"{SITE}/media.html"
    main = (f'<h1 class="pt">{title}</h1><p class="lede">{html.escape(desc)}</p>\n'
            f'<div class="archive speeches">{body}</div>')
    return shell(lang, up, title, desc, url, alt,
                 nav(lang, up, "media", "sl/mediji.html" if en else "media.html"), main)


def paragraphs(m, lang):
    raw = (TXT / f"{m['slug']}.{lang}.txt").read_text(encoding="utf-8").strip()
    names = {"H": m["host"], "G": "Matjaž Gruden"}
    out, prev = [], None
    for block in [b.strip() for b in raw.split("\n\n") if b.strip()]:
        who, text = block.split(":", 1)
        who = who.strip()
        text = html.escape(text.strip())
        cls = "q" if who == "H" else "a"
        label = f'<strong class="spk">{html.escape(names[who])}:</strong> ' if who != prev else ""
        out.append(f'<p class="{cls}">{label}{text}</p>')
        prev = who
    return "\n".join(out)


def transcript_page(m, lang):
    e = html.escape
    en = lang == "en"
    up = "../../" if en else "../../../"
    title = m["title_en" if en else "title_sl"].strip("“”»«")
    kind = KIND[m["kind"]][0 if en else 1]
    meta = (f'<time datetime="{m["date"]}">{fmt_date(m["date"], lang)}</time><span class="sep">·</span>'
            f'{kind}<span class="sep">·</span>{m["minutes"]} min')
    if en:
        notes = (f'<p class="translation"><a href="{up}{sl_url(m)}" hreflang="sl">Slovenian transcript</a>'
                 f'<span class="sep">·</span><a href="{e(m["listen"])}">Listen on {e(m["listen_name"])} (in Slovenian)</a></p>'
                 '<p class="ai-note">The interview was conducted in Slovenian. This is a lightly edited transcript, '
                 'translated with the help of AI. Repetitions and fillers have been removed; […] marks a passage missing '
                 'from the transcript and [?] a word that was unclear in the recording.</p>')
        kicker = f'<p class="kicker"><a href="{up}media.html">Media</a></p>'
        desc = m["sum_en"]
        url, alt = f"{SITE}/{en_url(m)}", f"{SITE}/{sl_url(m)}"
        alt_rel = sl_url(m)
    else:
        notes = (f'<p class="translation"><a href="{e(m["listen"])}">Poslušajte na {e(m["listen_name"])}</a>'
                 f'<span class="sep">·</span><a href="{up}{en_url(m)}" hreflang="en">English translation</a></p>'
                 '<p class="ai-note">Prepis je rahlo urejen za branje: ponavljanja in mašila so odstranjena; […] označuje '
                 'del, ki v prepisu manjka, [?] pa besedo, ki na posnetku ni bila razločna.</p>')
        kicker = f'<p class="kicker"><a href="{up}sl/mediji.html">Mediji</a></p>'
        desc = m["sum_sl"]
        url, alt = f"{SITE}/{sl_url(m)}", f"{SITE}/{en_url(m)}"
        alt_rel = en_url(m)
    audio = (f'<audio class="aud" controls preload="none" src="{e(m["audio"])}"></audio>' if m.get("audio") else "")
    main = (f'<article class="piece transcript">\n<header>{kicker}<h1>{e(title)}</h1>'
            f'<p class="occ">{e(m["outlet_en" if en else "outlet_sl"])}</p>'
            f'<p class="meta">{meta}</p>{notes}{figure(m, lang, up, "(max-width:760px) 100vw, 38rem")}{audio}</header>\n'
            f'<div class="prose">\n{paragraphs(m, lang)}\n</div>\n</article>')
    return shell(lang, up, title, desc, url, alt, nav(lang, up, "media", alt_rel), main, og_type="article")


if __name__ == "__main__":
    (ROOT / "media.html").write_text(index_page("en"), encoding="utf-8")
    (ROOT / "sl" / "mediji.html").write_text(index_page("sl"), encoding="utf-8")
    n = 0
    for m in MEDIA:
        if has_transcript(m):
            for lang, rel in (("en", en_url(m)), ("sl", sl_url(m))):
                p = ROOT / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(transcript_page(m, lang), encoding="utf-8")
            n += 1
    print(f"Wrote media.html, sl/mediji.html and {n} transcript(s) in two languages")
