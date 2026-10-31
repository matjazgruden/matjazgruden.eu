#!/usr/bin/env python3
"""Rebuild feed.xml (English) and sl/feed.xml (Slovenian) from the site's pages.

Run from the repository root after adding a new piece:  python3 tools/build_feeds.py
The newsletter service watches these feeds and emails subscribers when a new item appears.
"""
import glob, html, re, sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://matjazgruden.eu"
LIMIT = 30

FEEDS = {
    "en": dict(out="feed.xml", globs=["columns/**/*.html", "speeches/**/*.html"],
               title="Matjaž Gruden", lang="en",
               desc="Columns and speeches by Matjaž Gruden on democracy, Europe and Slovenia.",
               home=SITE + "/"),
    "sl": dict(out="sl/feed.xml", globs=["sl/clanki/**/*.html", "speeches/**/*.html"],
               title="Matjaž Gruden", lang="sl",
               desc="Kolumne in govori Matjaža Grudna o demokraciji, Evropi in Sloveniji.",
               home=SITE + "/sl/index.html"),
}

def meta(src, pattern):
    m = re.search(pattern, src, re.S)
    return html.unescape(m.group(1)).strip() if m else None

def parse_date(s):
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(s, fmt).replace(hour=8, tzinfo=timezone.utc)
        except ValueError:
            pass
    return None

def items_for(globs):
    items = []
    for g in globs:
        for f in glob.glob(str(ROOT / g), recursive=True):
            src = Path(f).read_text(encoding="utf-8")
            d = meta(src, r'<time datetime="([^"]+)"')
            url = meta(src, r'<link rel="canonical" href="([^"]+)"')
            title = meta(src, r"<h1[^>]*>(.*?)</h1>")
            if not (d and url and title):
                continue
            title = re.sub(r"<[^>]+>", "", title)
            items.append(dict(date=parse_date(d), url=url, title=title,
                              desc=meta(src, r'<meta name="description" content="([^"]*)"') or ""))
    items.sort(key=lambda i: (i["date"], i["url"]), reverse=True)
    return items[:LIMIT]

def esc(s):
    return html.escape(s, quote=False)

def build(cfg):
    items = items_for(cfg["globs"])
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">', "<channel>",
           f"<title>{esc(cfg['title'])}</title>", f"<link>{cfg['home']}</link>",
           f"<description>{esc(cfg['desc'])}</description>", f"<language>{cfg['lang']}</language>",
           f'<atom:link href="{SITE}/{cfg["out"]}" rel="self" type="application/rss+xml"/>',
           f"<lastBuildDate>{format_datetime(items[0]['date'])}</lastBuildDate>"]
    for i in items:
        out += ["<item>", f"<title>{esc(i['title'])}</title>", f"<link>{i['url']}</link>",
                f'<guid isPermaLink="true">{i["url"]}</guid>',
                f"<pubDate>{format_datetime(i['date'])}</pubDate>",
                f"<description>{esc(i['desc'])}</description>", "</item>"]
    out += ["</channel>", "</rss>", ""]
    (ROOT / cfg["out"]).write_text("\n".join(out), encoding="utf-8")
    print(f"{cfg['out']}: {len(items)} items, newest: {items[0]['title']} ({items[0]['date']:%Y-%m-%d})")

if __name__ == "__main__":
    for cfg in FEEDS.values():
        build(cfg)
