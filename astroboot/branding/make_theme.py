#!/usr/bin/env python3
"""Generate the AstroBoot GRUB theme artwork.

Everything is drawn as SVG and rasterised with rsvg-convert, so the theme can
be regenerated from this file alone:

    python3 astroboot/branding/make_theme.py

Output: INSTALL/grub/themes/astroboot/*.png and icons/*.png
"""
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "INSTALL", "grub", "themes", "astroboot")
ICONS = os.path.join(OUT, "icons")

W, H = 1024, 768

# AstroTune family palette
VIOLET = "#7a00ff"
MAGENTA = "#d900e6"
PINK = "#ff0aa0"
LAVENDER = "#b98cff"
ICON = "#d9c2ff"

GRAD = f"""<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="18" y1="108" x2="100" y2="12">
  <stop offset="0" stop-color="{VIOLET}"/><stop offset="0.5" stop-color="{MAGENTA}"/><stop offset="1" stop-color="{PINK}"/>
</linearGradient>"""

LOGO_BODY = """
<mask id="crescent"><rect width="120" height="120" fill="#fff"/>
  <circle cx="70" cy="52" r="31" fill="#000"/>
  <rect x="45" y="-30" width="30" height="72" rx="15" fill="#000"/></mask>
<circle cx="58" cy="64" r="44" fill="url(#g)" mask="url(#crescent)"/>
<rect x="54" y="6" width="12" height="54" rx="6" fill="url(#g)"/>
<path d="M96 14 L98.8 22.2 L107 25 L98.8 27.8 L96 36 L93.2 27.8 L85 25 L93.2 22.2 Z" fill="#ff0aa0"/>
"""

# Geometry of the glass panel that holds the boot menu (fractions of W/H).
# theme.txt uses the same numbers so the menu always sits inside the panel.
PANEL = dict(x=0.055, y=0.205, w=0.89, h=0.665)


def render(svg, path, w=None, h=None):
    tmp = path + ".svg"
    with open(tmp, "w") as f:
        f.write(svg)
    cmd = ["rsvg-convert", tmp, "-o", path]
    if w:
        cmd += ["-w", str(w)]
    if h:
        cmd += ["-h", str(h)]
    subprocess.check_call(cmd)
    os.remove(tmp)


def background():
    rnd = random.Random(7)
    stars = []
    for _ in range(170):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.choice([0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.5])
        o = rnd.uniform(0.25, 0.9)
        c = rnd.choice(["#ffffff", "#ffffff", "#ffd6f0", "#e3d1ff"])
        stars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" opacity="{o:.2f}"/>')
    px, py = PANEL["x"] * W, PANEL["y"] * H
    pw, ph = PANEL["w"] * W, PANEL["h"] * H
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  {GRAD}
  <radialGradient id="glowV" cx="0.08" cy="1.02" r="0.75">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.55"/>
    <stop offset="0.55" stop-color="{VIOLET}" stop-opacity="0.12"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowP" cx="0.97" cy="-0.05" r="0.6">
    <stop offset="0" stop-color="{PINK}" stop-opacity="0.45"/>
    <stop offset="0.6" stop-color="{MAGENTA}" stop-opacity="0.08"/>
    <stop offset="1" stop-color="{MAGENTA}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#ffe3f4"/>
  </linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1d1b22" stop-opacity="0.88"/>
    <stop offset="1" stop-color="#121115" stop-opacity="0.92"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0.22"/>
    <stop offset="0.5" stop-color="#ffffff" stop-opacity="0.06"/>
    <stop offset="1" stop-color="{PINK}" stop-opacity="0.30"/>
  </linearGradient>
  <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0"/>
    <stop offset="0.3" stop-color="{MAGENTA}" stop-opacity="0.7"/>
    <stop offset="0.7" stop-color="{PINK}" stop-opacity="0.7"/>
    <stop offset="1" stop-color="{PINK}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="#050507"/>
<rect width="{W}" height="{H}" fill="url(#glowV)"/>
<rect width="{W}" height="{H}" fill="url(#glowP)"/>
{''.join(stars)}
<!-- big faint moon ring, bottom right -->
<circle cx="930" cy="760" r="210" fill="none" stroke="{MAGENTA}" stroke-opacity="0.10" stroke-width="2"/>
<circle cx="930" cy="760" r="250" fill="none" stroke="{VIOLET}" stroke-opacity="0.06" stroke-width="1"/>
<!-- header -->
<g transform="translate({px:.0f},34) scale(0.62)">{LOGO_BODY}</g>
<text x="{px + 86:.0f}" y="86" font-family="DejaVu Sans" font-weight="bold" font-size="40" fill="url(#title)" letter-spacing="0.5">Astro<tspan fill="{PINK}">Boot</tspan></text>
<text x="{px + 88:.0f}" y="112" font-family="DejaVu Sans" font-weight="bold" font-size="14" fill="{LAVENDER}" letter-spacing="0.4">Arranca cualquier sistema desde un solo USB</text>
<!-- glass panel -->
<rect x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}" rx="18" fill="url(#panel)"/>
<rect x="{px + 0.5:.1f}" y="{py + 0.5:.1f}" width="{pw - 1:.1f}" height="{ph - 1:.1f}" rx="18" fill="none" stroke="url(#edge)" stroke-width="1.2"/>
<!-- footer rule -->
<rect x="{px:.0f}" y="{H * 0.905:.0f}" width="{pw:.0f}" height="1" fill="url(#rule)"/>
</svg>"""
    render(svg, os.path.join(OUT, "background.png"))


def selection():
    # Selected menu item: rounded gradient pill split into w / c / e slices.
    h = 34
    r = 12
    left = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{r}" height="{h}">
<rect x="0" y="0" width="{r * 2}" height="{h}" rx="{r}" fill="#6c10e8"/>
<rect x="0" y="0" width="3" height="{h}" fill="{PINK}" opacity="0"/></svg>"""
    center = f"""<svg xmlns="http://www.w3.org/2000/svg" width="64" height="{h}">
<defs><linearGradient id="s" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#6c10e8"/><stop offset="0.55" stop-color="#b80fd6"/><stop offset="1" stop-color="#e40a8f"/></linearGradient>
<linearGradient id="hl" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#ffffff" stop-opacity="0.16"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>
<rect width="64" height="{h}" fill="url(#s)"/><rect width="64" height="{h}" fill="url(#hl)"/></svg>"""
    right = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{r}" height="{h}">
<rect x="-{r}" y="0" width="{r * 2}" height="{h}" rx="{r}" fill="#e40a8f"/></svg>"""
    render(left, os.path.join(OUT, "select_w.png"))
    render(center, os.path.join(OUT, "select_c.png"))
    render(right, os.path.join(OUT, "select_e.png"))


def slider():
    w = 6
    render(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{w}"><rect width="{w}" height="{w * 2}" rx="3" fill="{PINK}"/></svg>',
           os.path.join(OUT, "slider_n.png"))
    render(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="8"><rect width="{w}" height="8" fill="{PINK}"/></svg>',
           os.path.join(OUT, "slider_c.png"))
    render(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{w}"><rect y="-{w}" width="{w}" height="{w * 2}" rx="3" fill="{MAGENTA}"/></svg>',
           os.path.join(OUT, "slider_s.png"))
    # track
    render(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="8"><rect x="2" width="2" height="8" fill="#ffffff" opacity="0.08"/></svg>',
           os.path.join(OUT, "scroll_c.png"))


def nine_slice(prefix, fill, stroke, radius=12, fill_op=0.96):
    """Rounded box split into 9 pngs (nw n ne w c e sw s se)."""
    s = radius
    big = s * 3
    full = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{big}" height="{big}">
<rect x="0.5" y="0.5" width="{big - 1}" height="{big - 1}" rx="{radius}" fill="{fill}" fill-opacity="{fill_op}" stroke="{stroke}" stroke-width="1"/></svg>"""
    tmp = os.path.join(OUT, f"_{prefix}_full.png")
    render(full, tmp)
    parts = {"nw": (0, 0), "n": (1, 0), "ne": (2, 0), "w": (0, 1), "c": (1, 1), "e": (2, 1), "sw": (0, 2), "s": (1, 2), "se": (2, 2)}
    for name, (cx, cy) in parts.items():
        subprocess.check_call(["convert", tmp, "-crop", f"{s}x{s}+{cx * s}+{cy * s}", "+repage",
                               os.path.join(OUT, f"{prefix}_{name}.png")])
    os.remove(tmp)


# ---------------------------------------------------------------- icons ----
def icon_svg(body, color=ICON):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"
 fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<defs>{GRAD.replace('x1="18" y1="108" x2="100" y2="12"', 'x1="2" y1="22" x2="22" y2="2"')}</defs>{body}</svg>"""


DISC = '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.4" fill="url(#g)" stroke="none"/><path d="M7.5 9.5a5 5 0 0 1 2.5-3" />'
WINDOW = '<rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M12 4v16M3 12h18"/>'
CHIP = '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx="1" fill="url(#g)" stroke="none"/><path d="M9 2.5v3M15 2.5v3M9 18.5v3M15 18.5v3M2.5 9h3M2.5 15h3M18.5 9h3M18.5 15h3"/>'
IMAGE = '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/><rect x="9" y="12" width="7" height="5" rx="1" fill="url(#g)" stroke="none"/>'
HDD = '<rect x="3" y="6" width="18" height="12" rx="3"/><path d="M3 13h18"/><circle cx="17" cy="15.6" r="1" fill="url(#g)" stroke="none"/>'
FOLDER = '<path d="M3 7a2 2 0 0 1 2-2h4l2 2.5h8a2 2 0 0 1 2 2V18a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'
BACK = '<path d="M14.5 6 8.5 12l6 6"/>'
GEAR = '<circle cx="12" cy="12" r="3" stroke="url(#g)"/><path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M5.5 18.5l1.7-1.7M16.8 7.2l1.7-1.7"/>'
POWER = '<path d="M12 3v8" stroke="url(#g)"/><path d="M7 6.3a8 8 0 1 0 10 0"/>'
REBOOT = '<path d="M20 12a8 8 0 1 1-2.4-5.7"/><path d="M20 4v4.5h-4.5" stroke="url(#g)"/>'
WINLOGO = '<path d="M3 5.5 10.5 4.5v7H3zM12.5 4.2 21 3v8.5h-8.5zM3 12.5h7.5v7L3 18.5zM12.5 12.5H21V21l-8.5-1.2z" fill="url(#g)" stroke="none"/>'
KEYBOARD = '<rect x="2.5" y="6" width="19" height="12" rx="2.5"/><path d="M6 10h.01M9 10h.01M12 10h.01M15 10h.01M18 10h.01M7 14h10"/>'
GLOBE = '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18z" stroke="url(#g)"/>'
SHIELD = '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6z"/><path d="m8.8 12 2.3 2.3 4.2-4.6" stroke="url(#g)"/>'
ROCKET = '<path d="M12 2.8c3.2 2 4.6 5.6 4.2 10.2l-2.2 3H10l-2.2-3C7.4 8.4 8.8 4.8 12 2.8z"/><circle cx="12" cy="9.2" r="1.7" fill="url(#g)" stroke="none"/><path d="M8 13.5 5 16.5v3l3.6-2M16 13.5l3 3v3l-3.6-2M10.5 19.5 12 21.5l1.5-2" stroke="url(#g)"/>'
MEMORY = '<rect x="2.5" y="7" width="19" height="9" rx="1.5"/><path d="M6 10.5v2M9 10.5v2M12 10.5v2M15 10.5v2M18 10.5v2" stroke="url(#g)"/><path d="M5 16v2.5M8 16v2.5M11 16v2.5M14 16v2.5M17 16v2.5M20 16v2.5"/>'
CLOUD = '<path d="M7 18.5a4.5 4.5 0 0 1-.6-9 6 6 0 0 1 11.5 1.6A3.8 3.8 0 0 1 17.5 18.5z"/><path d="M12 11.5v5M9.8 14.3 12 16.5l2.2-2.2" stroke="url(#g)"/>'
TERMINAL = '<rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path d="m6.5 9.5 3 2.5-3 2.5" stroke="url(#g)"/><path d="M12 15h5"/>'
INFO = '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5" stroke="url(#g)"/><circle cx="12" cy="7.8" r="1.1" fill="url(#g)" stroke="none"/>'
MONITOR = '<rect x="2.5" y="4" width="19" height="13" rx="2"/><path d="M8.5 20.5h7M12 17v3.5"/><path d="M6 13.5 9.5 10l2.5 2.5L15 9l3 3" stroke="url(#g)"/>'
LIST = '<path d="M9 6.5h11M9 12h11M9 17.5h11"/><circle cx="4.8" cy="6.5" r="1.2" fill="url(#g)" stroke="none"/><circle cx="4.8" cy="12" r="1.2" fill="url(#g)" stroke="none"/><circle cx="4.8" cy="17.5" r="1.2" fill="url(#g)" stroke="none"/>'
UEFI = '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8.5 9h7M8.5 12h4.5M8.5 15h6" stroke="url(#g)"/>'
PALETTE = '<path d="M12 3a9 9 0 1 0 0 18c1.3 0 1.8-1 1.4-2-.5-1.2.3-2.5 1.7-2.5H17a4 4 0 0 0 4-4C21 7 17 3 12 3z"/><circle cx="7.5" cy="11" r="1.2" fill="url(#g)" stroke="none"/><circle cx="10.5" cy="7.5" r="1.2" fill="url(#g)" stroke="none"/><circle cx="15" cy="7.8" r="1.2" fill="url(#g)" stroke="none"/>'
TOGGLE = '<rect x="2.5" y="7" width="19" height="10" rx="5"/><circle cx="16.5" cy="12" r="3" fill="url(#g)" stroke="none"/>'
SEARCH = '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5" stroke="url(#g)"/>'

ICON_MAP = {
    # image types listed in the main menu
    "vtoyiso": DISC, "vtoywim": WINDOW, "vtoyefi": UEFI, "vtoyimg": IMAGE,
    "vtoyvhd": HDD, "vtoyvtoy": HDD, "vtoydir": FOLDER, "vtoyret": BACK,
    # F4 local boot
    "F4boot": HDD, "boot_disk": HDD, "boot_windows": WINLOGO, "boot_uefi": UEFI,
    "boot_g4d": TERMINAL, "boot_xorboot": TERMINAL,
    # F5 tools
    "F5tool": GEAR, "debug_power": POWER, "debug_reboot": REBOOT, "debug_halt": POWER,
    "debug_efisetup": UEFI, "debug_hwinfo": CHIP, "debug_kbd": KEYBOARD,
    "debug_menu_lang": GLOBE, "menu_lang_item": GLOBE, "debug_resolution": MONITOR,
    "debug_videomode": MONITOR, "debug_screen_mode": MONITOR, "debug_text_mode": TERMINAL,
    "debug_gui_mode": MONITOR, "debug_theme_select": PALETTE, "debug_theme": PALETTE,
    "debug_util": UEFI, "debug_temp_set": TOGGLE, "debug_control": TOGGLE,
    "debug_uefi_res_lock": MONITOR, "debug_json": LIST, "debug_imagelist": LIST,
    "debug_util_efidrv": LIST, "debug_util_blinit": SHIELD,
    "checksum_md5": SHIELD, "checksum_sha1": SHIELD, "checksum_sha256": SHIELD, "checksum_sha512": SHIELD,
    # AstroBoot tools
    "astro_tools": ROCKET, "astro_memtest": MEMORY, "astro_netboot": CLOUD,
    "astro_shell": TERMINAL, "astro_info": INFO, "astro_disks": HDD, "astro_search": SEARCH,
    "astro_pci": CHIP, "astro_video": MONITOR, "astro_about": ROCKET,
}


def icons():
    os.makedirs(ICONS, exist_ok=True)
    for name, body in ICON_MAP.items():
        render(icon_svg(body), os.path.join(ICONS, name + ".png"), 22, 22)


def logo_pngs():
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><defs>{GRAD}</defs>{LOGO_BODY}</svg>'
    with open(os.path.join(HERE, "logo.svg"), "w") as f:
        f.write(svg + "\n")
    for size in (16, 32, 48, 64, 128, 256, 512):
        render(svg, os.path.join(HERE, f"logo_{size}.png"), size, size)


def main():
    os.makedirs(OUT, exist_ok=True)
    background()
    selection()
    slider()
    nine_slice("terminal_box", "#121115", "#4b2d63", radius=10)
    # menu_*.png: fully transparent (the glass panel lives in background.png).
    # Ventoy's gfxmenu expects a menu pixmap style to exist.
    for part in ("nw", "n", "ne", "w", "c", "e", "sw", "s", "se"):
        subprocess.check_call(["convert", "-size", "8x8", "xc:none", "PNG32:" + os.path.join(OUT, f"menu_{part}.png")])
    icons()
    logo_pngs()
    print("theme written to", OUT)


if __name__ == "__main__":
    sys.exit(main())
