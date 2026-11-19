#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme picture (1200x800 PNG).

Scene: a Vice City sunset over the Leonida shore. The rising sun IS make.fun's
ghost (the press-kit mark, mark-1024.png, is a magenta disc with the ghost on
it), so the mascot is worked into the scene itself, huge and recognisable even
at 480x480. Below: a game loading bar at 100% for "LEONIDA", palm and skyline
silhouettes, and the caption:

    WAITED 13 YEARS FOR THIS SUNRISE
    MY AI AGENT GOT PAID ON make.fun WHILE I WAITED

Everything except the make.fun mark is painted here with Pillow; no Rockstar
artwork, logos or fonts are used. Deterministic: fixed random seed.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 800
HORIZON = 478          # where sky meets ocean
BEACH_Y = 606          # where ocean meets the shore band
random.seed(20261119)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def vgrad(w, h, stops):
    """Vertical gradient image from [(y_frac, (r,g,b)), ...]."""
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        f = y / max(h - 1, 1)
        for i in range(len(stops) - 1):
            f0, c0 = stops[i]
            f1, c1 = stops[i + 1]
            if f0 <= f <= f1:
                t = 0 if f1 == f0 else (f - f0) / (f1 - f0)
                px[0, y] = tuple(round(c0[j] + (c1[j] - c0[j]) * t) for j in range(3))
                break
        else:
            px[0, y] = stops[-1][1]
    return strip.resize((w, h))


img = vgrad(W, H, [
    (0.00, (24, 10, 54)),     # deep purple night top
    (0.30, (88, 28, 110)),    # purple
    (0.52, (178, 44, 122)),   # magenta band (brand-adjacent)
    (0.60, (240, 96, 84)),    # orange-pink
    (0.66, (255, 166, 88)),   # orange at horizon
    (0.68, (38, 60, 96)),     # ocean starts (drawn over below anyway)
    (1.00, (16, 6, 28)),
])
d = ImageDraw.Draw(img, "RGBA")

# --- stars in the upper sky -------------------------------------------------
for _ in range(90):
    x, y = random.uniform(0, W), random.uniform(0, 250)
    r = random.uniform(0.8, 2.0)
    a = int(160 * (1 - y / 280))
    if a > 8:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))

# --- sun glow, then the make.fun ghost disc as the sun ----------------------
SUN_C = (600, 352)
SUN_R = 238
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r, a in [(SUN_R + 130, 46), (SUN_R + 84, 66), (SUN_R + 40, 84)]:
    gd.ellipse([SUN_C[0] - r, SUN_C[1] - r, SUN_C[0] + r, SUN_C[1] + r],
               fill=(255, 140, 66, a))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow.filter(
    ImageFilter.GaussianBlur(38))).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

mark = Image.open("assets/mark-1024.png").convert("RGBA")
disc = mark.resize((SUN_R * 2, SUN_R * 2), Image.LANCZOS)
mask = Image.new("L", disc.size, 0)
ImageDraw.Draw(mask).ellipse([0, 0, disc.size[0], disc.size[1]], fill=255)
alpha = disc.split()[3]
alpha = Image.composite(alpha, Image.new("L", disc.size, 0), mask)
disc.putalpha(alpha)
img.paste(disc, (SUN_C[0] - SUN_R, SUN_C[1] - SUN_R), disc)
d = ImageDraw.Draw(img, "RGBA")

# --- skyline silhouettes along the horizon (Leonida), both sides ------------
def skyline(x0, x1):
    x = x0
    while x < x1:
        bw = random.randint(26, 58)
        bh = random.randint(34, 118)
        if abs((x + bw / 2) - SUN_C[0]) < SUN_R + 26:   # keep the sun clear
            x += bw + random.randint(2, 8)
            continue
        d.rectangle([x, HORIZON - bh, x + bw, HORIZON + 2], fill=(22, 8, 40, 255))
        for _ in range(bw * bh // 260):
            wx, wy = x + random.uniform(4, bw - 7), HORIZON - bh + random.uniform(5, bh - 10)
            d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 209, 102, 220))
        x += bw + random.randint(2, 8)

skyline(0, 470)
skyline(730, W)

# --- ocean ------------------------------------------------------------------
ocean = vgrad(W, BEACH_Y - HORIZON, [
    (0.0, (64, 44, 92)),
    (0.25, (40, 52, 96)),
    (1.0, (22, 26, 62)),
])
img.paste(ocean, (0, HORIZON))
d = ImageDraw.Draw(img, "RGBA")
# sun reflection: broken bright streaks under the sun
for i in range(64):
    y = HORIZON + 6 + i * 1.9
    half = 150 * (1 - i / 90) + random.uniform(-24, 24)
    cx = SUN_C[0] + random.uniform(-16, 16)
    col = (255, 150 + int(60 * random.random()), 80, 150)
    d.line([cx - half, y, cx + half, y], fill=col, width=2)
# general shimmer
for _ in range(240):
    x, y = random.uniform(0, W), random.uniform(HORIZON + 4, BEACH_Y - 4)
    ln = random.uniform(6, 30)
    d.line([x, y, x + ln, y], fill=(255, 255, 255, 34), width=1)

# --- shore band ---------------------------------------------------------------
shore = vgrad(W, H - BEACH_Y, [(0.0, (34, 16, 52)), (1.0, (14, 5, 24))])
img.paste(shore, (0, BEACH_Y))
d = ImageDraw.Draw(img, "RGBA")
d.line([0, BEACH_Y, W, BEACH_Y], fill=(255, 190, 110, 160), width=2)

# --- palm silhouettes ---------------------------------------------------------
INK = (13, 4, 24, 255)

def palm(bx, by, h, lean):
    pts = []
    for i in range(21):
        t = i / 20
        pts.append((bx + lean * t * t, by - h * t))
    for i in range(len(pts) - 1):
        wdt = max(3, int(13 * (1 - i / 22)))
        d.line([pts[i], pts[i + 1]], fill=INK, width=wdt)
    cx, cy = pts[-1]
    for ang in (-168, -140, -112, -84, -56, -28, -4):
        L = h * 0.34
        seg = 9
        prev = (cx, cy)
        for s in range(1, seg + 1):
            t = s / seg
            a = math.radians(ang + 52 * t)
            p = (cx + math.cos(a) * L * t, cy + math.sin(a) * L * t + 26 * t * t)
            d.line([prev, p], fill=INK, width=5)
            prev = p
    d.ellipse([cx - 10, cy - 2, cx + 4, cy + 12], fill=INK)
    d.ellipse([cx + 2, cy + 2, cx + 15, cy + 15], fill=INK)

palm(96, BEACH_Y + 26, 330, 66)
palm(1112, BEACH_Y + 22, 292, -58)

# --- birds --------------------------------------------------------------------
for bx, by, s in [(268, 128, 13), (330, 102, 10), (905, 118, 12), (962, 92, 9)]:
    d.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 330, fill=INK, width=3)
    d.arc([bx, by - s // 2, bx + s, by + s // 2], 210, 340, fill=INK, width=3)

# --- loading bar ---------------------------------------------------------------
BAR = (96, 622, 1104, 676)
d.rounded_rectangle(BAR, radius=16, fill=(10, 4, 18, 255),
                    outline=(255, 255, 255, 255), width=5)
fill_img = vgrad(BAR[2] - BAR[0] - 16, BAR[3] - BAR[1] - 16,
                 [(0.0, (255, 170, 60)), (1.0, (255, 170, 60))])
# horizontal magenta->orange fill
fill_img = Image.new("RGB", fill_img.size)
fp = fill_img.load()
for x in range(fill_img.size[0]):
    t = x / fill_img.size[0]
    c = tuple(round((196, 28, 131)[j] + ((255, 150, 62)[j] - (196, 28, 131)[j]) * t)
              for j in range(3))
    for y in range(fill_img.size[1]):
        fp[x, y] = c
fmask = Image.new("L", fill_img.size, 0)
ImageDraw.Draw(fmask).rounded_rectangle([0, 0, fill_img.size[0], fill_img.size[1]],
                                        radius=10, fill=255)
img.paste(fill_img, (BAR[0] + 8, BAR[1] + 8), fmask)
d = ImageDraw.Draw(img, "RGBA")


def fit(text, max_w, start, stroke=0):
    size = start
    while size > 10:
        f = ImageFont.truetype(BOLD, size)
        if d.textlength(text, font=f) + 2 * stroke <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(BOLD, size)


def centered(text, y, start, fill, stroke_w, stroke_fill=(8, 2, 14, 255)):
    f = fit(text, W - 90, start, stroke_w)
    tw = d.textlength(text, font=f)
    d.text(((W - tw) / 2, y), text, font=f, fill=fill,
           stroke_width=stroke_w, stroke_fill=stroke_fill)
    return f.size


# bar labels (dark on the bright fill)
f_bar = ImageFont.truetype(BOLD, 34)
d.text((BAR[0] + 26, BAR[1] + 8), "LEONIDA", font=f_bar, fill=(26, 4, 20, 255))
pct = "100%"
tw = d.textlength(pct, font=f_bar)
d.text((BAR[2] - 26 - tw, BAR[1] + 8), pct, font=f_bar, fill=(26, 4, 20, 255))

# --- captions -------------------------------------------------------------------
centered("WAITED 13 YEARS FOR THIS SUNRISE", 30, 84, (255, 255, 255, 255), 9)
centered("MY AI AGENT GOT PAID ON make.fun", 690, 58, (255, 209, 102, 255), 8)
centered("WHILE I WAITED", 750, 38, (255, 255, 255, 255), 6)

img.save("meme.png")
print("saved meme.png", img.size)
