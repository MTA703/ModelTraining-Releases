import json, math, sys, os

paths = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)

PIVOT = (1229, 545)
ATTACH = {"left": (819, 590), "right": (1636, 590)}

GRAD = """<linearGradient id="gold" gradientUnits="userSpaceOnUse" x1="150" y1="0" x2="1850" y2="0">
      <stop offset="0" stop-color="#D9A535"/>
      <stop offset=".09" stop-color="#F3CC66"/>
      <stop offset=".27" stop-color="#D4A00A"/>
      <stop offset=".53" stop-color="#F7D478"/>
      <stop offset=".70" stop-color="#D4A00A"/>
      <stop offset=".87" stop-color="#F6CD62"/>
      <stop offset="1" stop-color="#DCA935"/>
    </linearGradient>"""

ORDER = ["beam", "hanger-left", "hanger-right", "pan-left", "pan-right", "name", "title", "subtitle"]


def layers(animated):
    a = ' pathLength="1"' if animated else ""
    def p(k):
        return f'<path id="{k}" class="part" d="{paths[k]}"{a}/>'
    return f"""<g id="logo" fill="url(#gold)">
    <g id="title-g">{p('title')}</g>
    <g id="scale">
      <g id="beam-g">{p('beam')}
        <g id="side-left">{p('hanger-left')}{p('pan-left')}</g>
        <g id="side-right">{p('hanger-right')}{p('pan-right')}</g>
      </g>
    </g>
    <g id="name-g">{p('name')}</g>
    <g id="subtitle-g">{p('subtitle')}</g>
  </g>"""


HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 2000" role="img" aria-label="مؤسسة النصر للمحاماة">'

# ---------- static ----------
static = f"""{HEAD}
  <title>مؤسسة النصر للمحاماة</title>
  <defs>
    {GRAD}
  </defs>
  {layers(False)}
</svg>
"""
open(f"{out}/logo.svg", "w").write(static)

# ---------- balance keyframes ----------
# beam rotates around PIVOT; each pan side is counter-rotated so pans stay level
# (rotate(-θ) around its own attach point inside the rotated beam group).
def side_kf(name, steps):
    ax, ay = ATTACH[name]
    rows = []
    for pct, th in steps:
        rows.append(f"  {pct}% {{ transform: rotate({-th}deg); }}")
    return f"@keyframes swing-{name} {{\n" + "\n".join(rows) + "\n}"

STEPS = [(0, 0), (22, 4), (44, -2.6), (62, 1.6), (78, -0.7), (90, 0.25), (100, 0)]
beam_kf = "@keyframes swing-beam {\n" + "\n".join(
    f"  {p}% {{ transform: rotate({t}deg); }}" for p, t in STEPS) + "\n}"

# ---------- animated ----------
# timeline (s): draw outlines 0→2.2, fill 0.9→3.0, balance 2.6→5.4, shimmer 4.6→6.0
delays = {"beam": 0.0, "hanger-left": .35, "hanger-right": .35, "pan-left": .6, "pan-right": .6,
          "name": .5, "title": .9, "subtitle": 1.1}
part_css = "\n".join(
    f"#logo #{k} {{ animation-delay: {d}s, {d + 1.0}s; }}" for k, d in delays.items())

CSS = f"""
#logo .part {{
  stroke: url(#gold); stroke-width: 5; stroke-linejoin: round;
  stroke-dasharray: 1 1; stroke-dashoffset: 1; fill-opacity: 0;
  animation: draw 1.6s cubic-bezier(.55,.1,.35,1) forwards, fill 1.3s ease forwards;
}}
{part_css}
@keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
@keyframes fill {{ to {{ fill-opacity: 1; stroke-width: 0; }} }}

#beam-g {{ transform-origin: {PIVOT[0]}px {PIVOT[1]}px; animation: swing-beam 2.8s ease-in-out 2.6s both; }}
#side-left {{ transform-origin: {ATTACH['left'][0]}px {ATTACH['left'][1]}px; animation: swing-left 2.8s ease-in-out 2.6s both; }}
#side-right {{ transform-origin: {ATTACH['right'][0]}px {ATTACH['right'][1]}px; animation: swing-right 2.8s ease-in-out 2.6s both; }}
{beam_kf}
{side_kf('left', STEPS)}
{side_kf('right', STEPS)}

#shine {{ transform: translateX(-1400px); animation: shine 1.4s ease-in-out 4.6s forwards; }}
@keyframes shine {{ to {{ transform: translateX(2200px); }} }}

@media (prefers-reduced-motion: reduce) {{
  #logo .part, #beam-g, #side-left, #side-right, #shine {{ animation-duration: 1ms !important; animation-delay: 0s !important; }}
}}
"""

anim = f"""{HEAD}
  <title>مؤسسة النصر للمحاماة</title>
  <defs>
    {GRAD}
    <linearGradient id="shine-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#FFF6D8" stop-opacity=".85"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="logo-clip">
      {''.join(f'<use href="#{k}"/>' for k in ORDER)}
    </clipPath>
  </defs>
  <style>{CSS}</style>
  {layers(True)}
  <g clip-path="url(#logo-clip)" pointer-events="none">
    <rect id="shine" x="0" y="-200" width="420" height="2400" fill="url(#shine-grad)" transform-origin="center" style="transform-box: view-box" />
  </g>
</svg>
"""
# skew the shine band slightly for a nicer sweep
anim = anim.replace('<g clip-path="url(#logo-clip)" pointer-events="none">',
                    '<g clip-path="url(#logo-clip)" pointer-events="none"><g transform="skewX(-18)">', 1)
anim = anim.replace('style="transform-box: view-box" />\n  </g>', 'style="transform-box: view-box" />\n  </g></g>', 1)
open(f"{out}/logo-animated.svg", "w").write(anim)
print("ok")
