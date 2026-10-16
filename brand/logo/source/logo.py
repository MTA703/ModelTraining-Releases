"""Al-Nasr Law Firm — new logo, constructed from scratch.

Geometry of the scale is hand-built; the Arabic lettering is set in Aref Ruqaa
(SIL OFL) and converted to outlines so the SVG has no font dependency.
Outputs a dict of named parts (path data) + pivot/anchor metadata.
"""
import json, sys
from textpath import text_path

FONT = "ArefRuqaa-Bold.ttf"
CX = 500

def r(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")

def P(*pts):
    return " ".join(r(p) if isinstance(p, (int, float)) else p for p in pts)

# ---------------- scale ----------------
KNOB = (CX, 172)
BEAM_Y = 220
ARM = 235                       # half-span of the beam
LX, RX = CX - ARM, CX + ARM
PAN_Y = 382                     # rim of pans
PAN_W = 92                      # half-width of pans
PIVOT = (CX, BEAM_Y)

knob = (f"M{P(CX, KNOB[1]-19)}a19 19 0 1 1 -0.01 0Z"
        # neck that flows into the beam
        f"M{P(CX-7, KNOB[1]+15)}C{P(CX-6, BEAM_Y-26, CX-16, BEAM_Y-16, CX-19, BEAM_Y-10)}L{P(CX+19, BEAM_Y-10)}"
        f"C{P(CX+16, BEAM_Y-16, CX+6, BEAM_Y-26, CX+7, KNOB[1]+15)}Z")

def beam_half(sign):
    # tapered arm that sweeps slightly upwards to a teardrop finial
    s = sign
    x = lambda dx: CX + s * dx
    return (f"M{P(x(0), BEAM_Y-11)}"
            f"C{P(x(80), BEAM_Y-12, x(160), BEAM_Y-16, x(ARM-30), BEAM_Y-14)}"
            f"C{P(x(ARM-14), BEAM_Y-28, x(ARM+22), BEAM_Y-30, x(ARM+30), BEAM_Y-12)}"
            f"C{P(x(ARM+36), BEAM_Y+4, x(ARM+12), BEAM_Y+16, x(ARM-8), BEAM_Y+10)}"
            f"C{P(x(ARM-20), BEAM_Y+7, x(ARM-26), BEAM_Y+4, x(ARM-34), BEAM_Y+3)}"
            f"C{P(x(160), BEAM_Y+3, x(80), BEAM_Y+9, x(0), BEAM_Y+11)}Z")

beam = beam_half(-1) + beam_half(1)

# pillar with a capital under the beam and a stepped base
TOP, BOT = BEAM_Y + 10, 468
pillar = (
    # capital
    f"M{P(CX-30, TOP)}L{P(CX+30, TOP)}C{P(CX+30, TOP+10, CX+20, TOP+14, CX+12, TOP+18)}"
    f"L{P(CX-12, TOP+18)}C{P(CX-20, TOP+14, CX-30, TOP+10, CX-30, TOP)}Z"
    # ring
    f"M{P(CX-17, TOP+17)}h34v10h-34Z"
    # shaft (gentle entasis)
    f"M{P(CX-10, TOP+26)}C{P(CX-12, 330, CX-13, 400, CX-15, BOT-28)}"
    f"L{P(CX+15, BOT-28)}C{P(CX+13, 400, CX+12, 330, CX+10, TOP+26)}Z"
    # base steps
    f"M{P(CX-40, BOT-28)}h80c0 8-6 14-14 14h-52c-8 0-14-6-14-14Z"
    f"M{P(CX-78, BOT-14)}h156c0 8-6 14-14 14h-128c-8 0-14-6-14-14Z"
)

def hanger(ax):
    # three tapered cords meeting in a small ring under the finial
    ry = BEAM_Y + 14
    out = f"M{P(ax, ry+8)}a8 8 0 1 1 0.01 0Z"
    for ex in (-PAN_W + 8, 0, PAN_W - 8):
        tx = ax + ex
        w0, w1 = 2.2, 3.4
        out += (f"M{P(ax - w0, ry+14)}L{P(tx - w1, PAN_Y)}L{P(tx + w1, PAN_Y)}"
                f"L{P(ax + w0, ry+14)}Z")
    return out

def pan(ax):
    # shallow bowl with a lip
    return (f"M{P(ax-PAN_W-10, PAN_Y)}h{r(2*PAN_W+20)}c0 6-3 9-8 10"
            f"C{P(ax+PAN_W-6, PAN_Y+48, ax+40, PAN_Y+62, ax, PAN_Y+62)}"
            f"C{P(ax-40, PAN_Y+62, ax-PAN_W+6, PAN_Y+48, ax-PAN_W-2, PAN_Y+10)}"
            f"c-5-1-8-4-8-10Z")

# ---------------- lettering ----------------
title, tb = text_path("مؤسسة", FONT, 120, CX, 118)
name, nb = text_path("النصر", FONT, 280, CX, 722)
sub, sb = text_path("للمحاماة", FONT, 125, CX, 935)

# ornament: two hairlines with diamonds flanking "للمحاماة"
def rule(x1, x2, y):
    sx = 1 if x2 > x1 else -1
    return (f"M{P(x1, y-1.6)}L{P(x2, y-1.6)}L{P(x2, y+1.6)}L{P(x1, y+1.6)}Z"
            f"M{P(x2 + sx*4, y)}l{r(sx*9)} -9l{r(sx*9)} 9l{r(-sx*9)} 9Z")

orn_y = 900
ornament = rule(sb[0] - 30, sb[0] - 150, orn_y) + rule(sb[2] + 30, sb[2] + 150, orn_y)

parts = {
    "title": title, "knob": knob, "beam": beam, "pillar": pillar,
    "hanger-left": hanger(LX), "hanger-right": hanger(RX),
    "pan-left": pan(LX), "pan-right": pan(RX),
    "name": name, "subtitle": sub, "ornament": ornament,
}
meta = {
    "pivot": PIVOT, "left": (LX, BEAM_Y + 14), "right": (RX, BEAM_Y + 14),
    "bounds": {"title": tb, "name": nb, "subtitle": sb},
}
json.dump({"parts": parts, "meta": meta}, open(sys.argv[1], "w"))
print(json.dumps(meta))
