#!/usr/bin/env python3
"""
Serenity Reports — Build Script
Reads reports.json (single source of truth), then:
  1. Generates nav.js  (shared navigation injection script)
  2. Generates index.html  (card-based navigation homepage)
  3. Injects <script src="../nav.js"> into every .html file under html/  (idempotent)

Usage:
  python build.py          # full build
  python build.py --check  # dry-run: show what would change
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_DIR = ROOT / "html"
REPORTS_JSON = ROOT / "reports.json"
NAV_JS = ROOT / "nav.js"
INDEX_HTML = ROOT / "index.html"

# Category display config
CATEGORIES = {
    "company": {"label": "公司深度分析", "icon": "📈", "tag_class": "tag-analysis"},
    "industry": {"label": "行业深度调研", "icon": "🔬", "tag_class": "tag-research"},
}

SCRIPT_TAG = '<script src="../nav.js"></script>'

# ---------------------------------------------------------------------------
# 1. Load
# ---------------------------------------------------------------------------
def load_reports():
    with open(REPORTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    # validate
    required = {"file", "title", "category"}
    for i, r in enumerate(data):
        missing = required - set(r.keys())
        if missing:
            raise ValueError(f"reports.json entry {i}: missing fields {missing}")
        if r["category"] not in CATEGORIES:
            raise ValueError(f"reports.json entry {i}: unknown category '{r['category']}'")
        file_path = HTML_DIR / r["file"]
        if not file_path.exists():
            print(f"  ⚠ WARNING: file not found — {r['file']}")
    return data


# ---------------------------------------------------------------------------
# 2. Generate nav.js
# ---------------------------------------------------------------------------
def generate_nav_js(reports):
    reports_js = json.dumps(reports, ensure_ascii=False, indent=4)
    categories_js = json.dumps(CATEGORIES, ensure_ascii=False, indent=4)

    # Template: everything between the marker comments gets replaced
    template = r"""(function() {
  'use strict';

  // ====== AUTO-GENERATED FROM reports.json — DO NOT EDIT ======

  var REPORTS = __REPORTS__;

  var CATEGORIES = __CATEGORIES__;

  // ====== Detect current page ======
  var pathParts = window.location.pathname.split('/');
  var currentFile = decodeURIComponent(pathParts[pathParts.length - 1]);
  var isIndex = (currentFile === '' || currentFile.toLowerCase() === 'index.html');

  // ====== Inject CSS ======
  var style = document.createElement('style');
  style.textContent = [
    '.sn-nav *,.sn-panel *,.sn-top-btn *{margin:0;padding:0;box-sizing:border-box}',
    '.sn-nav{position:fixed;top:0;left:0;right:0;z-index:9999;height:48px;background:#161b22;border-bottom:1px solid #30363d;display:flex;align-items:center;justify-content:space-between;padding:0 24px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif}',
    '.sn-nav a{color:#58a6ff;text-decoration:none;font-size:14px;transition:color 0.15s}',
    '.sn-nav a:hover{color:#79c0ff}',
    '.sn-nav .sn-brand{color:#f0f6fc;font-weight:600;font-size:15px;display:flex;align-items:center;gap:8px;cursor:pointer}',
    '.sn-nav .sn-brand:hover{color:#f0f6fc;text-decoration:none}',
    '.sn-nav .sn-brand .sn-logo{font-size:18px}',
    '.sn-nav .sn-right{display:flex;align-items:center;gap:12px}',
    '.sn-nav .sn-toggle{background:#21262d;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:5px 14px;cursor:pointer;font-size:13px;font-family:inherit;transition:background 0.15s,border-color 0.15s;display:flex;align-items:center;gap:6px}',
    '.sn-nav .sn-toggle:hover{background:#30363d;border-color:#58a6ff}',
    '.sn-nav .sn-toggle .sn-arrow{font-size:10px;transition:transform 0.2s}',
    '.sn-nav .sn-toggle.open .sn-arrow{transform:rotate(180deg)}',
    '.sn-panel{display:none;position:fixed;top:48px;left:0;right:0;z-index:9998;background:#161b22;border-bottom:1px solid #30363d;max-height:70vh;overflow-y:auto;padding:16px 24px;box-shadow:0 8px 24px rgba(0,0,0,0.5)}',
    '.sn-panel.open{display:block;animation:snFadeIn 0.15s ease}',
    '@keyframes snFadeIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}',
    '.sn-panel .sn-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}',
    '.sn-panel .sn-group{margin-bottom:4px}',
    '.sn-panel .sn-group-label{color:#8b949e;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;padding-left:4px;font-weight:600}',
    '.sn-panel .sn-item{display:block;padding:7px 10px;border-radius:6px;font-size:13px;color:#c9d1d9;text-decoration:none;transition:background 0.12s,color 0.12s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.sn-panel .sn-item:hover{background:#1c2128;color:#f0f6fc}',
    '.sn-panel .sn-item.active{color:#58a6ff;font-weight:600;background:rgba(88,166,255,0.08)}',
    '.sn-panel .sn-item .sn-badge{font-size:11px;color:#8b949e;font-weight:400;margin-left:4px}',
    '.sn-top-btn{position:fixed;bottom:28px;right:28px;z-index:9997;width:42px;height:42px;border-radius:50%;background:#161b22;border:1px solid #30363d;color:#8b949e;font-size:20px;cursor:pointer;display:none;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,0.4);transition:border-color 0.2s,color 0.2s,transform 0.15s}',
    '.sn-top-btn:hover{border-color:#58a6ff;color:#58a6ff;transform:translateY(-2px)}',
    '.sn-top-btn.visible{display:flex}',
    '.sn-overlay{display:none;position:fixed;inset:0;z-index:9997;background:rgba(0,0,0,0.3)}',
    '.sn-overlay.open{display:block}',
    '@media print{.sn-nav,.sn-panel,.sn-top-btn,.sn-overlay{display:none!important}}',
    '@media(max-width:640px){.sn-nav{padding:0 16px}.sn-panel{padding:12px 16px;max-height:60vh}.sn-panel .sn-grid{grid-template-columns:1fr}.sn-top-btn{bottom:20px;right:20px;width:38px;height:38px}}'
  ].join('');
  document.head.appendChild(style);

  // ====== Inject overlay ======
  var overlay = document.createElement('div');
  overlay.className = 'sn-overlay';
  overlay.id = 'snOverlay';
  document.body.appendChild(overlay);

  // ====== Inject nav bar ======
  var brandHTML = isIndex
    ? '<span class="sn-brand"><span class="sn-logo">🔍</span>Serenity 研究报告</span>'
    : '<a class="sn-brand" href="../index.html"><span class="sn-logo">🔍</span>Serenity 研究报告</a>';

  var navHTML = '<div class="sn-nav" id="snNav">'
    + brandHTML
    + '<div class="sn-right">'
    + '<button class="sn-toggle" id="snToggle">📋 所有报告 <span class="sn-arrow">▾</span></button>'
    + '</div></div>';

  document.body.insertAdjacentHTML('afterbegin', navHTML);

  // ====== Inject dropdown panel ======
  var panelHTML = '<div class="sn-panel" id="snPanel"><div class="sn-grid">';

  Object.keys(CATEGORIES).forEach(function(catKey) {
    var cat = CATEGORIES[catKey];
    panelHTML += '<div class="sn-group"><div class="sn-group-label">' + cat.icon + ' ' + cat.label + '</div>';
    REPORTS.forEach(function(r) {
      if (r.category !== catKey) return;
      var isActive = (!isIndex && r.file === currentFile);
      var activeClass = isActive ? ' active' : '';
      var link = isIndex ? 'html/' + r.file : encodeURIComponent(r.file);
      panelHTML += '<a class="sn-item' + activeClass + '" href="' + link + '">'
        + '▸ ' + r.title
        + (r.subtitle ? '<span class="sn-badge">· ' + r.subtitle + '</span>' : '')
        + (isActive ? ' ←' : '')
        + '</a>';
    });
    panelHTML += '</div>';
  });

  panelHTML += '</div></div>';
  document.body.insertAdjacentHTML('beforeend', panelHTML);

  // ====== Inject back-to-top button ======
  var topBtn = document.createElement('button');
  topBtn.className = 'sn-top-btn';
  topBtn.id = 'snTop';
  topBtn.innerHTML = '↑';
  topBtn.title = '回到顶部';
  document.body.appendChild(topBtn);

  document.body.style.paddingTop = '52px';

  // ====== Event handlers ======
  var toggle = document.getElementById('snToggle');
  var panel = document.getElementById('snPanel');
  var topBtnEl = document.getElementById('snTop');
  var overlayEl = document.getElementById('snOverlay');

  function openPanel() {
    panel.classList.add('open');
    toggle.classList.add('open');
    overlayEl.classList.add('open');
  }
  function closePanel() {
    panel.classList.remove('open');
    toggle.classList.remove('open');
    overlayEl.classList.remove('open');
  }

  if (toggle) {
    toggle.addEventListener('click', function(e) {
      e.stopPropagation();
      panel.classList.contains('open') ? closePanel() : openPanel();
    });
  }
  if (overlayEl) {
    overlayEl.addEventListener('click', closePanel);
  }
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && panel && panel.classList.contains('open')) {
      closePanel();
    }
  });
  window.addEventListener('scroll', function() {
    if (topBtnEl) {
      topBtnEl.classList.toggle('visible', window.scrollY > 300);
    }
  });
  if (topBtnEl) {
    topBtnEl.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
})();
"""

    # Add a more readable indent: 2 spaces for JS (but keep the array compact per entry)
    reports_compact = json.dumps(reports, ensure_ascii=False, indent=2)
    categories_compact = json.dumps(CATEGORIES, ensure_ascii=False, indent=2)

    result = template.replace("__REPORTS__", reports_compact)
    result = result.replace("__CATEGORIES__", categories_compact)

    with open(NAV_JS, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"  ✓ Generated {NAV_JS.name}")


# ---------------------------------------------------------------------------
# 3. Generate index.html
# ---------------------------------------------------------------------------
def generate_card(report):
    """Generate a single card <a> element for the index page."""
    cat = CATEGORIES[report["category"]]
    tags_html = ""
    for tag_text in report.get("tags", []):
        # first tag uses category class, rest use stock tag
        if tag_text == report["tags"][0]:
            tags_html += f'\n          <span class="tag {cat["tag_class"]}">{tag_text}</span>'
        else:
            tags_html += f'\n          <span class="tag tag-stock">{tag_text}</span>'

    return f'''      <a class="card" href="html/{report["file"]}">
        <div class="card-tags">{tags_html}
        </div>
        <div class="card-title">{report["title"]}</div>
        <div class="card-subtitle">{report["subtitle"]}</div>
      </a>'''


def generate_index_html(reports):
    company_cards = "\n\n".join(generate_card(r) for r in reports if r["category"] == "company")
    industry_cards = "\n\n".join(generate_card(r) for r in reports if r["category"] == "industry")
    company_count = sum(1 for r in reports if r["category"] == "company")
    industry_count = sum(1 for r in reports if r["category"] == "industry")
    total = len(reports)

    index_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Serenity 研究报告 · 供应链瓶颈分析</title>
  <style>
    :root {{
      --bg: #0d1117;
      --card-bg: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --text-muted: #8b949e;
      --heading: #f0f6fc;
      --accent: #58a6ff;
      --green: #3fb950;
      --orange: #d2991d;
      --purple: #a371f7;
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
    }}

    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 32px 24px 60px;
    }}

    .hero {{
      text-align: center;
      padding: 48px 0 36px;
    }}
    .hero .logo {{
      font-size: 48px;
      margin-bottom: 12px;
      display: block;
    }}
    .hero h1 {{
      font-size: 36px;
      font-weight: 700;
      color: var(--heading);
      letter-spacing: -0.5px;
    }}
    .hero h1 .accent {{
      color: var(--accent);
    }}
    .hero p {{
      color: var(--text-muted);
      margin-top: 10px;
      font-size: 17px;
      max-width: 520px;
      margin-left: auto;
      margin-right: auto;
    }}
    .hero .stats {{
      display: flex;
      justify-content: center;
      gap: 28px;
      margin-top: 20px;
    }}
    .hero .stat {{
      text-align: center;
    }}
    .hero .stat-num {{
      font-size: 28px;
      font-weight: 700;
      color: var(--accent);
    }}
    .hero .stat-label {{
      font-size: 12px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .section {{
      margin-top: 36px;
    }}
    .section-title {{
      font-size: 20px;
      font-weight: 600;
      color: var(--heading);
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .section-title .count {{
      font-size: 13px;
      font-weight: 400;
      color: var(--text-muted);
      background: var(--card-bg);
      padding: 2px 10px;
      border-radius: 10px;
      border: 1px solid var(--border);
    }}

    .card-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 16px;
    }}

    .card {{
      display: block;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 22px 24px;
      text-decoration: none;
      color: inherit;
      transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
      position: relative;
      overflow: hidden;
    }}
    .card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 3px;
      height: 100%;
      background: var(--border);
      transition: background 0.2s;
    }}
    .card:hover {{
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }}
    .card:hover::before {{
      background: var(--accent);
    }}

    .card-tags {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }}
    .tag {{
      font-size: 11px;
      padding: 3px 10px;
      border-radius: 12px;
      font-weight: 500;
      border: 1px solid;
    }}
    .tag-analysis {{
      background: rgba(88, 166, 255, 0.1);
      color: var(--accent);
      border-color: rgba(88, 166, 255, 0.25);
    }}
    .tag-research {{
      background: rgba(63, 185, 80, 0.1);
      color: var(--green);
      border-color: rgba(63, 185, 80, 0.25);
    }}
    .tag-stock {{
      background: var(--bg);
      color: var(--text-muted);
      border-color: var(--border);
    }}

    .card-title {{
      font-size: 16px;
      font-weight: 600;
      color: var(--heading);
      margin-bottom: 6px;
      line-height: 1.4;
    }}
    .card-subtitle {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    .footer {{
      text-align: center;
      color: #484f58;
      font-size: 13px;
      padding: 40px 0 16px;
      margin-top: 48px;
      border-top: 1px solid var(--border);
      line-height: 1.8;
    }}
    .footer strong {{
      color: #6e7681;
    }}

    @media (max-width: 768px) {{
      .hero {{ padding: 32px 0 24px; }}
      .hero h1 {{ font-size: 26px; }}
      .hero p {{ font-size: 15px; }}
      .hero .stats {{ gap: 18px; }}
      .hero .stat-num {{ font-size: 22px; }}
      .card-grid {{ grid-template-columns: 1fr; }}
      .container {{ padding: 20px 16px 40px; }}
    }}

    @media print {{
      body {{ background: #fff; color: #1a1a1a; }}
      .card {{ border-color: #ddd; break-inside: avoid; }}
      .card:hover {{ transform: none; box-shadow: none; }}
    }}
  </style>
</head>
<body>

<div class="container">

  <header class="hero">
    <span class="logo">🔍</span>
    <h1>Serenity <span class="accent">研究报告</span></h1>
    <p>AI 半导体产业链 · 供应链瓶颈分析 · A 股深度调研</p>
    <div class="stats">
      <div class="stat">
        <div class="stat-num">{total}</div>
        <div class="stat-label">份报告</div>
      </div>
      <div class="stat">
        <div class="stat-num">{company_count}</div>
        <div class="stat-label">公司分析</div>
      </div>
      <div class="stat">
        <div class="stat-num">{industry_count}</div>
        <div class="stat-label">行业调研</div>
      </div>
      <div class="stat">
        <div class="stat-num">2026</div>
        <div class="stat-label">年份</div>
      </div>
    </div>
  </header>

  <section class="section">
    <h2 class="section-title">
      📈 公司深度分析
      <span class="count">{company_count} 篇</span>
    </h2>
    <div class="card-grid">

{company_cards}

    </div>
  </section>

  <section class="section">
    <h2 class="section-title">
      🔬 行业深度调研
      <span class="count">{industry_count} 篇</span>
    </h2>
    <div class="card-grid">

{industry_cards}

    </div>
  </section>

  <footer class="footer">
    <strong>Serenity</strong> · Supply-Chain Bottleneck Hunter<br>
    本页面仅供研究参考，不构成任何投资建议。<br>
    Generated 2026-06
  </footer>

</div>

</body>
</html>
'''

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  ✓ Generated {INDEX_HTML.name}  ({total} reports)")


# ---------------------------------------------------------------------------
# 4. Inject nav.js script tag into all HTML files (idempotent)
# ---------------------------------------------------------------------------
def inject_scripts(dry_run=False):
    html_files = sorted(HTML_DIR.glob("*.html"))
    if not html_files:
        print("  ⚠ No HTML files found in html/")
        return

    injected = 0
    skipped = 0

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")

        if SCRIPT_TAG in content:
            skipped += 1
            continue

        # Inject before </body>
        if "</body>" not in content:
            print(f"  ⚠ No </body> tag found in {html_file.name} — skipping")
            continue

        new_content = content.replace("</body>", f"{SCRIPT_TAG}\n</body>")

        if dry_run:
            print(f"  → Would inject: {html_file.name}")
        else:
            html_file.write_text(new_content, encoding="utf-8")
        injected += 1

    action = "Would inject" if dry_run else "Injected"
    print(f"  ✓ {action} script into {injected} file(s), {skipped} already had it")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    dry_run = "--check" in sys.argv or "--dry-run" in sys.argv

    if dry_run:
        print("=== DRY RUN (no files will be modified) ===\n")

    print("1. Loading reports.json ...")
    reports = load_reports()
    print(f"   Loaded {len(reports)} reports\n")

    if dry_run:
        print("2. Would generate nav.js ...")
        print("3. Would generate index.html ...")
        print("4. Would inject scripts into HTML files ...\n")
        inject_scripts(dry_run=True)
        print("\nRun without --check to apply changes.")
    else:
        print("2. Generating nav.js ...")
        generate_nav_js(reports)

        print("3. Generating index.html ...")
        generate_index_html(reports)

        print("4. Injecting nav.js into HTML files ...")
        inject_scripts(dry_run=False)

        print("\n✅ Build complete.")
        print(f"   Reports source: {REPORTS_JSON.name}")
        print(f"   Generated: {NAV_JS.name}, {INDEX_HTML.name}")
        print(f"   Script injected into HTML files under {HTML_DIR.name}/")


if __name__ == "__main__":
    main()
