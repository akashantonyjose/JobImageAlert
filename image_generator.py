import os
import time
import textwrap
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1080, 1920

BG_COLOR = (10, 31, 68)          # navy blue
TITLE_COLOR = (255, 212, 0)      # yellow
TEXT_COLOR = (255, 255, 255)     # white
ACCENT_COLOR = (124, 255, 107)   # green - experience/location line
NOTE_COLOR = (255, 140, 140)     # soft red - official site warning
DIVIDER_COLOR = (44, 62, 99)
SUBSCRIBE_BG = (255, 212, 0)     # yellow banner
SUBSCRIBE_TEXT = (10, 31, 68)    # navy text on yellow banner

FONT_CANDIDATES_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONT_CANDIDATES_REGULAR = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def _load_font(size, bold=True):
    candidates = FONT_CANDIDATES_BOLD if bold else FONT_CANDIDATES_REGULAR
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def create_job_image(jobs, title, out_dir="output_images"):
    """
    jobs: list of dicts with keys title, company, experience, location, work_mode
    title: heading text, e.g. "LATEST JOBS - IT" or "FRESHER JOBS - IT"
    Returns the path to the saved PNG.
    """
    os.makedirs(out_dir, exist_ok=True)

    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    title_font = _load_font(56)
    heading_font = _load_font(32)
    body_font = _load_font(26)
    note_font = _load_font(24)
    sub_font = _load_font(30)

    y = 90
    draw.text((WIDTH / 2, y), title, font=title_font, fill=TITLE_COLOR, anchor="ma")
    y += 90
    draw.line((60, y, WIDTH - 60, y), fill=DIVIDER_COLOR, width=2)
    y += 50

    # Reserve space at the bottom for the note + subscribe banner
    footer_reserved = 260
    max_y = HEIGHT - footer_reserved

    for job in jobs:
        if y > max_y:
            break
        header_line = f"{job.get('title', '')} @ {job.get('company', '')}"
        for line in textwrap.wrap(header_line, width=34):
            draw.text((WIDTH / 2, y), line, font=heading_font, fill=TEXT_COLOR, anchor="ma")
            y += 40

        detail_line = (
            f"Exp: {job.get('experience') or 'See listing'}  |  "
            f"{job.get('work_mode', '')}  |  {job.get('location', '')}"
        )
        for line in textwrap.wrap(detail_line, width=46):
            draw.text((WIDTH / 2, y), line, font=body_font, fill=ACCENT_COLOR, anchor="ma")
            y += 34

        y += 30  # spacing between job entries

    # Footer note
    footer_y = HEIGHT - footer_reserved + 10
    draw.line((60, footer_y, WIDTH - 60, footer_y), fill=DIVIDER_COLOR, width=2)
    footer_y += 30
    note_text = "Apply only via the official company careers page - search the exact job title there directly."
    for line in textwrap.wrap(note_text, width=50):
        draw.text((WIDTH / 2, footer_y), line, font=note_font, fill=NOTE_COLOR, anchor="ma")
        footer_y += 30

    # Subscribe banner (high-contrast yellow bar at the very bottom)
    banner_y = HEIGHT - 90
    draw.rectangle((0, banner_y, WIDTH, HEIGHT), fill=SUBSCRIBE_BG)
    draw.text(
        (WIDTH / 2, banner_y + 45),
        "SUBSCRIBE FOR MORE JOB UPDATES",
        font=sub_font,
        fill=SUBSCRIBE_TEXT,
        anchor="mm",
    )

    out_path = os.path.join(out_dir, f"jobs_{int(time.time())}.png")
    img.save(out_path)
    return out_path
