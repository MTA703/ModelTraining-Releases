"""Shape Arabic text with HarfBuzz and return it as SVG outline path data."""
import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + os.sep
_cache = {}


def _load(name):
    if name not in _cache:
        path = FONTS + name
        blob = hb.Blob.from_file_path(path)
        _cache[name] = (hb.Font(hb.Face(blob)), TTFont(path))
    return _cache[name]


def text_path(text, font, size, cx, baseline, variations=None, kashida=None):
    """Return (d, bbox) for text centred horizontally on cx, baseline at y=baseline."""
    hbfont, tt = _load(font)
    if variations:
        hbfont.set_variations(variations)
    upem = tt["head"].unitsPerEm
    s = size / upem
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    gs = tt.getGlyphSet(location=variations) if variations else tt.getGlyphSet()
    order = tt.getGlyphOrder()
    # measure
    total = sum(p.x_advance for p in buf.glyph_positions)
    x0 = cx - total * s / 2
    pen = SVGPathPen(gs)
    bpen = BoundsPen(gs)
    x = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        g = order[info.codepoint]
        t = (s, 0, 0, -s, x0 + (x + pos.x_offset) * s, baseline - pos.y_offset * s)
        gs[g].draw(TransformPen(pen, t))
        gs[g].draw(TransformPen(bpen, t))
        x += pos.x_advance
    return pen.getCommands(), bpen.bounds
