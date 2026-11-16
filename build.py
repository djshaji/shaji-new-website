#!/usr/bin/env python3
"""Render the portfolio Markdown into a buildless Bootstrap website."""

from html import escape
from pathlib import Path
import re
import shutil

from markdown_it import MarkdownIt
import yaml


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
MARKDOWN = MarkdownIt("commonmark", {"html": False}).enable("table")
PALETTES = ("slate", "ocean", "forest", "rose", "warm")


def icon(name):
    return f'<i data-lucide="{escape(name)}" aria-hidden="true"></i>'


def read_page(path):
    _, frontmatter, markdown = path.read_text(encoding="utf-8").split("---\n", 2)
    page = yaml.safe_load(frontmatter)
    page["slug"] = path.stem
    page["href"] = f"{path.stem}.html"
    body = MARKDOWN.render(markdown.lstrip())
    body = re.sub(r'(href=")((?:\./)?[\w-]+)\.md(?=["?#])', r'\1\2.html', body)
    page["body"] = body
    return page


def destination_links(links, css_class, arrow):
    return "".join(
        f'<a class="{css_class}" href="{escape(url)}">{escape(label)}{icon(arrow)}</a>'
        for label, url in links.items()
    )


def home_main(page, pages, site):
    cards = "".join(
        f'''<div class="col">
          <a class="section-card tone-{p["slug"]}" href="{p["href"]}">
            <span class="card-icon">{icon(p["icon"])}</span>
            <span class="card-arrow">{icon("arrow-up-right")}</span>
            <h3>{escape(p["title"])}</h3>
            <p>{escape(p["teaser"])}</p>
          </a>
        </div>'''
        for p in pages if p["slug"] != "index"
    )
    return f'''<section class="home-hero" aria-labelledby="page-title">
      <div class="row g-0 align-items-stretch">
        <div class="col-lg-7 hero-copy">
          <p class="location">{icon("map-pin")} {escape(site["location"])}</p>
          <h1 id="page-title">{escape(site["name"])}<span class="name-period">.</span></h1>
          <p class="hero-subtitle">{escape(page["subtitle"])}</p>
          <p class="intro">{escape(page["description"])}</p>
          <a class="primary-link" href="#explore">Explore my work {icon("arrow-down-right")}</a>
        </div>
        <div class="col-lg-5 hero-media" aria-hidden="true">
          <span class="media-orbit orbit-a"></span><span class="media-orbit orbit-b"></span>
          <span class="media-orbit orbit-c"></span>
          {hero_image()}
        </div>
      </div>
    </section>
    <section id="explore" class="explore" aria-labelledby="explore-heading">
      <div class="section-heading"><h2 id="explore-heading">Explore</h2><span></span></div>
      <div class="row row-cols-1 row-cols-sm-2 row-cols-xl-4 g-3">{cards}</div>
    </section>
    <section id="about" class="about markdown-body" aria-label="About and contact">
      {page["body"]}
    </section>'''


def hero_image():
    for suffix in ("webp", "jpg", "png"):
        asset = f"editorial-cover.{suffix}"
        if (ROOT / "assets" / asset).is_file():
            return f'<img src="assets/{asset}" width="1536" height="1024" alt="" fetchpriority="high">'
    return ""


def topic_main(page):
    facts = "".join(
        f"<div><dt>{escape(label)}</dt><dd>{escape(value)}</dd></div>"
        for label, value in page.get("facts", {}).items()
    )
    links = destination_links(page.get("links", {}), "external-link", "arrow-up-right")
    links_panel = f'<div class="sidebar-links"><h2>Links</h2>{links}</div>' if links else ""
    return f'''<section class="topic-hero tone-{page["slug"]}" aria-labelledby="page-title">
      <div class="topic-copy">
        <h1 id="page-title">{escape(page["title"])}</h1>
        <p class="hero-subtitle">{escape(page["subtitle"])}</p>
        <p class="intro">{escape(page["description"])}</p>
      </div>
      <div class="topic-art" aria-hidden="true"><span>{icon(page["icon"])}</span></div>
    </section>
    <div class="row topic-content">
      <article class="col-lg-8 markdown-body">{page["body"]}</article>
      <aside class="col-lg-4 topic-sidebar" aria-label="At a glance">
        <div class="sidebar-card"><h2>At a glance</h2><dl>{facts}</dl>{links_panel}</div>
      </aside>
    </div>'''


def render(page, pages, site):
    is_home = page["slug"] == "index"
    name = escape(site["name"])
    title = name if is_home else f'{escape(page["title"])} · {name}'
    nav = []
    for item in pages:
        current = ' aria-current="page"' if item is page else ""
        label = escape(item.get("label", item["title"]))
        nav.append(f'<li class="nav-item"><a class="nav-link" href="{item["href"]}"{current}>{label}</a></li>')
    options = "".join(f'<option value="{key}">{key.title()}</option>' for key in PALETTES)
    footer_links = destination_links(site["links"], "footer-link", "arrow-up-right")
    main = home_main(page, pages, site) if is_home else topic_main(page)
    return f'''<!doctype html>
<html lang="en" data-bs-theme="{site["mode"]}" data-palette="{site["theme"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(page["description"])}">
  <title>{title}</title>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/vendor/bootstrap.min.css">
  <link rel="stylesheet" href="assets/site.css">
  <script>
    try {{
      const mode = localStorage.getItem('sk-appearance');
      const palette = localStorage.getItem('sk-palette');
      if (['light', 'dark'].includes(mode)) document.documentElement.dataset.bsTheme = mode;
      if (['slate', 'ocean', 'forest', 'rose', 'warm'].includes(palette)) document.documentElement.dataset.palette = palette;
    }} catch {{}}
  </script>
  <script defer src="assets/vendor/bootstrap.bundle.min.js"></script>
  <script defer src="assets/vendor/lucide.min.js"></script>
  <script defer src="assets/site.js"></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <nav class="navbar navbar-expand-lg" aria-label="Main navigation">
    <div class="container site-width">
      <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">SK</span>{name}</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#site-nav"
        aria-controls="site-nav" aria-expanded="false" aria-label="Toggle navigation">{icon("menu")}</button>
      <div class="collapse navbar-collapse" id="site-nav">
        <ul class="navbar-nav mx-lg-auto">{''.join(nav)}</ul>
        <div class="appearance">
          <label class="visually-hidden" for="palette-select">Colour theme</label>
          <select id="palette-select" class="form-select form-select-sm">{options}</select>
          <button id="mode-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false">{icon("sun-moon")}</button>
        </div>
      </div>
    </div>
  </nav>
</header>
<main id="main" class="container site-width" tabindex="-1">{main}</main>
<footer class="site-footer">
  <div class="container site-width">
    <span class="footer-name">{name}<span> · {escape(site["location"])}</span></span>
    <nav aria-label="External profiles">{footer_links}</nav>
  </div>
</footer>
</body>
</html>
'''


def build():
    site = yaml.safe_load((ROOT / "site.yaml").read_text(encoding="utf-8"))
    if site["theme"] not in PALETTES or site["mode"] not in ("light", "dark"):
        raise ValueError("Invalid theme or mode in site.yaml")
    pages = sorted(
        (read_page(path) for path in (ROOT / "content").glob("*.md")),
        key=lambda page: page["order"],
    )
    if not any(page["slug"] == "index" for page in pages):
        raise ValueError("content/index.md is required")
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "assets", DIST / "assets")
    for page in pages:
        (DIST / page["href"]).write_text(render(page, pages, site), encoding="utf-8")
    print(f"Built {len(pages)} pages in {DIST}")


if __name__ == "__main__":
    build()
