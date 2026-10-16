"""Build static + 6 animated SVG variants of the Al-Nasr logo from parts.json."""
import json, os, sys

data = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
P, M = data["parts"], data["meta"]
PX, PY = M["pivot"]
LX, LY = M["left"]
RX, RY = M["right"]

LABEL = "مؤسسة النصر للمحاماة"
GOLD = """<linearGradient id="gold" gradientUnits="userSpaceOnUse" x1="120" y1="0" x2="880" y2="0">
      <stop offset="0" stop-color="#B8860B"/>
      <stop offset=".22" stop-color="#E8C35E"/>
      <stop offset=".36" stop-color="#C99A1C"/>
      <stop offset=".5" stop-color="#F0D27C"/>
      <stop offset=".64" stop-color="#C99A1C"/>
      <stop offset=".78" stop-color="#E8C35E"/>
      <stop offset="1" stop-color="#B8860B"/>
    </linearGradient>"""
SHINE = """<linearGradient id="shine-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#FFF7DC" stop-opacity=".9"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>"""
ALL = ["title", "knob", "beam", "pillar", "hanger-left", "pan-left", "hanger-right", "pan-right",
       "name", "ornament", "subtitle"]


def path(k, draw=False):
    a = ' pathLength="1"' if draw else ""
    return f'<path id="p-{k}" class="p" d="{P[k]}"{a}/>'


def body(fill="url(#gold)", draw=False):
    p = lambda k: path(k, draw)
    return f"""<g id="logo" fill="{fill}">
    <g id="title" class="word">{p('title')}</g>
    <g id="scale">
      <g id="stand">{p('pillar')}</g>
      <g id="drop"><g id="arm">{p('knob')}{p('beam')}
        <g id="side-l">{p('hanger-left')}{p('pan-left')}</g>
        <g id="side-r">{p('hanger-right')}{p('pan-right')}</g>
      </g></g>
    </g>
    <g id="name" class="word">{p('name')}</g>
    <g id="sub" class="word">{p('subtitle')}</g>
    <g id="orn">{p('ornament')}</g>
  </g>"""


def svg(inner, defs="", css=""):
    style = f"<style>{css}</style>" if css else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-label="{LABEL}">
  <title>{LABEL}</title>
  <defs>
    {GOLD}{defs}
  </defs>{style}
  {inner}
</svg>
"""


def shine_layer(start, dur=1.3):
    clip = '<clipPath id="clip">' + "".join(f'<use href="#p-{k}"/>' for k in ALL) + "</clipPath>"
    layer = ('<g clip-path="url(#clip)" pointer-events="none"><g transform="skewX(-20)">'
             '<rect id="shine" x="0" y="-100" width="260" height="1200" fill="url(#shine-grad)"/></g></g>')
    css = (f"#shine {{ transform: translateX(-500px); animation: shine {dur}s ease-in-out {start}s forwards; }}"
           "@keyframes shine { to { transform: translateX(1700px); } }")
    return SHINE + clip, layer, css


# swing: beam rotates about the pivot, pans counter-rotate so they stay level
def swing_css(start, dur, steps):
    kf_arm = " ".join(f"{p}% {{ transform: rotate({t}deg); }}" for p, t in steps)
    kf_side = " ".join(f"{p}% {{ transform: rotate({-t}deg); }}" for p, t in steps)
    return f"""
#arm, #side-l, #side-r {{ transform-box: view-box; }}
#arm {{ transform-origin: {PX}px {PY}px; animation: swing {dur}s ease-in-out {start}s both; }}
#side-l {{ transform-origin: {LX}px {LY}px; animation: unswing {dur}s ease-in-out {start}s both; }}
#side-r {{ transform-origin: {RX}px {RY}px; animation: unswing {dur}s ease-in-out {start}s both; }}
@keyframes swing {{ {kf_arm} }}
@keyframes unswing {{ {kf_side} }}"""


REDUCED = """
@media (prefers-reduced-motion: reduce) {
  *, *::before { animation-duration: 1ms !important; animation-delay: 0s !important; }
}"""
BOX = "#logo g, #logo path { transform-box: fill-box; }"

files = {}

# ---------- static ----------
files["logo.svg"] = svg(body())
files["logo-white.svg"] = svg(body("#FFFFFF"))
files["logo-black.svg"] = svg(body("#1A1A1A"))

# ---------- 1. draw: outlines are inked, then gilded ----------
delays = {"pillar": 0, "knob": .15, "beam": .2, "hanger-left": .55, "hanger-right": .55,
          "pan-left": .75, "pan-right": .75, "title": .9, "name": 1.1, "subtitle": 1.4, "ornament": 1.6}
d, layer, scss = shine_layer(4.2)
css = """
#logo .p { stroke: url(#gold); stroke-width: 2.5; stroke-linejoin: round; stroke-dasharray: 1 1;
  stroke-dashoffset: 1; fill-opacity: 0;
  animation: draw 1.8s cubic-bezier(.6,.05,.3,1) forwards, gild 1s ease forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
@keyframes gild { to { fill-opacity: 1; stroke-opacity: 0; } }
""" + "\n".join(f"#logo #p-{k} {{ animation-delay: {v}s, {v + 1.5}s; }}" for k, v in delays.items()) + scss + REDUCED
files["anim-1-draw.svg"] = svg(body(draw=True) + layer, d, css)

# ---------- 2. balance: stand rises, beam drops in and finds its balance ----------
css = BOX + """
#stand { transform-origin: 50% 100%; animation: rise .8s cubic-bezier(.2,.8,.2,1) both; }
#drop  { animation: drop .9s cubic-bezier(.3,1.4,.5,1) .6s both; }
@keyframes rise { from { transform: scaleY(0); } }
@keyframes drop { from { transform: translateY(-260px); opacity: 0; } to { opacity: 1; } }
.word, #orn { animation: up .9s cubic-bezier(.2,.8,.2,1) both; }
#title { animation-delay: 2.6s; } #name { animation-delay: 2.8s; } #sub { animation-delay: 3.05s; } #orn { animation-delay: 3.25s; }
@keyframes up { from { opacity: 0; transform: translateY(40px); } }
""" + swing_css(1.3, 2.6, [(0, 0), (18, 9), (40, -6), (60, 3.5), (78, -1.4), (90, .5), (100, 0)]) + REDUCED
files["anim-2-balance.svg"] = svg(body(), "", css)

# ---------- 3. write: words are written right-to-left like a pen ----------
d, layer, scss = shine_layer(4.0)
css = BOX + """
#scale { animation: zoom 1s cubic-bezier(.2,.8,.2,1) both; transform-origin: 50% 50%; }
@keyframes zoom { from { opacity: 0; transform: scale(.85); } }
.word { clip-path: inset(-20% -5% -20% 105%); animation: write 1.2s cubic-bezier(.55,.1,.3,1) forwards; }
#title { animation-delay: .7s; } #name { animation-delay: 1.4s; animation-duration: 1.5s; } #sub { animation-delay: 2.6s; }
@keyframes write { to { clip-path: inset(-20% -5% -20% -5%); } }
#ornament { transform-box: fill-box; transform-origin: 50% 50%; animation: grow .9s cubic-bezier(.2,.8,.2,1) 3.4s both; }
@keyframes grow { from { transform: scaleX(0); opacity: 0; } }
""" + scss + REDUCED
files["anim-3-write.svg"] = svg(body() + layer, d, css)

# ---------- 4. shine: soft focus-in, then a sweep of light and sparkles ----------
d, layer, scss = shine_layer(1.9, 1.5)
spark = lambda x, y, s, t: (f'<g transform="translate({x} {y})"><path class="spark" style="animation-delay:{t}s" '
                            f'd="M0 {-s}C{s*.12} {-s*.12} {s*.12} {-s*.12} {s} 0C{s*.12} {s*.12} {s*.12} {s*.12} 0 {s}'
                            f'C{-s*.12} {s*.12} {-s*.12} {s*.12} {-s} 0C{-s*.12} {-s*.12} {-s*.12} {-s*.12} 0 {-s}Z"/></g>')
sparks = '<g fill="#FFF3C4" stroke="#D9A521" stroke-width="2">' + spark(PX, 172, 34, 2.4) + spark(LX - 30, PY - 12, 26, 2.1) + \
         spark(RX + 30, PY - 12, 26, 2.7) + spark(690, 560, 30, 3.0) + spark(330, 845, 22, 3.3) + "</g>"
css = BOX + """
#logo { animation: focus 1.6s cubic-bezier(.2,.8,.2,1) both; transform-origin: 500px 500px; }
@keyframes focus { from { opacity: 0; filter: blur(18px); transform: scale(1.08); } }
.spark { transform-box: fill-box; transform-origin: 50% 50%; opacity: 0; animation: twinkle 1s ease-in-out both; }
@keyframes twinkle { 0% { opacity: 0; transform: scale(0) rotate(0); } 50% { opacity: 1; transform: scale(1) rotate(45deg); }
  100% { opacity: 0; transform: scale(0) rotate(90deg); } }
""" + scss + REDUCED
files["anim-4-shine.svg"] = svg(body() + layer + sparks, d, css)

# ---------- 5. assemble: every part flies in from its own direction ----------
moves = {"stand": "translateY(420px)", "p-knob": "translateY(-300px) scale(0)", "p-beam": "scaleX(0)",
         "side-l": "translate(-420px,-60px) rotate(-30deg)", "side-r": "translate(420px,-60px) rotate(30deg)",
         "title": "translateY(-200px)", "name": "translateX(-600px)", "sub": "translateX(600px)",
         "orn": "scaleX(0)"}
delays = {"stand": 0, "p-beam": .35, "p-knob": .55, "side-l": .7, "side-r": .8, "title": 1.2, "name": 1.4,
          "sub": 1.6, "orn": 1.9}
d, layer, scss = shine_layer(3.5)
css = BOX + "".join(
    f"#{k} {{ transform-origin: 50% 50%; animation: in-{k} .9s cubic-bezier(.3,1.35,.5,1) {delays[k]}s both; }}"
    f"@keyframes in-{k} {{ from {{ transform: {v}; opacity: 0; }} 40% {{ opacity: 1; }} }}"
    for k, v in moves.items()) + scss + REDUCED
files["anim-5-assemble.svg"] = svg(body(), d, css)

# ---------- 6. seal: logo is stamped in with a golden ripple ----------
ring = ('<g fill="none" stroke="url(#gold)">'
        '<circle id="ring1" cx="500" cy="500" r="470" stroke-width="6" pathLength="1"/>'
        '<circle id="ring2" cx="500" cy="500" r="440" stroke-width="2" pathLength="1"/>'
        '<circle id="ripple" cx="500" cy="500" r="300" stroke-width="10"/></g>')
css = BOX + """
#logo { transform-origin: 500px 500px; animation: stamp .7s cubic-bezier(.5,0,.75,0) .2s both, settle .5s cubic-bezier(.2,1.6,.4,1) .9s both; }
@keyframes stamp { from { transform: scale(2.2); opacity: 0; } to { transform: scale(.94); opacity: 1; } }
@keyframes settle { from { transform: scale(.94); } to { transform: scale(1); } }
#ripple { transform-origin: 500px 500px; transform-box: view-box; opacity: 0; animation: ripple 1.2s cubic-bezier(.1,.7,.3,1) .9s both; }
@keyframes ripple { from { transform: scale(.6); opacity: 0; } 8% { opacity: .9; } to { transform: scale(1.75); opacity: 0; stroke-width: 1; } }
#ring1, #ring2 { stroke-dasharray: 1 1; stroke-dashoffset: 1; transform-origin: 500px 500px; transform-box: view-box;
  transform: rotate(-90deg); animation: ring 1.6s cubic-bezier(.6,.05,.3,1) both; }
#ring1 { animation-delay: 1.1s; } #ring2 { animation-delay: 1.35s; animation-direction: normal; }
@keyframes ring { to { stroke-dashoffset: 0; } }
""" + REDUCED
d, layer, scss = shine_layer(2.9)
files["anim-6-seal.svg"] = svg(ring + '<g transform="translate(500 500) scale(.78) translate(-500 -500)">' + body() + layer + "</g>", d, css + scss)

for name, content in files.items():
    open(os.path.join(OUT, name), "w").write(content)
print("\n".join(files))
