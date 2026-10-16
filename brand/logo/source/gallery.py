"""Build the animation gallery page. usage: gallery.py <logo_dir> <out.html> [--inline]"""
import base64, sys, os

D, OUT = sys.argv[1], sys.argv[2]
INLINE = "--inline" in sys.argv

OPTIONS = [
    ("anim-1-draw", "رسم بالقلم", "حدود الشعار تترسم بخط ذهبي رفيع، وبعدين تتملي بالذهب ولمعة تعدّي عليه.", "5.5 ث"),
    ("anim-2-balance", "توازن الميزان", "العمود يطلع من تحت، والذراع تنزل وتتأرجح لحد ما الكفّتين يتوازنوا، وبعدها يظهر الاسم.", "4 ث"),
    ("anim-3-write", "كتابة من اليمين", "الميزان يظهر، والكلمات تتكتب من اليمين للشمال زي الخط العربي، والزخرفة تتمد.", "5.5 ث"),
    ("anim-4-shine", "لمعة ذهبية", "الشعار يوضح من ضباب ناعم، وبعدها لمعة ضوء ونجوم صغيرة بتلمع على الميزان.", "4.5 ث"),
    ("anim-5-assemble", "تجميع القطع", "كل جزء بييجي من اتجاه: الكفّتين من الجناب، والعمود من تحت، والكلام من الناحيتين.", "5 ث"),
    ("anim-6-seal", "الختم", "الشعار ينزل زي الختم مع موجة ذهبية، وحلقتين حواليه يترسموا زي الخاتم الرسمي.", "4.5 ث"),
]
STATIC = [("logo", "ذهبي", "light"), ("logo-white", "أبيض", "dark"), ("logo-black", "أسود", "light")]


def src(rel):
    if not INLINE:
        return rel
    data = open(os.path.join(D, rel), "rb").read()
    return "data:image/svg+xml;base64," + base64.b64encode(data).decode()


cards = "\n".join(f"""      <article class="card">
        <div class="stage"><img id="img-{k}" src="{src('animations/' + k + '.svg')}" alt="أنيميشن {t}" data-src="{src('animations/' + k + '.svg')}"></div>
        <div class="meta">
          <div class="row"><h2><span class="num">{i}</span>{t}</h2><span class="dur">{dur}</span></div>
          <p>{desc}</p>
          <div class="row foot"><code>{k}.svg</code><button type="button" class="replay" data-for="img-{k}">إعادة التشغيل</button></div>
        </div>
      </article>""" for i, (k, t, desc, dur) in enumerate(OPTIONS, 1))

statics = "\n".join(f"""      <figure class="swatch {bg}"><img src="{src(k + '.svg')}" alt="الشعار {t}"><figcaption>{t} · <code>{k}.svg</code></figcaption></figure>"""
                    for k, t, bg in STATIC)

html = f"""<title>شعار النصر للمحاماة</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Aref+Ruqaa:wght@700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap">
<style>
  /* Layout: a quiet archive wall — six equal stages, gold only on the marks themselves */
  :root {{
    --bg: #F3F2EE; --surface: #FFFFFF; --ink: #1E1D1A; --muted: #6B6658; --line: #DEDACF;
    --gold: #A97A08; --stage: #FFFFFF; --stage-alt: #15140F;
    --display: "Aref Ruqaa", "Amiri", serif;
    --body: "IBM Plex Sans Arabic", "Segoe UI", Tahoma, sans-serif;
    --mono: ui-monospace, "SFMono-Regular", Menlo, monospace;
  }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
    --bg: #12110E; --surface: #1B1A16; --ink: #EEE9DC; --muted: #A39C8A; --line: #2E2C25;
    --gold: #E2B947; --stage: #0D0C0A; --stage-alt: #FFFFFF; color-scheme: dark; }} }}
  :root[data-theme="dark"] {{
    --bg: #12110E; --surface: #1B1A16; --ink: #EEE9DC; --muted: #A39C8A; --line: #2E2C25;
    --gold: #E2B947; --stage: #0D0C0A; --stage-alt: #FFFFFF; color-scheme: dark; }}
  body {{ background: var(--bg); color: var(--ink); font-family: var(--body); font-size: 15px; line-height: 1.6; }}
  .wrap {{ max-width: 1180px; margin: 0 auto; padding-block: 40px 64px;
    padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
    display: grid; gap: 40px; }}
  header {{ display: flex; flex-wrap: wrap; align-items: end; justify-content: space-between; gap: 16px 32px; }}
  header .lead {{ display: grid; gap: 6px; min-width: 0; }}
  .eyebrow {{ color: var(--gold); font-weight: 600; font-size: 13px; }}
  h1 {{ font-family: var(--display); font-weight: 700; font-size: clamp(34px, 5vw, 52px); line-height: 1.15; margin: 0; text-wrap: balance; }}
  header p {{ margin: 0; color: var(--muted); max-width: 60ch; }}
  .controls {{ display: flex; flex-wrap: wrap; gap: 8px; }}
  button {{ font: inherit; font-size: 14px; font-weight: 500; color: var(--ink); background: var(--surface);
    border: 1px solid var(--line); border-radius: 999px; padding: 7px 16px; cursor: pointer; }}
  button:hover {{ border-color: var(--gold); color: var(--gold); }}
  button:focus-visible {{ outline: 2px solid var(--gold); outline-offset: 2px; }}
  button.primary {{ background: var(--gold); border-color: var(--gold); color: var(--surface); }}
  button.primary:hover {{ color: var(--surface); opacity: .9; }}
  .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; }}
  @media (max-width: 900px) {{ .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
  @media (max-width: 560px) {{ .grid {{ grid-template-columns: minmax(0, 1fr); }} }}
  .card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; display: grid; grid-template-rows: auto 1fr; }}
  .stage {{ background: var(--stage); aspect-ratio: 1; max-width: 100%; display: grid; place-items: center; border-bottom: 1px solid var(--line); transition: background .3s; }}
  body.alt .stage {{ background: var(--stage-alt); }}
  .stage img {{ width: 82%; height: auto; }}
  .meta {{ padding: 16px 18px 18px; display: grid; gap: 8px; align-content: start; min-width: 0; }}
  .row {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; }}
  .foot {{ margin-top: auto; padding-top: 4px; }}
  h2 {{ margin: 0; font-size: 18px; font-weight: 600; display: flex; align-items: center; gap: 10px; }}
  .num {{ font-family: var(--display); color: var(--gold); font-size: 22px; line-height: 1; }}
  .dur {{ color: var(--muted); font-size: 13px; font-variant-numeric: tabular-nums; white-space: nowrap; }}
  .meta p {{ margin: 0; color: var(--muted); font-size: 14px; }}
  code {{ font-family: var(--mono); font-size: 12px; color: var(--muted); direction: ltr; unicode-bidi: isolate; overflow-wrap: anywhere; }}
  section > h3 {{ font-size: 16px; font-weight: 600; margin: 0 0 14px; }}
  .swatches {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; margin: 0; }}
  @media (max-width: 560px) {{ .swatches {{ grid-template-columns: minmax(0, 1fr); }} }}
  .swatch {{ margin: 0; border: 1px solid var(--line); border-radius: 14px; overflow: hidden; background: var(--surface); }}
  .swatch img {{ display: block; width: 100%; aspect-ratio: 1; max-width: 100%; padding: 12%; box-sizing: border-box; background: #FFFFFF; }}
  .swatch.dark img {{ background: #15140F; }}
  figcaption {{ padding: 10px 14px; font-size: 14px; color: var(--muted); }}
</style>
<div class="wrap" dir="rtl" lang="ar">
  <header>
    <div class="lead">
      <span class="eyebrow">الهوية البصرية · مؤسسة النصر للمحاماة</span>
      <h1>اختار حركة الشعار</h1>
      <p>ست طرق مختلفة لظهور الشعار. اضغط «إعادة التشغيل» تحت أي واحدة عشان تشوفها من الأول، وجرّب الخلفية التانية عشان تشوف شكلها على الموقع والفيديو.</p>
    </div>
    <div class="controls">
      <button type="button" id="replay-all" class="primary">تشغيل الكل من الأول</button>
      <button type="button" id="toggle-bg">قلب لون الخلفية</button>
    </div>
  </header>
  <div class="grid">
{cards}
  </div>
  <section>
    <h3>الشعار الثابت</h3>
    <div class="swatches">
{statics}
    </div>
  </section>
</div>
<script>
  function replay(img) {{
    const s = img.dataset.src;
    img.src = s + '#r' + Date.now();
  }}
  document.querySelectorAll('.replay').forEach(b =>
    b.addEventListener('click', () => replay(document.getElementById(b.dataset.for))));
  document.getElementById('replay-all').addEventListener('click', () =>
    document.querySelectorAll('.stage img').forEach(replay));
  document.getElementById('toggle-bg').addEventListener('click', () => document.body.classList.toggle('alt'));
</script>
"""
if not INLINE:
    html = '<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n' + \
        html.replace("<style>", "<style>\n  body { margin: 0; }", 1).replace('<div class="wrap"', '</head>\n<body>\n<div class="wrap"', 1) + "</body>\n</html>\n"
open(OUT, "w").write(html)
print(OUT, len(html))
