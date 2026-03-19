#!/usr/bin/env python3
"""
build_blog.py — Blog build script for rushitnshah.com

Usage:
  python3 build_blog.py

Source:  blog/posts/src/YYYY-MM-DD-slug.md   (with YAML frontmatter)
Output:  blog/posts/YYYY-MM-DD-slug.html     (styled HTML pages)
Updates: blog/index.html                     (post listing)

Frontmatter keys: title, date, description
"""

import re
import markdown
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
REPO_ROOT  = Path(__file__).parent
SRC_DIR    = REPO_ROOT / "blog" / "posts" / "src"
OUT_DIR    = REPO_ROOT / "blog" / "posts"
INDEX_FILE = REPO_ROOT / "blog" / "index.html"

# ── Templates ──────────────────────────────────────────────────────────────
POST_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en-us" data-theme="light">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-4GLEB505RT"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', 'G-4GLEB505RT');
  </script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="Rushit N. Shah">
  <meta name="description" content="{description}">
  <link rel="icon" type="image/png" href="/img/icon.png">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" crossorigin="anonymous">
  <link rel="stylesheet" href="/styles.css">
  <title>{title} — Rushit N. Shah</title>
  <style>
    .post-header {{ margin-bottom: 2rem; }}
    .post-title  {{ font-family: var(--font-mono); font-size: 1.35rem; font-weight: 700;
                    letter-spacing: -0.02em; line-height: 1.3; margin-bottom: 0.3rem; }}
    .post-meta   {{ font-size: 0.82rem; color: var(--muted); font-family: var(--font-mono); }}
    .post-body   {{ font-size: 0.97rem; line-height: 1.78; max-width: 58ch; }}
    .post-body p  {{ margin-bottom: 1.1rem; }}
    .post-body h2 {{ font-family: var(--font-mono); font-size: 0.95rem; font-weight: 600;
                     margin: 1.8rem 0 0.6rem; color: var(--text); }}
    .post-body h3 {{ font-family: var(--font-mono); font-size: 0.85rem; font-weight: 600;
                     margin: 1.4rem 0 0.4rem; color: var(--muted); }}
    .post-body a  {{ color: var(--accent); text-decoration: none; }}
    .post-body a:hover {{ text-decoration: underline; }}
    .post-body code      {{ font-family: var(--font-mono); font-size: 0.88em;
                            background: var(--border); padding: 0.1em 0.35em; border-radius: 2px; }}
    .post-body pre       {{ background: var(--border); padding: 1rem; border-radius: 3px;
                            overflow-x: auto; margin-bottom: 1.1rem; }}
    .post-body pre code  {{ background: none; padding: 0; }}
    .post-body blockquote {{ border-left: 2px solid var(--accent); padding-left: 1rem;
                             color: var(--muted); margin-bottom: 1.1rem; }}
    .post-body ul, .post-body ol {{ padding-left: 1.4rem; margin-bottom: 1.1rem; }}
    .post-body li {{ margin-bottom: 0.25rem; }}
    .back-link {{ font-size: 0.82rem; color: var(--muted); text-decoration: none;
                  font-family: var(--font-mono); display: inline-block; margin-bottom: 2rem; }}
    .back-link:hover {{ color: var(--accent); }}
  </style>
</head>
<body>
<nav>
  <div class="nav-inner">
    <a class="nav-brand" href="/">Rushit N. Shah</a>
    <button class="nav-menu-btn" id="nav-menu-btn" aria-label="Open navigation"><i class="fa fa-bars"></i></button>
    <ul class="nav-links">
      <li><a href="/#news">News</a></li>
      <li><a href="/#experience">Experience</a></li>
      <li><a href="/#publications">Publications</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/#interests">Interests</a></li>
      <li><a href="/#contact">Contact</a></li>
      <li>
        <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
          <i class="fa fa-moon-o" id="toggle-icon"></i>
        </button>
      </li>
    </ul>
  </div>
</nav>
<main>
  <section>
    <a class="back-link" href="/blog/">← all posts</a>
    <div class="post-header">
      <div class="post-title">{title}</div>
      <div class="post-meta">{date_fmt}</div>
    </div>
    <div class="post-body">
{body}
    </div>
  </section>
</main>
<footer>
  <span>&copy; 2026 Rushit N. Shah</span>
  <a class="back-to-top" href="#top">↑ top</a>
</footer>
<script src="/js/site.js"></script>
</body>
</html>
"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en-us" data-theme="light">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-4GLEB505RT"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', 'G-4GLEB505RT');
  </script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="Rushit N. Shah">
  <meta name="description" content="Writing on ML, RL, and things I find interesting.">
  <link rel="icon" type="image/png" href="/img/icon.png">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" crossorigin="anonymous">
  <link rel="stylesheet" href="/styles.css">
  <title>Blog — Rushit N. Shah</title>
  <style>
    .blog-desc  {{ font-size: 0.97rem; color: var(--muted); margin-bottom: 2rem; max-width: 50ch; }}
    .post-list  {{ list-style: none; }}
    .post-entry {{ display: flex; gap: 1.5rem; align-items: baseline;
                   padding: 0.5rem 0; border-bottom: 1px solid var(--border); }}
    .post-entry:last-child {{ border-bottom: none; }}
    .post-date  {{ font-family: var(--font-mono); font-size: 0.78rem; color: var(--muted);
                   white-space: nowrap; width: 6.5rem; flex-shrink: 0; }}
    .post-info  {{ font-size: 0.92rem; }}
    .post-info a {{ color: var(--text); text-decoration: none; font-weight: 500; }}
    .post-info a:hover {{ color: var(--accent); }}
    .post-desc  {{ font-size: 0.85rem; color: var(--muted); margin-top: 0.1rem; }}
  </style>
</head>
<body>
<nav>
  <div class="nav-inner">
    <a class="nav-brand" href="/">Rushit N. Shah</a>
    <button class="nav-menu-btn" id="nav-menu-btn" aria-label="Open navigation"><i class="fa fa-bars"></i></button>
    <ul class="nav-links">
      <li><a href="/#news">News</a></li>
      <li><a href="/#experience">Experience</a></li>
      <li><a href="/#publications">Publications</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/#interests">Interests</a></li>
      <li><a href="/#contact">Contact</a></li>
      <li>
        <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
          <i class="fa fa-moon-o" id="toggle-icon"></i>
        </button>
      </li>
    </ul>
  </div>
</nav>
<main>
  <section>
    <h2 class="section-title">Blog</h2>
    <p class="blog-desc">Occasional writing on ML, RL, and things I find interesting.</p>
    <ul class="post-list">
{post_entries}
    </ul>
  </section>
</main>
<footer>
  <span>&copy; 2026 Rushit N. Shah</span>
  <a class="back-to-top" href="#top">↑ top</a>
</footer>
<script src="/js/site.js"></script>
</body>
</html>
"""

POST_ENTRY_TEMPLATE = """\
      <li class="post-entry">
        <span class="post-date">{date_fmt}</span>
        <div class="post-info">
          <a href="/blog/posts/{slug}.html">{title}</a>
          <div class="post-desc">{description}</div>
        </div>
      </li>"""

# ── Helpers ────────────────────────────────────────────────────────────────
def parse_frontmatter(text):
    """Parse YAML-style frontmatter delimited by ---."""
    meta, body = {}, text
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                key, _, val = line.partition(':')
                meta[key.strip()] = val.strip()
        body = m.group(2)
    return meta, body

def fmt_date(date_str):
    try:
        return datetime.strptime(str(date_str), "%Y-%m-%d").strftime("%b %d, %Y")
    except ValueError:
        return str(date_str)

# ── Build ──────────────────────────────────────────────────────────────────
def build():
    md_files = sorted(SRC_DIR.glob("*.md"), reverse=True)
    if not md_files:
        print("No markdown files found in", SRC_DIR)
        return

    posts = []
    for src in md_files:
        slug = src.stem
        meta, body_md = parse_frontmatter(src.read_text())
        title       = meta.get("title", slug)
        date_str    = meta.get("date", "")
        description = meta.get("description", "")
        date_fmt    = fmt_date(date_str)
        body_html   = markdown.markdown(body_md, extensions=["fenced_code", "tables"])

        html = POST_TEMPLATE.format(
            title=title, description=description,
            date_fmt=date_fmt, body=body_html
        )
        out_path = OUT_DIR / f"{slug}.html"
        out_path.write_text(html)
        print(f"  wrote {out_path.relative_to(REPO_ROOT)}")
        posts.append({"slug": slug, "title": title, "date_fmt": date_fmt, "description": description})

    entries = "\n".join(
        POST_ENTRY_TEMPLATE.format(**p) for p in posts
    )
    INDEX_FILE.write_text(INDEX_TEMPLATE.format(post_entries=entries))
    print(f"  wrote {INDEX_FILE.relative_to(REPO_ROOT)}")
    print(f"\nBuilt {len(posts)} post(s).")

if __name__ == "__main__":
    build()
