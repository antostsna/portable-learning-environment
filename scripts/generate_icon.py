"""Generate the PLE app icon.

Produces ``assets/ico.png`` (256×256) and ``assets/ico.ico`` (multi-size:
16, 24, 32, 48, 64, 128, 256). The PNG is what Qt loads at runtime; the
ICO is what PyInstaller embeds in the Windows executable.

Run from the repo root::

    python scripts/generate_icon.py

Design — "Classroom":
    Blue squircle (PLE primary gradient) holds a white classroom card.
    A dark slate chalkboard sits along the top of the card. Below it,
    three silhouettes — a teacher (centre, taller, primary blue) flanked
    by two student silhouettes (slate-grey). A subtle desk line anchors
    them. Reads as "teacher, students, class system" in one glyph.

Re-run after tweaking ``render_icon`` to regenerate both files.
"""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


# ---------- Palette (matches src/ple/views/theme/light.qss) ----------
PRIMARY_DARK = (29, 78, 216)    # #1d4ed8 — squircle top
PRIMARY = (37, 99, 235)         # #2563eb — teacher silhouette
PRIMARY_LIGHT = (59, 130, 246)  # #3b82f6 — squircle bottom
TEACHER = PRIMARY
STUDENT = (51, 65, 85)          # #334155 — slate-700
CHALKBOARD = (15, 23, 42)       # #0f172a — slate-900
DESK = (203, 213, 225)          # #cbd5e1 — slate-300, soft desk line
SHADOW = (15, 23, 42, 110)
PAGE = (255, 255, 255, 255)
CHALK_TEXT = (255, 255, 255, 220)


def _squircle_mask(size: int, radius_ratio: float = 0.22) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size - 1, size - 1),
        radius=int(size * radius_ratio),
        fill=255,
    )
    return mask


def _vertical_gradient(size: int, top_color, bottom_color) -> Image.Image:
    """RGB image with a vertical linear gradient."""
    base = Image.new("RGB", (size, size), bottom_color)
    overlay = Image.new("RGB", (size, size), top_color)
    mask = Image.linear_gradient("L").resize((size, size))  # 0 top → 255 bottom
    return Image.composite(base, overlay, mask)


def _draw_figure(draw: ImageDraw.ImageDraw, cx: int, head_cy: int,
                 head_r: int, color: tuple) -> None:
    """Draw a head + shoulders silhouette centred on (cx, head_cy).

    The body is a short, wide dome — head sits on top of it like a classic
    "person" icon. Bust stays compact so multiple figures don't bleed into
    each other at small sizes.
    """
    # Head
    draw.ellipse(
        (cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r),
        fill=color,
    )
    # Shoulders: wide, shallow ellipse — only its top arc reads as a torso
    body_w_half = int(head_r * 1.8)
    body_h_half = int(head_r * 1.4)
    body_cy = head_cy + int(head_r * 1.4)
    draw.ellipse(
        (cx - body_w_half, body_cy - body_h_half,
         cx + body_w_half, body_cy + body_h_half),
        fill=color,
    )


def render_icon(size: int) -> Image.Image:
    """Render the icon at the requested pixel size as RGBA."""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # 1) Blue squircle background ------------------------------------------------
    bg_rgb = _vertical_gradient(size, PRIMARY_DARK, PRIMARY_LIGHT)
    bg = bg_rgb.convert("RGBA")
    bg.putalpha(_squircle_mask(size))
    canvas = Image.alpha_composite(canvas, bg)

    # 2) Classroom card geometry --------------------------------------------------
    card_left = int(size * 0.18)
    card_right = size - card_left
    card_top = int(size * 0.22)
    card_bottom = int(size * 0.84)
    card_radius = max(2, int(size * 0.055))

    # Drop shadow under the card
    shadow_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = max(2, size // 64)
    blur_r = max(3, size // 48)
    ImageDraw.Draw(shadow_layer).rounded_rectangle(
        (card_left + offset, card_top + offset,
         card_right + offset, card_bottom + offset),
        radius=card_radius,
        fill=SHADOW,
    )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=blur_r))
    canvas = Image.alpha_composite(canvas, shadow_layer)

    draw = ImageDraw.Draw(canvas)

    # White card
    draw.rounded_rectangle(
        (card_left, card_top, card_right, card_bottom),
        radius=card_radius,
        fill=PAGE,
    )

    # 3) Card-shape mask used to clip figure bodies that extend past the bottom --
    card_mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(card_mask).rounded_rectangle(
        (card_left, card_top, card_right, card_bottom),
        radius=card_radius,
        fill=255,
    )

    # 4) Chalkboard bar at the top of the card -----------------------------------
    bar_h = int(size * 0.12)
    draw.rounded_rectangle(
        (card_left, card_top, card_right, card_top + bar_h),
        radius=card_radius,
        fill=(*CHALKBOARD, 255),
    )
    # Square off the bottom edge of the rounded rect
    draw.rectangle(
        (card_left, card_top + bar_h - card_radius - 1,
         card_right, card_top + bar_h),
        fill=(*CHALKBOARD, 255),
    )
    # Three small chalk strokes on the board
    dash_y = card_top + bar_h // 2
    dash_w = int(size * 0.07)
    dash_h = max(1, int(size * 0.014))
    dash_gap = int(size * 0.025)
    total_w = 3 * dash_w + 2 * dash_gap
    dash_start_x = (card_left + card_right) // 2 - total_w // 2
    for i in range(3):
        x = dash_start_x + i * (dash_w + dash_gap)
        draw.rounded_rectangle(
            (x, dash_y - dash_h // 2, x + dash_w, dash_y + dash_h // 2),
            radius=max(1, dash_h // 2),
            fill=CHALK_TEXT,
        )

    # 5) Figures (drawn onto a clipped layer so bodies don't bleed past card) ----
    figures_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(figures_layer)

    content_top = card_top + bar_h
    figure_baseline = card_bottom - int(size * 0.08)  # approximate body bottom

    centre_x = (card_left + card_right) // 2
    teacher_head_r = max(2, int(size * 0.070))
    student_head_r = max(2, int(size * 0.055))

    # Vertical placement: teacher head higher than students (visually taller)
    teacher_head_cy = content_top + int(size * 0.075)
    student_head_cy = content_top + int(size * 0.115)

    # Wider spacing so the two students stay visible behind the teacher
    student_dx = int(size * 0.155)

    # Draw students first so the teacher overlaps slightly in front
    _draw_figure(fdraw, centre_x - student_dx, student_head_cy,
                 student_head_r, STUDENT)
    _draw_figure(fdraw, centre_x + student_dx, student_head_cy,
                 student_head_r, STUDENT)
    _draw_figure(fdraw, centre_x, teacher_head_cy, teacher_head_r, TEACHER)

    # Clip figures to the card silhouette so bodies tuck behind the rounded edge
    alpha = figures_layer.getchannel("A")
    figures_layer.putalpha(ImageChops.multiply(alpha, card_mask))
    canvas = Image.alpha_composite(canvas, figures_layer)

    # 6) Subtle desk line at the bottom of the card ------------------------------
    desk_y = figure_baseline + int(size * 0.005)
    desk_h = max(1, int(size * 0.012))
    desk_inset = int(size * 0.025)
    ImageDraw.Draw(canvas).rounded_rectangle(
        (card_left + desk_inset, desk_y,
         card_right - desk_inset, desk_y + desk_h),
        radius=max(1, desk_h // 2),
        fill=(*DESK, 255),
    )

    return canvas


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    out_png = repo_root / "assets" / "ico.png"
    out_ico = repo_root / "assets" / "ico.ico"

    img_256 = render_icon(256)
    img_256.save(out_png, optimize=True)
    print(f"wrote {out_png.relative_to(repo_root)} ({out_png.stat().st_size:,} bytes)")

    ico_sizes = (16, 24, 32, 48, 64, 128, 256)
    base = render_icon(max(ico_sizes))
    base.save(out_ico, format="ICO", sizes=[(s, s) for s in ico_sizes])
    print(f"wrote {out_ico.relative_to(repo_root)} "
          f"({out_ico.stat().st_size:,} bytes) — sizes {ico_sizes}")


if __name__ == "__main__":
    main()
