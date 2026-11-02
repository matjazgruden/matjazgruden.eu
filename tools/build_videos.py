#!/usr/bin/env python3
"""Build videos.html (English) and sl/video.html (Slovenian) from the VIDEOS list below.

To add a video: add an entry to VIDEOS, then run from the repository root:
    python3 tools/build_videos.py

Videos are embedded from YouTube (privacy-enhanced youtube-nocookie.com), Vimeo (dnt=1)
or Arnes Video; nothing is hosted on the site itself.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://matjazgruden.eu"

MONTHS_SL = ["januarja", "februarja", "marca", "aprila", "maja", "junija", "julija",
             "avgusta", "septembra", "oktobra", "novembra", "decembra"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August",
             "September", "October", "November", "December"]

# Newest first. date: YYYY-MM-DD or YYYY-MM. source: youtube | vimeo | arnes (embed = full iframe src).
VIDEOS = [
    dict(date="2025-11-18", source="arnes", id="tm98mqtkb7d8",
         embed="https://video.arnes.si/embed/tm98mqtkb7d8", watch="https://video.arnes.si/en/watch/tm98mqtkb7d8",
         title="The Way Forward",
         occ_en="Speech, “The Way Forward”, closing conference of the European Year of Digital Citizenship Education 2025",
         occ_sl="Govor, »The Way Forward«, zaključna konferenca evropskega leta izobraževanja za digitalno državljanstvo 2025",
         place_en="Ljubljana, Slovenia", place_sl="Ljubljana",
         text="speeches/2025/european-year-of-digital-citizenship-education.html"),
    dict(date="2024-09-24", source="youtube", id="e-AiKbFBtxQ",
         title="Young People, Democracy and Climate Action",
         occ_en="Opening speech, Symposium “Young people, democracy and climate action”, EU–Council of Europe Youth Partnership",
         occ_sl="Uvodni govor, simpozij »Mladi, demokracija in podnebno ukrepanje«, mladinsko partnerstvo EU in Sveta Evrope",
         place_en="European Youth Centre, Strasbourg", place_sl="Evropski mladinski center, Strasbourg",
         text="speeches/2024/young-people-democracy-and-climate-action.html"),
    dict(date="2024-04", source="vimeo", id="949863692",
         title="No Culture, No Democracy",
         occ_en="Talk at The Other Session, marking 70 years of the European Cultural Convention, during the opening of the Venice Biennale",
         occ_sl="Nastop na dogodku The Other Session ob 70-letnici Evropske kulturne konvencije, med odprtjem beneškega bienala",
         place_en="Docks Cucchini, Venice", place_sl="Docks Cucchini, Benetke"),
    dict(date="2022-09-22", source="youtube", id="64gpqZg-evo",
         title="Navigating Transitions",
         occ_en="Opening speech, Symposium “Navigating transitions: adapting policies to young people’s changing realities”, EU–Council of Europe Youth Partnership",
         occ_sl="Uvodni govor, simpozij »Navigating transitions« o prilagajanju politik spreminjajoči se stvarnosti mladih, mladinsko partnerstvo EU in Sveta Evrope",
         place_en="", place_sl=""),
    dict(date="2019-11-28", source="youtube", id="GHkf2jLDrD0",
         title="Edu4Europe",
         occ_en="Opening speech, Edu4Europe, EU–Council of Europe Youth Partnership",
         occ_sl="Uvodni govor, Edu4Europe, mladinsko partnerstvo EU in Sveta Evrope",
         place_en="", place_sl=""),
    dict(date="2017-10-16", source="youtube", id="MTmsD_0lDnU",
         title="The Ups and Downs of Liberal Democracy: Will History Ever End?",
         occ_en="Talk, seminar of the Moscow School of Civic Education",
         occ_sl="Nastop, seminar Moskovske šole državljanske vzgoje",
         place_en="Warsaw", place_sl="Varšava"),
]

def fmt_date(d, lang):
    parts = [int(x) for x in d.split("-")]
    if lang == "en":
        return (f"{parts[2]} " if len(parts) > 2 else "") + f"{MONTHS_EN[parts[1]-1]} {parts[0]}"
    if len(parts) > 2:
        return f"{parts[2]}. {MONTHS_SL[parts[1]-1]} {parts[0]}"
    return f"{['januar','februar','marec','april','maj','junij','julij','avgust','september','oktober','november','december'][parts[1]-1]} {parts[0]}"

def embed_src(v):
    if v["source"] == "youtube":
        return f"https://www.youtube-nocookie.com/embed/{v['id']}?rel=0"
    if v["source"] == "vimeo":
        return f"https://player.vimeo.com/video/{v['id']}?dnt=1"
    return v["embed"]

def watch_url(v):
    if v["source"] == "youtube":
        return f"https://www.youtube.com/watch?v={v['id']}"
    if v["source"] == "vimeo":
        return f"https://vimeo.com/{v['id']}"
    return v["watch"]

SOURCE_NAME = {"youtube": "YouTube", "vimeo": "Vimeo", "arnes": "Arnes Video"}

def player(v, title):
    e = html.escape
    return (f'<div class="vid"><iframe src="{e(embed_src(v))}" title="{e(title)}" loading="lazy" '
            f'allow="fullscreen; picture-in-picture; encrypted-media" allowfullscreen '
            f'referrerpolicy="strict-origin-when-cross-origin"></iframe></div>')

def item(v, lang, prefix):
    e = html.escape
    when = f'<time datetime="{v["date"]}">{fmt_date(v["date"], lang)}</time>'
    place = v["place_en" if lang == "en" else "place_sl"]
    if place:
        when += f'<span class="sep">·</span>{e(place)}'
    links = [f'<a href="{e(watch_url(v))}">{"Watch on" if lang == "en" else "Oglejte si na"} {SOURCE_NAME[v["source"]]}</a>']
    if v.get("text"):
        links.insert(0, f'<a href="{prefix}{v["text"]}">{"Read the text" if lang == "en" else "Preberite besedilo"}</a>')
    joined = '<span class="sep">·</span>'.join(links)
    return (f'<li><h3 class="t">{e(v["title"])}</h3>'
            f'<span class="occ">{e(v["occ_en" if lang == "en" else "occ_sl"])}</span>'
            f'<span class="when">{when}</span>'
            f'{player(v, v["title"])}'
            f'<p class="vlinks">{joined}</p></li>')

def body(lang, prefix):
    years = {}
    for v in VIDEOS:
        years.setdefault(v["date"][:4], []).append(v)
    out = []
    for y in sorted(years, reverse=True):
        out.append(f'<section class="yr"><h2>{y}</h2><ol class="list sp vids">'
                   + "".join(item(v, lang, prefix) for v in years[y]) + "</ol></section>")
    return '<div class="archive speeches">' + "".join(out) + "</div>"

def n_word(n, lang):
    if lang == "en":
        return f"{n} recordings"
    return f"{n} posnetkov" if n >= 5 else f"{n} posnetki"

def page(lang):
    n = len(VIDEOS)
    if lang == "en":
        title, url, alt, prefix = "Videos", f"{SITE}/videos.html", f"{SITE}/sl/video.html", ""
        desc = (f"{n_word(n, 'en').capitalize()} of speeches and talks by Matjaž Gruden, most from his time "
                "as Director for Democracy at the Council of Europe. Where the text is published on this site, "
                "it is linked below the video.")
        nav = ('<nav aria-label="Main"><a href="index.html">Home</a><a href="archive.html">Archive</a>'
               '<a href="speeches.html">Speeches</a><a href="videos.html" aria-current="page">Videos</a>'
               '<a href="search.html">Search</a><a href="about.html">About</a>'
               '<a class="lang" href="sl/video.html" hreflang="sl">Slovensko</a></nav>')
        home, css, feed, locale = "index.html", "assets/site.css", f"{SITE}/feed.xml", "en_GB"
        foot = ('<p>© Matjaž Gruden. The columns were first published in Slovenian in the daily Večer.</p>\n'
                '<p class="follow"><a href="subscribe.html">Follow new texts (RSS or email)</a></p>')
        js, skip = "assets/site.js", "Skip to content"
    else:
        title, url, alt, prefix = "Video", f"{SITE}/sl/video.html", f"{SITE}/videos.html", "../"
        desc = (f"{n_word(n, 'sl').capitalize()} govorov in nastopov Matjaža Grudna, večinoma iz časa, ko je bil "
                "direktor za demokracijo pri Svetu Evrope. Govori so v izvirnem jeziku (večinoma v angleščini); "
                "kjer je besedilo objavljeno na tej strani, je povezava pod posnetkom.")
        nav = ('<nav aria-label="Glavni meni"><a href="../sl/index.html">Domov</a><a href="../sl/arhiv.html">Arhiv</a>'
               '<a href="../sl/govori.html">Govori</a><a href="../sl/video.html" aria-current="page">Video</a>'
               '<a href="../sl/iskanje.html">Iskanje</a><a href="../sl/o-avtorju.html">O avtorju</a>'
               '<a class="lang" href="../videos.html" hreflang="en">English</a></nav>')
        home, css, feed, locale = "../sl/index.html", "../assets/site.css", f"{SITE}/sl/feed.xml", "sl_SI"
        foot = ('<p>© Matjaž Gruden. Kolumne so bile prvič objavljene v časniku Večer.</p>\n'
                '<p class="follow"><a href="../sl/spremljanje.html">Spremljajte nova besedila (RSS ali e-pošta)</a></p>')
        js, skip = "../assets/site.js", "Skip to content"
    e = html.escape
    other = "sl" if lang == "en" else "en"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | Matjaž Gruden</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="{other}" href="{alt}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title} | Matjaž Gruden">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Matjaž Gruden">
<meta property="og:image" content="{SITE}/assets/share-5.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:locale" content="{locale}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&family=Schibsted+Grotesk:wght@400;500;600&display=swap">
<link rel="alternate" type="application/rss+xml" title="Matjaž Gruden" href="{feed}">
<link rel="stylesheet" href="{css}">
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<header class="site"><div class="wrap bar">
<a class="name" href="{home}">Matjaž Gruden</a>
{nav}
</div></header>
<main id="main" class="wrap">
<h1 class="pt">{title}</h1><p class="lede">{e(desc)}</p>
{body(lang, prefix)}
</main>
<footer class="site"><div class="wrap">
{foot}
</div></footer>
<script src="{js}" defer></script>
</body>
</html>
"""

if __name__ == "__main__":
    (ROOT / "videos.html").write_text(page("en"), encoding="utf-8")
    (ROOT / "sl" / "video.html").write_text(page("sl"), encoding="utf-8")
    print(f"Wrote videos.html and sl/video.html ({len(VIDEOS)} videos)")
