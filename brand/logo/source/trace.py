import sys, json
import cv2, numpy as np, potrace

src = sys.argv[1]
im = cv2.imread(src)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
# soft mask from saturation, upsample-free smoothing for clean edges
s = hsv[:, :, 1].astype(np.float32)
s = cv2.GaussianBlur(s, (0, 0), 1.6)
mask = (s > 60).astype(np.uint8)

n, lab, st, _ = cv2.connectedComponentsWithStats(mask)
H, W = mask.shape
yy, xx = np.mgrid[0:H, 0:W]

def comp_at(x, y):
    return lab[y, x]

groups = {k: np.zeros_like(mask) for k in
          ["title", "beam", "hanger-left", "hanger-right", "pan-left", "pan-right", "name", "subtitle"]}

for i in range(1, n):
    x, y, w, h, a = st[i]
    if a < 150:
        continue
    c = (lab == i)
    cx, cy = x + w / 2, y + h / 2
    if y + h < 420:
        groups["title"][c] = 1
    elif h > 1000:  # big merged piece: beam + hangers + pillar + name
        beam = c & (yy < 590)
        hl = c & (yy >= 590) & (yy < 880) & (xx < 1100)
        hr = c & (yy >= 590) & (yy < 880) & (xx > 1300)
        groups["beam"][beam] = 1
        groups["hanger-left"][hl] = 1
        groups["hanger-right"][hr] = 1
        groups["name"][c & ~beam & ~hl & ~hr] = 1
    elif 840 < y < 900 and h < 120:
        groups["pan-left" if cx < 1000 else "pan-right"][c] = 1
    elif y > 1400:
        groups["subtitle"][c] = 1
    else:
        groups["name"][c] = 1

def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")

def trace(m):
    bm = potrace.Bitmap(~m.astype(bool))
    plist = bm.trace(turdsize=20, alphamax=1.0, opticurve=True, opttolerance=0.25)
    out = []
    for curve in plist:
        p = curve.start_point
        d = [f"M{f(p.x)} {f(p.y)}"]
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f"L{f(seg.c.x)} {f(seg.c.y)}L{f(seg.end_point.x)} {f(seg.end_point.y)}")
            else:
                d.append(f"C{f(seg.c1.x)} {f(seg.c1.y)} {f(seg.c2.x)} {f(seg.c2.y)} {f(seg.end_point.x)} {f(seg.end_point.y)}")
        d.append("Z")
        out.append("".join(d))
    return "".join(out)

res = {k: trace(m) for k, m in groups.items()}
json.dump(res, open(sys.argv[2], "w"))
for k, v in res.items():
    print(k, len(v))
