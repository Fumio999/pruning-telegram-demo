"""Generates two flat-icon illustration PNGs for the pruning work-standard demo.

Each image: simple flat vector-style icon(s) + a short Khmer caption band.
No Japanese/English text in the artwork itself (numerals/degree symbols excepted).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).parent / "output"
OUT_DIR.mkdir(exist_ok=True)

SS = 2  # supersampling factor for smoother edges
SIZE = 1080 * SS

BG = (248, 246, 240)
GREEN = (66, 122, 75)
GREEN_DARK = (38, 74, 46)
STEM = (90, 140, 90)
BROWN = (124, 90, 62)
RED_CUT = (178, 60, 48)
BLUE = (74, 122, 163)
BLUE_LIGHT = (198, 219, 235)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
CAPTION_BG = (38, 74, 46)

KHMER_FONT = r"C:\Windows\Fonts\LeelawUI.ttf"
LABEL_FONT = r"C:\Windows\Fonts\arialbd.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * SS)


def rounded_line(draw, xy, width, fill):
    draw.line(xy, fill=fill, width=width, joint="curve")
    r = width // 2
    for x, y in (xy[0], xy[1]):
        draw.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def draw_caption_band(draw, text, canvas_size, khmer_size=64):
    band_h = int(canvas_size * 0.16)
    y0 = canvas_size - band_h
    draw.rectangle([0, y0, canvas_size, canvas_size], fill=CAPTION_BG)
    f = font(KHMER_FONT, khmer_size)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (canvas_size - tw) / 2 - bbox[0]
    ty = y0 + (band_h - th) / 2 - bbox[1]
    draw.text((tx, ty), text, font=f, fill=WHITE)


def draw_number_badge(draw, n, canvas_size):
    r = int(canvas_size * 0.045)
    cx, cy = int(canvas_size * 0.09), int(canvas_size * 0.09)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN_DARK)
    f = font(LABEL_FONT, int(r * 1.0 / SS))
    bbox = draw.textbbox((0, 0), str(n), font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), str(n), font=f, fill=WHITE)


def draw_shears(draw, cx, cy, scale, angle_deg, color=GRAY):
    import math
    a = math.radians(angle_deg)
    blade_len = 130 * scale
    handle_len = 110 * scale
    pivot = (cx, cy)

    for side in (-1, 1):
        bx = cx + side * blade_len * 0.35 * math.sin(a)
        by = cy - blade_len * math.cos(a)
        draw.polygon(
            [
                (pivot[0], pivot[1]),
                (pivot[0] + side * 14 * scale, pivot[1] - 6 * scale),
                (bx + side * 10 * scale, by),
                (cx, cy - blade_len),
            ],
            fill=color,
        )
        hx = cx + side * handle_len * 0.5
        hy = cy + handle_len * 0.85
        draw.line([pivot, (hx, hy)], fill=color, width=int(16 * scale))
        draw.ellipse(
            [hx - 22 * scale, hy - 22 * scale, hx + 22 * scale, hy + 22 * scale],
            outline=color,
            width=int(10 * scale),
        )
    draw.ellipse(
        [pivot[0] - 10 * scale, pivot[1] - 10 * scale, pivot[0] + 10 * scale, pivot[1] + 10 * scale],
        fill=GREEN_DARK,
    )


def make_image1():
    img = Image.new("RGB", (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)

    cx = SIZE // 2
    stem_bottom = int(SIZE * 0.86)
    stem_top = int(SIZE * 0.30)
    stem_w = int(SIZE * 0.028)

    d.line([(cx, stem_bottom), (cx, stem_top)], fill=STEM, width=stem_w)
    d.ellipse(
        [cx - stem_w // 2, stem_bottom - stem_w // 2, cx + stem_w // 2, stem_bottom + stem_w // 2],
        fill=STEM,
    )

    leaf_y = int(SIZE * 0.62)
    d.ellipse([cx - int(SIZE * 0.10), leaf_y - int(SIZE * 0.035),
               cx + int(SIZE * 0.02), leaf_y + int(SIZE * 0.035)], fill=STEM)
    d.ellipse([cx + int(SIZE * 0.02) - int(SIZE * 0.02), leaf_y + int(SIZE * 0.12) - int(SIZE * 0.035),
               cx + int(SIZE * 0.14), leaf_y + int(SIZE * 0.12) + int(SIZE * 0.035)], fill=STEM)

    bud_y = stem_top + int(SIZE * 0.02)
    d.ellipse([cx - int(SIZE * 0.022), bud_y - int(SIZE * 0.022),
               cx + int(SIZE * 0.022), bud_y + int(SIZE * 0.022)], fill=GREEN)

    cut_y = stem_top - int(SIZE * 0.015)
    dx = int(SIZE * 0.09)
    dy = int(SIZE * 0.09)
    d.line([(cx - dx, cut_y - dy), (cx + dx, cut_y + dy)], fill=RED_CUT, width=int(SIZE * 0.012))

    guide_len = int(SIZE * 0.11)
    d.line([(cx - dx, cut_y - dy), (cx - dx + guide_len, cut_y - dy)], fill=GRAY, width=int(SIZE * 0.004))
    f45 = font(LABEL_FONT, 46)
    d.text((cx - dx + guide_len + 10, cut_y - dy - 40), "45°", font=f45, fill=GRAY)

    draw_shears(d, int(SIZE * 0.76), int(SIZE * 0.40), scale=SS * 1.0, angle_deg=25, color=(110, 110, 110))

    drop_cx, drop_cy = int(SIZE * 0.80), int(SIZE * 0.52)
    r = int(SIZE * 0.018)
    d.polygon(
        [(drop_cx, drop_cy - r * 1.6), (drop_cx - r, drop_cy + r * 0.4),
         (drop_cx, drop_cy + r * 1.2), (drop_cx + r, drop_cy + r * 0.4)],
        fill=BLUE,
    )

    draw_number_badge(d, 1, SIZE)
    draw_caption_band(d, "កាត់មុំ ៤៥ អង្សា សំអាតឧបករណ៍កាត់", SIZE, khmer_size=52)

    img = img.resize((1080, 1080), Image.LANCZOS)
    img.save(OUT_DIR / "standard_1_cutting_technique.png")


def make_image2():
    img = Image.new("RGB", (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)
    cx = SIZE // 2

    BRISTLE = (196, 164, 90)

    handle_top = (cx - int(SIZE * 0.15), int(SIZE * 0.14))
    handle_bottom = (cx + int(SIZE * 0.01), int(SIZE * 0.32))
    d.line([handle_top, handle_bottom], fill=BROWN, width=int(SIZE * 0.018))

    bx, by = handle_bottom
    fan_w = int(SIZE * 0.11)
    fan_h = int(SIZE * 0.10)
    d.polygon(
        [(bx - int(SIZE * 0.02), by - int(SIZE * 0.01)),
         (bx - fan_w * 0.4, by + fan_h),
         (bx + fan_w, by + fan_h * 0.85),
         (bx + int(SIZE * 0.03), by - int(SIZE * 0.01))],
        fill=BRISTLE,
    )
    for i in range(5):
        t = i / 4
        x0 = bx - fan_w * 0.4 + t * (fan_w * 1.4)
        y0 = by + fan_h * (0.85 + 0.15 * (1 - abs(t - 0.5) * 2))
        d.line([(bx, by), (x0, y0)], fill=(160, 132, 66), width=int(SIZE * 0.006))

    for r0, a0, a1 in [(0.09, 200, 260), (0.13, 195, 250)]:
        d.arc(
            [bx + int(SIZE * 0.02) - int(SIZE * r0), by - int(SIZE * r0),
             bx + int(SIZE * 0.02) + int(SIZE * r0), by + int(SIZE * r0)],
            start=a0, end=a1, fill=GRAY, width=int(SIZE * 0.004),
        )

    pile_cx, pile_cy = bx + int(SIZE * 0.13), by + int(SIZE * 0.13)
    for ox, oy, rw, rh in [(-0.03, 0.0, 0.028, 0.016), (0.02, 0.008, 0.03, 0.017),
                           (0.0, -0.012, 0.024, 0.014), (0.045, -0.004, 0.022, 0.013)]:
        px, py = pile_cx + int(SIZE * ox), pile_cy + int(SIZE * oy)
        rw, rh = int(SIZE * rw), int(SIZE * rh)
        d.ellipse([px - rw, py - rh, px + rw, py + rh], fill=GREEN)

    arrow_top = int(SIZE * 0.47)
    arrow_bottom = arrow_top + int(SIZE * 0.09)
    d.line([(cx, arrow_top), (cx, arrow_bottom)], fill=GREEN, width=int(SIZE * 0.012))
    aw = int(SIZE * 0.025)
    d.polygon(
        [(cx - aw, arrow_bottom - aw), (cx + aw, arrow_bottom - aw), (cx, arrow_bottom + aw)],
        fill=GREEN,
    )

    BAG = (48, 48, 56)
    BAG_HEM = (66, 66, 76)
    BAG_INNER = (20, 20, 24)
    WRINKLE = (86, 86, 98)
    CORD = (236, 190, 58)

    # Drawstring garbage bag: tapered body, gathered hem with a yellow cord
    # pulled out and knotted, so it reads as a bag you can tie shut.
    bag_cx = cx
    top_y = int(SIZE * 0.64)
    bottom_y = int(SIZE * 0.825)
    top_hw = int(SIZE * 0.11)
    bottom_hw = int(SIZE * 0.145)
    corner = int(SIZE * 0.035)
    hem_h = int(SIZE * 0.028)

    d.polygon(
        [(bag_cx - top_hw, top_y),
         (bag_cx + top_hw, top_y),
         (bag_cx + bottom_hw, bottom_y - corner),
         (bag_cx + bottom_hw - corner, bottom_y),
         (bag_cx - bottom_hw + corner, bottom_y),
         (bag_cx - bottom_hw, bottom_y - corner)],
        fill=BAG,
    )

    # Wrinkles running down from the gathered hem
    ww = int(SIZE * 0.005)
    for x_top, x_bot in [(-0.08, -0.11), (-0.025, -0.04), (0.03, 0.05), (0.085, 0.12)]:
        x0 = bag_cx + int(SIZE * x_top)
        x1 = bag_cx + int(SIZE * x_bot)
        y0 = top_y + hem_h + int(SIZE * 0.012)
        y1 = top_y + int(SIZE * 0.125)
        xm = (x0 + x1) / 2 + int(SIZE * 0.012)
        d.line([(x0, y0), (xm, (y0 + y1) / 2), (x1, y1)], fill=WRINKLE, width=ww, joint="curve")

    # Hem band with a gathered (scalloped) top edge
    d.rectangle([bag_cx - top_hw, top_y, bag_cx + top_hw, top_y + hem_h], fill=BAG_HEM)
    n = 9
    sr = top_hw / n
    for i in range(n):
        sx = bag_cx - top_hw + sr * (2 * i + 1)
        d.ellipse([sx - sr, top_y - sr * 0.55, sx + sr, top_y + sr * 0.55], fill=BAG_HEM)

    # Open mouth showing cuttings already inside
    mouth_rx = top_hw - int(SIZE * 0.02)
    mouth_ry = int(SIZE * 0.018)
    d.ellipse([bag_cx - mouth_rx, top_y - mouth_ry * 1.4, bag_cx + mouth_rx, top_y + mouth_ry * 0.6],
              fill=BAG_INNER)
    for ox, oy, rw, rh in [(-0.04, -0.006, 0.026, 0.010), (0.03, -0.009, 0.028, 0.011)]:
        px, py = bag_cx + int(SIZE * ox), top_y + int(SIZE * oy)
        rw, rh = int(SIZE * rw), int(SIZE * rh)
        d.ellipse([px - rw, py - rh, px + rw, py + rh], fill=GREEN)

    # Yellow drawstring through the hem, pulled out at the front and knotted
    cw = int(SIZE * 0.008)
    cord_y = top_y + hem_h // 2
    gap_l = bag_cx + int(SIZE * 0.025)
    gap_r = bag_cx + int(SIZE * 0.065)
    d.line([(bag_cx - top_hw, cord_y), (gap_l, cord_y)], fill=CORD, width=cw)
    d.line([(gap_r, cord_y), (bag_cx + top_hw, cord_y)], fill=CORD, width=cw)
    knot = (bag_cx + int(SIZE * 0.045), top_y + int(SIZE * 0.075))
    d.line([(gap_l, cord_y), knot], fill=CORD, width=cw)
    d.line([(gap_r, cord_y), knot], fill=CORD, width=cw)
    kr = int(SIZE * 0.011)
    d.ellipse([knot[0] - kr, knot[1] - kr, knot[0] + kr, knot[1] + kr], fill=CORD)
    for dx in (-0.018, 0.016):
        end = (knot[0] + int(SIZE * dx), knot[1] + int(SIZE * 0.035))
        d.line([knot, end], fill=CORD, width=cw)

    # Cuttings falling in
    leaf_cx, leaf_cy = bag_cx, top_y - int(SIZE * 0.035)
    lr = int(SIZE * 0.02)
    d.ellipse([leaf_cx - lr - int(SIZE * 0.03), leaf_cy - lr * 0.6,
               leaf_cx - int(SIZE * 0.03) + lr, leaf_cy + lr * 0.6], fill=GREEN)
    d.ellipse([leaf_cx - lr + int(SIZE * 0.025), leaf_cy + int(SIZE * 0.012) - lr * 0.5,
               leaf_cx + int(SIZE * 0.025) + lr, leaf_cy + int(SIZE * 0.012) + lr * 0.5], fill=GREEN)

    draw_number_badge(d, 2, SIZE)
    draw_caption_band(d, "សម្អាតកន្លែងធ្វើការ កម្ចាត់សំណល់", SIZE, khmer_size=52)

    img = img.resize((1080, 1080), Image.LANCZOS)
    img.save(OUT_DIR / "standard_2_timing_disposal.png")


if __name__ == "__main__":
    make_image1()
    make_image2()
    print("Saved:")
    for p in sorted(OUT_DIR.glob("*.png")):
        print(" -", p)
