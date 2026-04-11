from playwright.sync_api import sync_playwright
import os

WIDTH, HEIGHT = 1080, 1080
BRAND = "#6C5CE7"

def items_html():
    rows = [
        ("Placement fee", "Already paid. Non-refundable in most cases."),
        ("Onboarding time", "2-4 weeks of manager and team bandwidth, gone."),
        ("Discovery lag", "3-6 weeks before the performance gap becomes undeniable."),
        ("Exit process", "Notice period, documentation, rehiring approval."),
        ("Repeat search", "Full cycle restarts. Timeline resets."),
    ]
    return "".join(
        f'<div class="item"><div class="num">{i+1}</div><div class="body">'
        f'<div class="label">{label}</div><div class="desc">{desc}</div></div></div>'
        for i, (label, desc) in enumerate(rows)
    )

BASE = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{WIDTH}px;height:{HEIGHT}px;background:#fff;
     font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;
     display:flex;flex-direction:column;padding:72px;position:relative;overflow:hidden}}
.bar{{position:absolute;top:0;left:0;right:0;height:8px;background:{BRAND}}}
.items{{display:flex;flex-direction:column;gap:18px;flex:1}}
.item{{display:flex;align-items:flex-start;gap:22px;padding:20px 28px;
       background:#F5F3FF;border-radius:14px;border-left:5px solid {BRAND}}}
.num{{font-size:26px;font-weight:800;color:{BRAND};min-width:32px;margin-top:2px}}
.label{{font-size:24px;font-weight:700;color:#1A1A2E;margin-bottom:4px}}
.desc{{font-size:19px;color:#64748B;line-height:1.4}}
.footer{{margin-top:28px;display:flex;justify-content:space-between;align-items:center}}
.brand{{font-size:24px;font-weight:700;color:{BRAND}}}
.brand b{{color:#1A1A2E;font-weight:800}}
.url{{font-size:18px;color:#94A3B8}}
"""

html_a = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE}
.tag{{display:inline-block;background:{BRAND};color:#fff;font-size:18px;
      font-weight:700;letter-spacing:.08em;text-transform:uppercase;
      padding:9px 24px;border-radius:6px;margin-bottom:28px;align-self:flex-start}}
.title{{font-size:50px;font-weight:800;color:#1A1A2E;line-height:1.15;margin-bottom:40px;max-width:880px}}
</style></head><body><div class="bar"></div>
<div class="tag">For Hiring Agencies</div>
<div class="title">The Proxy Cost Cascade</div>
<div class="items">{items_html()}</div>
<div class="footer"><div class="brand">Talent<b>Lens</b></div><div class="url">talentlens.evolvision.com</div></div>
</body></html>"""

html_b = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE}
.tag{{display:inline-block;background:{BRAND}1a;color:{BRAND};font-size:17px;
      font-weight:700;letter-spacing:.08em;text-transform:uppercase;
      padding:8px 20px;border-radius:6px;margin-bottom:16px;align-self:flex-start}}
.hook{{font-size:25px;font-weight:600;color:#EF4444;margin-bottom:14px;line-height:1.3}}
.title{{font-size:46px;font-weight:800;color:#1A1A2E;line-height:1.15;margin-bottom:34px;max-width:880px}}
</style></head><body><div class="bar"></div>
<div class="tag">Framework</div>
<div class="hook">One proxy hire. 3-5 months of calendar time lost.</div>
<div class="title">The Proxy Cost Cascade</div>
<div class="items">{items_html()}</div>
<div class="footer"><div class="brand">Talent<b>Lens</b></div><div class="url">talentlens.evolvision.com</div></div>
</body></html>"""

html_c = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE}
.tag{{display:inline-block;background:{BRAND};color:#fff;font-size:17px;
      font-weight:700;letter-spacing:.08em;text-transform:uppercase;
      padding:9px 24px;border-radius:6px;margin-bottom:16px;align-self:flex-start}}
.hook{{font-size:25px;font-weight:600;color:#EF4444;margin-bottom:14px;line-height:1.3}}
.title{{font-size:46px;font-weight:800;color:#1A1A2E;line-height:1.15;margin-bottom:34px;max-width:880px}}
</style></head><body><div class="bar"></div>
<div class="tag">For Hiring Agencies</div>
<div class="hook">One proxy hire. 3-5 months of calendar time lost.</div>
<div class="title">The Proxy Cost Cascade</div>
<div class="items">{items_html()}</div>
<div class="footer"><div class="brand">Talent<b>Lens</b></div><div class="url">talentlens.evolvision.com</div></div>
</body></html>"""

os.makedirs("output/Day-1_2026-04-11", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, html in [
        ("option-a-audience-tag", html_a),
        ("option-b-hook-line", html_b),
        ("option-c-combined", html_c),
    ]:
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
        page.set_content(html, wait_until="networkidle")
        path = f"output/Day-1_2026-04-11/{name}.png"
        page.screenshot(path=path)
        print(f"Saved: {path}")
    browser.close()
