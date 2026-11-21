"""Generate news.png for make.fun news-image-20261120 (20 Nov 2026).
Illustrated front page, following ~/workspace/custom-skills/news-image-quality/SKILL.md.
Deterministic: fixed text, fixed colours, fixed layout, fixed asset files,
no network, no time. Run once locally; the submitted main.py only copies
the generated PNG.

Stories (verified 2026-11-21 via AP / Reuters / CNN / ISW / Investopedia):
 - Lead: Russian Kh-101 missiles + a jet-powered drone crash in Poland
   during the overnight 19-20 Nov attack on Ukraine; Tusk: "intentional
   provocation"; NATO's Rutte: "grave violation"; no injuries; NATO jets
   scrambled, Patriots activated. Hours after Trump, Putin and Xi met
   in Shenzhen, China.
 - Ukraine: 400+ drones and 110+ missiles in a single night (27 ballistic),
   8+ killed; three Kyiv bridges hit, power cut.
 - COP31 Antalya: draft deal drops all fossil-fuel references, talks spill
   into overtime on Friday, no deal in sight.
 - Wall Street AI rout: Nasdaq -5.3%, erases its 2026 gains; S&P 500 -3.7%
   into correction, down 10% from its high; Nvidia -14%.
 - Denmark expels Russia's defence attache over an alleged plot to kill a
   Ukrainian-American rapper; two arrested.
 - Saudi forces intercept a Houthi missile over Riyadh.

Geometry (same proven layout as the 21 Nov v2): thumbnail 100 + title
bar 34 + body 82 = 216 per grid row, body 19pt / 24px line height,
3 lines max, pixel-measured wrap. Hero cropped with centering
(0.5, 0.32) so the missile, drone and jets stay inside the frame.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
W = H = 1024
CREAM = (247, 243, 232)
INK = (17, 24, 39)
DARKRED = (185, 28, 28)
GOLD = (253, 203, 88)
WHITE = (255, 255, 255)
BODY = (31, 41, 55)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(p, s):
    return ImageFont.truetype(p, s)


def wrap_px(d, text, f, max_w):
    """Greedy word wrap measured in pixels, so no line ever overflows."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=f) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur or not lines:
            lines.append(cur)
    return lines


def draw_lines(d, x, y, text, f, fill, max_w, lh):
    for line in wrap_px(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def fit(path, w, h, cy=0.45):
    im = Image.open(path).convert("RGB")
    return ImageOps.fit(im, (w, h), method=Image.LANCZOS, centering=(0.5, cy))


def draw_riyadh_panel(w, h):
    """Pillow-drawn thumbnail for Denmark + Riyadh: night desert skyline,
    a missile streak crossing the sky and an interception burst.
    Fully filled, no text, no empty area."""
    im = Image.new("RGB", (w, h), (10, 22, 48))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=(
            int(10 + 40 * t), int(22 + 30 * t), int(48 + 55 * t)))
    for sx, sy in [(28, 14), (70, 30), (120, 10), (180, 26), (240, 12),
                   (300, 32), (360, 14), (420, 28), (52, 44), (330, 48)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 244, 200))
    # interception streak + burst, kept inside the panel
    d.line([(40, 88), (400, 30)], fill=(255, 190, 80), width=5)
    d.line([(40, 88), (400, 30)], fill=(255, 255, 255), width=2)
    bx, by = 400, 30
    for r, col in [(24, (255, 190, 80)), (14, (255, 230, 150)), (7, (255, 255, 255))]:
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    for dx, dy in [(-30, -8), (-24, 14), (-34, 4), (-18, -16)]:
        d.line([(bx, by), (bx + dx, by + dy)], fill=(255, 210, 110), width=2)
    buildings = [(0, 62, 58, 100), (52, 48, 96, 100), (92, 70, 150, 100),
                 (146, 40, 186, 100), (182, 66, 240, 100), (236, 52, 282, 100),
                 (278, 72, 330, 100), (326, 46, 368, 100), (364, 68, 420, 100),
                 (416, 56, 476, 100)]
    for x0, y0, x1, y1 in buildings:
        d.rectangle([x0, y0, x1, y1], fill=(6, 14, 32))
        for wy in range(y0 + 8, y1 - 6, 12):
            for wx in range(x0 + 7, x1 - 7, 14):
                if (wx * 7 + wy * 3) % 5 < 2:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 200, 90))
    return im


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 92], fill=INK)
d.text((24, 10), "THE WORLD TODAY", font=font(SERIFB, 58), fill=WHITE)
d.text((24, 70), "FRIDAY  •  20 NOVEMBER 2026  •  ONE IMAGE, SIX STORIES",
       font=font(BOLD, 17), fill=GOLD)
d.rectangle([0, 92, W, 98], fill=DARKRED)

# ---- lead: hero image, kicker, headline, deck, quote strip ----
LX0, LX1 = 24, 1000
img.paste(fit(os.path.join(ASSETS,
    "media-generation-hero-poland-0-fe62b10d-b872-4179-a489-920f7aed9053.webp"),
    LX1 - LX0, 200, cy=0.32), (LX0, 106))
d.rectangle([LX0, 306, LX1, 338], fill=DARKRED)
d.text((LX0 + 16, 313), "LEAD  •  NATO ON ALERT", font=font(BOLD, 21), fill=WHITE)
d.text((LX0 + 16, 348), "RUSSIAN MISSILES", font=font(SERIFB, 44), fill=INK)
d.text((LX0 + 16, 396), "LAND IN POLAND", font=font(SERIFB, 44), fill=INK)
draw_lines(d, LX0 + 16, 444,
           "Two Kh-101 missiles and a drone crash in Poland during a huge "
           "attack on Ukraine. NATO jets scrambled.",
           font(REG, 20), BODY, LX1 - LX0 - 32, 25)
d.rectangle([LX0, 494, LX1, 526], fill=INK)
d.text((LX0 + 16, 501),
       "Tusk: “intentional provocation”  •  Rutte: “grave violation”  •  No injuries",
       font=font(BOLD, 18), fill=WHITE)

# ---- 2x2 grid: thumbnail 100 + title bar 34 + body 82 = 216 per row ----
stories = [
    ("UKRAINE UNDER FIRE", DARKRED,
     os.path.join(ASSETS,
        "media-generation-thumb-ukraine-0-3a90ba75-a905-4c18-a338-4cd695a7b3db.webp"),
     "400+ drones and 110+ missiles\nin a single night. 8+ killed;\nbridges hit, power cut."),
    ("COP31 STALLS", (4, 120, 87),
     os.path.join(ASSETS,
        "media-generation-thumb-cop31-0-53cf64c7-23ff-434e-926d-7176230903d6.webp"),
     "Climate talks in Antalya\nstall into overtime. Draft\ndrops fossil fuels."),
    ("WALL ST. AI ROUT", (120, 53, 15),
     os.path.join(ASSETS,
        "media-generation-thumb-markets-0-9141e43a-0e57-4c45-b37a-34df29678bfa.webp"),
     "Nasdaq plunges 5.3%, erases\nits 2026 gains. S&P 500 sinks\ninto correction, down 10%."),
    ("DENMARK  •  RIYADH", (30, 64, 175),
     None,
     "Denmark expels Russia's\nenvoy. Saudi forces intercept\na Houthi missile over Riyadh."),
]
boxes = [(24, 538, 500, 754), (524, 538, 1000, 754),
         (24, 766, 500, 982), (524, 766, 1000, 982)]
for (x0, y0, x1, y1), (title, col, thumb, body) in zip(boxes, stories):
    bw = x1 - x0
    d.rectangle([x0, y0, x1, y1], fill=WHITE)
    if thumb:
        img.paste(fit(thumb, bw, 100), (x0, y0))
    else:
        img.paste(draw_riyadh_panel(bw, 100), (x0, y0))
    d.rectangle([x0, y0 + 100, x1, y0 + 134], fill=col)
    d.text((x0 + 12, y0 + 107), title, font=font(BOLD, 22), fill=WHITE)
    draw_lines(d, x0 + 12, y0 + 142, body, font(REG, 19), BODY, bw - 24, 24)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=3)

# ---- footer ----
d.rectangle([0, 990, W, 1024], fill=INK)
d.text((24, 998),
       "Sources: AP / Reuters, 20 Nov 2026  •  All six stories happened on 19–20 Nov 2026",
       font=font(REG, 15), fill=WHITE)

img.save(os.path.join(HERE, "news.png"), format="PNG", optimize=True, compress_level=9)
print("saved")
