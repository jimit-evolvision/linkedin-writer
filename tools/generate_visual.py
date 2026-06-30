#!/usr/bin/env python3
"""
LinkedIn Visual Generator — AI Access Campaign
Generates structured visuals locally using Playwright (headless Chromium).
No external API required.

Setup:
  pip install playwright
  playwright install chromium

Templates:
  framework  — numbered framework card (e.g. "The Integrity Stack")
  stat       — large number/claim card (e.g. "₹4/min")
  process    — numbered step flow (e.g. "The 4-Tool Problem")
  quote      — bold key line from the post (for stories and reflective posts)

Output is always saved under output/YYYY-MM-DD/ for easy tracking.
--output is optional: if omitted, a slug is auto-generated from the title.

Usage:
  python tools/generate_visual.py framework \\
    --title "The Integrity Stack" \\
    --items "Face liveness detection:Is the person on screen actually live?" \\
            "Multi-voice detection:Is someone coaching from off-screen?" \\
            "Naturalness scoring:Are answers too rehearsed?" \\
            "Eye movement tracking:Is attention consistent with real recall?"

  python tools/generate_visual.py stat \\
    --headline "₹4/min" \\
    --subtext "Full AI screening. Integrity suite. Live code editor." \\
    --context "vs $25,000/year with HireVue"

  python tools/generate_visual.py process \\
    --title "The 4-Tool Problem" \\
    --steps "Post JD on Naukri/LinkedIn" "ATS collects applications" \\
            "Manual phone screen" "HackerRank coding test" \\
            "Video call for tech round" "Evaluation shared manually"

  # Override the output filename (still saved under output/YYYY-MM-DD/):
  python tools/generate_visual.py framework --title "..." --items "..." --output my-card.png
"""

import argparse
import base64
import html
import os
import re
import sys
from datetime import date

WIDTH = 1080
HEIGHT = 1080
BRAND_COLOR = "#6C5CE7"
OUTPUT_ROOT = "output"

BG_DARK = "#0D0E1A"
BG_CARD = "rgba(255,255,255,0.07)"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#9CA3AF"
TEXT_MUTED = "rgba(255,255,255,0.38)"


def _load_logo_uri():
    """Load AI Access logo as a base64 data URI for embedding in HTML."""
    logo_path = os.path.join(os.path.dirname(__file__), "..", "images", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{data}"
    return None


LOGO_URI = _load_logo_uri()


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def output_dir(day=None):
    """
    Returns the output subdirectory.
    - With --day N: output/Day-N_YYYY-MM-DD/
    - Without:      output/YYYY-MM-DD/  (fallback)
    """
    today = date.today().strftime("%Y-%m-%d")
    if day is not None:
        return os.path.join(OUTPUT_ROOT, f"Day-{day}_{today}")
    return os.path.join(OUTPUT_ROOT, today)


def slugify(text):
    """Convert a title to a safe filename slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "visual"


def resolve_output(args_output, title_or_headline, day=None):
    """
    Determine final output path.
    - Absolute --output: used as-is.
    - Otherwise: place filename (or auto-slug) inside output/Day-N_YYYY-MM-DD/.
    """
    if args_output and os.path.isabs(args_output):
        return args_output

    directory = output_dir(day)

    if args_output:
        filename = os.path.basename(args_output)
        if not filename.endswith(".png"):
            filename += ".png"
    else:
        filename = slugify(title_or_headline) + ".png"

    return os.path.join(directory, filename)


# ---------------------------------------------------------------------------
# HTML templates
# ---------------------------------------------------------------------------

def e(text):
    """HTML-escape user text so special characters render correctly."""
    return html.escape(str(text))


def _footer_html():
    logo = f'<img class="logo-img" src="{LOGO_URI}" />' if LOGO_URI else '<span class="logo-fallback">AI Assess</span>'
    return f"""<div class="footer">
      {logo}
      <div class="brand-text">AI enabled Assessment Platform</div>
    </div>"""


def framework_card_html(title, items, brand=BRAND_COLOR, hook=None, tag="Framework"):
    items_html = "".join(
        f"""<div class="item">
              <div class="num">{i + 1}</div>
              <div class="body">
                <div class="label">{e(label)}</div>
                {"<div class='desc'>" + e(desc) + "</div>" if desc else ""}
              </div>
            </div>"""
        for i, (label, desc) in enumerate(items)
    )
    hook_html = f'<div class="hook">{e(hook)}</div>' if hook else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{width:{WIDTH}px;height:{HEIGHT}px;background:{BG_DARK};
         font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;
         display:flex;flex-direction:column;padding:72px;position:relative;overflow:hidden}}
    .bar{{position:absolute;top:0;left:0;right:0;height:6px;background:{brand}}}
    .glow{{position:absolute;top:-200px;right:-200px;width:600px;height:600px;
           border-radius:50%;background:radial-gradient(circle,{brand}22 0%,transparent 70%);pointer-events:none}}
    .tag{{display:inline-block;background:{brand};color:#fff;font-size:20px;
          font-weight:700;letter-spacing:.1em;text-transform:uppercase;
          padding:8px 20px;border-radius:6px;margin-bottom:16px;align-self:flex-start}}
    .hook{{font-size:25px;font-weight:700;color:#0D0E1A;background:#FFE566;
           display:inline-block;align-self:flex-start;
           padding:4px 12px;border-radius:4px;margin-bottom:16px;line-height:1.4}}
    .title{{font-size:50px;font-weight:800;color:{TEXT_PRIMARY};line-height:1.15;margin-bottom:44px;max-width:880px}}
    .items{{display:flex;flex-direction:column;gap:18px;flex:1}}
    .item{{display:flex;align-items:flex-start;gap:22px;
           padding:24px 28px;background:{BG_CARD};border-radius:14px;
           border-left:5px solid {brand};backdrop-filter:blur(10px)}}
    .num{{font-size:26px;font-weight:800;color:{brand};min-width:32px;margin-top:2px}}
    .label{{font-size:26px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:4px}}
    .desc{{font-size:20px;color:{TEXT_SECONDARY};line-height:1.45}}
    .footer{{margin-top:32px;display:flex;align-items:center;justify-content:space-between}}
    .logo-img{{height:72px;object-fit:contain}}
    .logo-fallback{{font-size:22px;font-weight:800;color:#fff}}
    .brand-text{{font-size:18px;font-weight:500;color:{TEXT_MUTED};letter-spacing:.02em}}
    </style></head><body>
    <div class="bar"></div>
    <div class="glow"></div>
    <div class="tag">{e(tag)}</div>
    {hook_html}
    <div class="title">{e(title)}</div>
    <div class="items">{items_html}</div>
    {_footer_html()}
    </body></html>"""


def stat_card_html(headline, subtext, context="", brand=BRAND_COLOR):
    ctx = f'<div class="ctx">{e(context)}</div>' if context else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{width:{WIDTH}px;height:{HEIGHT}px;
         background:linear-gradient(135deg,{BG_DARK} 0%,#14102A 100%);
         font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;
         display:flex;flex-direction:column;padding:80px;position:relative;overflow:hidden}}
    .c1{{position:absolute;width:720px;height:720px;border-radius:50%;
         background:radial-gradient(circle,{brand}28 0%,transparent 70%);
         top:-250px;right:-250px;pointer-events:none}}
    .c2{{position:absolute;width:400px;height:400px;border-radius:50%;
         background:radial-gradient(circle,{brand}18 0%,transparent 70%);
         bottom:-120px;left:-120px;pointer-events:none}}
    .content{{flex:1;display:flex;flex-direction:column;align-items:center;
              justify-content:center;text-align:center;position:relative;z-index:1}}
    .headline{{font-size:148px;font-weight:900;color:#fff;line-height:1;
               letter-spacing:-.03em;margin-bottom:28px}}
    .sub{{font-size:34px;font-weight:600;color:rgba(255,255,255,.9);
          line-height:1.45;margin-bottom:20px;max-width:720px}}
    .ctx{{font-size:24px;color:rgba(255,255,255,.45)}}
    .footer{{display:flex;align-items:center;justify-content:space-between;
             position:relative;z-index:1}}
    .logo-img{{height:72px;object-fit:contain}}
    .logo-fallback{{font-size:22px;font-weight:800;color:#fff}}
    .brand-text{{font-size:18px;font-weight:500;color:{TEXT_MUTED};letter-spacing:.02em}}
    </style></head><body>
    <div class="c1"></div><div class="c2"></div>
    <div class="content">
      <div class="headline">{e(headline)}</div>
      <div class="sub">{e(subtext)}</div>
      {ctx}
    </div>
    {_footer_html()}
    </body></html>"""


def process_flow_html(title, steps, brand=BRAND_COLOR, hook=None, tag="Process"):
    items_html = ""
    for i, step in enumerate(steps):
        items_html += (
            f'<div class="step">'
            f'<div class="num">{i + 1}</div>'
            f'<div class="text">{e(step)}</div>'
            f'</div>'
        )
        if i < len(steps) - 1:
            items_html += '<div class="connector"></div>'

    hook_html = f'<div class="hook">{e(hook)}</div>' if hook else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{width:{WIDTH}px;height:{HEIGHT}px;background:{BG_DARK};
         font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;
         display:flex;flex-direction:column;padding:72px;position:relative;overflow:hidden}}
    .bar{{position:absolute;top:0;left:0;right:0;height:6px;background:{brand}}}
    .glow{{position:absolute;top:-200px;right:-200px;width:600px;height:600px;
           border-radius:50%;background:radial-gradient(circle,{brand}22 0%,transparent 70%);pointer-events:none}}
    .tag{{display:inline-block;background:{brand};color:#fff;font-size:20px;
          font-weight:700;letter-spacing:.1em;text-transform:uppercase;
          padding:8px 20px;border-radius:6px;margin-bottom:16px;align-self:flex-start}}
    .hook{{font-size:25px;font-weight:700;color:#0D0E1A;background:#FFE566;
           display:inline-block;align-self:flex-start;
           padding:4px 12px;border-radius:4px;margin-bottom:16px;line-height:1.4}}
    .title{{font-size:46px;font-weight:800;color:{TEXT_PRIMARY};line-height:1.2;margin-bottom:44px}}
    .steps{{display:flex;flex-direction:column;flex:1;justify-content:center}}
    .step{{display:flex;align-items:center;gap:22px}}
    .num{{width:50px;height:50px;border-radius:50%;background:{brand};color:#fff;
          font-size:22px;font-weight:800;display:flex;align-items:center;
          justify-content:center;flex-shrink:0}}
    .text{{font-size:28px;font-weight:600;color:{TEXT_PRIMARY}}}
    .connector{{width:3px;height:24px;background:{brand}55;margin-left:24px}}
    .footer{{margin-top:32px;display:flex;align-items:center;justify-content:space-between}}
    .logo-img{{height:72px;object-fit:contain}}
    .logo-fallback{{font-size:22px;font-weight:800;color:#fff}}
    .brand-text{{font-size:18px;font-weight:500;color:{TEXT_MUTED};letter-spacing:.02em}}
    </style></head><body>
    <div class="bar"></div>
    <div class="glow"></div>
    <div class="tag">{e(tag)}</div>
    {hook_html}
    <div class="title">{e(title)}</div>
    <div class="steps">{items_html}</div>
    {_footer_html()}
    </body></html>"""


def quote_card_html(quote, author="Jimit Joshi", brand=BRAND_COLOR):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{width:{WIDTH}px;height:{HEIGHT}px;background:{BG_DARK};
         font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;
         display:flex;flex-direction:column;padding:96px;position:relative;overflow:hidden}}
    .ring1{{position:absolute;width:800px;height:800px;border-radius:50%;
            border:1px solid {brand}22;top:-300px;right:-300px}}
    .ring2{{position:absolute;width:500px;height:500px;border-radius:50%;
            border:1px solid {brand}15;bottom:-200px;left:-200px}}
    .glow{{position:absolute;top:-150px;right:-150px;width:500px;height:500px;
           border-radius:50%;background:radial-gradient(circle,{brand}20 0%,transparent 70%);pointer-events:none}}
    .content{{flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:1}}
    .mark{{font-size:160px;font-weight:900;color:{brand};line-height:.8;
           align-self:flex-start;margin-bottom:8px;opacity:.7}}
    .quote{{font-size:46px;font-weight:700;color:{TEXT_PRIMARY};line-height:1.35;
            text-align:left;margin-bottom:48px}}
    .divider{{width:64px;height:4px;background:{brand};border-radius:2px;
              align-self:flex-start;margin-bottom:28px}}
    .author{{font-size:24px;font-weight:600;color:rgba(255,255,255,.5);
             align-self:flex-start;letter-spacing:.02em}}
    .footer{{display:flex;align-items:center;justify-content:space-between;
             position:relative;z-index:1}}
    .logo-img{{height:72px;object-fit:contain}}
    .logo-fallback{{font-size:22px;font-weight:800;color:#fff}}
    .brand-text{{font-size:18px;font-weight:500;color:{TEXT_MUTED};letter-spacing:.02em}}
    </style></head><body>
    <div class="ring1"></div><div class="ring2"></div>
    <div class="glow"></div>
    <div class="content">
      <div class="mark">"</div>
      <div class="quote">{e(quote)}</div>
      <div class="divider"></div>
      <div class="author">{e(author)}</div>
    </div>
    {_footer_html()}
    </body></html>"""


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render(html, output_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not found. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=output_path)
        browser.close()

    print(f"Saved: {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_items(raw):
    result = []
    for item in raw:
        if ":" in item:
            label, _, desc = item.partition(":")
            result.append((label.strip(), desc.strip()))
        else:
            result.append((item.strip(), ""))
    return result


def main():
    p = argparse.ArgumentParser(description="Generate LinkedIn visuals for AI Access.")
    sub = p.add_subparsers(dest="type", required=True)

    fw = sub.add_parser("framework")
    fw.add_argument("--title", required=True)
    fw.add_argument("--items", nargs="+", required=True, metavar="LABEL:DESC")
    fw.add_argument("--tag", default="Framework",
                    help="Pill label at the top (default: 'Framework'). Use e.g. 'For Hiring Agencies' for audience-targeting posts.")
    fw.add_argument("--hook", default=None,
                    help="Optional red hook line shown below the pill tag (e.g. 'Your screening passed the proxy.').")
    fw.add_argument("--day", type=int, default=None,
                    help="Campaign day number (e.g. 1). Saves to output/Day-1_YYYY-MM-DD/.")
    fw.add_argument("--output", default=None,
                    help="Optional filename override (e.g. my-card.png).")
    fw.add_argument("--color", default=BRAND_COLOR)

    st = sub.add_parser("stat")
    st.add_argument("--headline", required=True)
    st.add_argument("--subtext", required=True)
    st.add_argument("--context", default="")
    st.add_argument("--day", type=int, default=None,
                    help="Campaign day number (e.g. 1). Saves to output/Day-1_YYYY-MM-DD/.")
    st.add_argument("--output", default=None,
                    help="Optional filename override.")
    st.add_argument("--color", default=BRAND_COLOR)

    pf = sub.add_parser("process")
    pf.add_argument("--title", required=True)
    pf.add_argument("--steps", nargs="+", required=True)
    pf.add_argument("--tag", default="Process",
                    help="Pill label at the top (default: 'Process'). Override for audience-targeting posts.")
    pf.add_argument("--hook", default=None,
                    help="Optional red hook line shown below the pill tag.")
    pf.add_argument("--day", type=int, default=None,
                    help="Campaign day number (e.g. 1). Saves to output/Day-1_YYYY-MM-DD/.")
    pf.add_argument("--output", default=None,
                    help="Optional filename override.")
    pf.add_argument("--color", default=BRAND_COLOR)

    qt = sub.add_parser("quote")
    qt.add_argument("--quote", required=True, help="The key line from the post (max ~120 chars).")
    qt.add_argument("--author", default="Jimit Joshi", help="Attribution line.")
    qt.add_argument("--day", type=int, default=None,
                    help="Campaign day number (e.g. 1). Saves to output/Day-1_YYYY-MM-DD/.")
    qt.add_argument("--output", default=None,
                    help="Optional filename override.")
    qt.add_argument("--color", default=BRAND_COLOR)

    args = p.parse_args()

    if args.type == "framework":
        html = framework_card_html(args.title, parse_items(args.items), args.color, args.hook, args.tag)
        output_path = resolve_output(args.output, args.title, args.day)
    elif args.type == "stat":
        html = stat_card_html(args.headline, args.subtext, args.context, args.color)
        output_path = resolve_output(args.output, args.headline, args.day)
    elif args.type == "process":
        html = process_flow_html(args.title, args.steps, args.color, args.hook, args.tag)
        output_path = resolve_output(args.output, args.title, args.day)
    elif args.type == "quote":
        html = quote_card_html(args.quote, args.author, args.color)
        output_path = resolve_output(args.output, args.quote[:40], args.day)

    render(html, output_path)


if __name__ == "__main__":
    main()
