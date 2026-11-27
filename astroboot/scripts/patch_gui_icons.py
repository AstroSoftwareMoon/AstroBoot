#!/usr/bin/env python3
"""Swap the Ventoy icons embedded in the prebuilt Linux GUI binaries
(tool/<arch>/Ventoy2Disk.gtk2/.gtk3/.qt5) for the AstroBoot ones.

The GTK/Qt front-ends keep each icon as a raw .ico byte array
(LinuxGUI/Ventoy2Disk/GTK/*_icon_data.c). Each array appears exactly once in a
binary, so it is replaced in place by an AstroBoot .ico of the same size or
smaller, padded with zeros. Binaries are only touched when the match is unique.

usage: patch_gui_icons.py <repo root> <tool dir>
"""
import os
import re
import sys

root, tooldir = sys.argv[1], sys.argv[2]
gtk = os.path.join(root, "LinuxGUI", "Ventoy2Disk", "GTK")
icons = os.path.join(root, "astroboot", "branding", "icons")
pairs = [("window_icon_data.c", "app.ico"),
         ("refresh_icon_data.c", "refresh32.ico"),
         ("secure_icon_data.c", "lock13x16.ico")]


def upstream_bytes(cfile):
    # the .c files in the repo hold the *upstream* arrays (kept for reference)
    s = open(os.path.join(gtk, cfile)).read()
    body = s[s.index("{", s.index("hexData")):s.index("};")]
    return bytes(int(x, 16) for x in re.findall(r"0x([0-9A-Fa-f]{2})", body))


swaps = []
for cfile, ico in pairs:
    old = upstream_bytes(cfile)
    new = open(os.path.join(icons, ico), "rb").read()
    if len(new) > len(old):
        sys.exit(f"{ico} ({len(new)}) larger than upstream {cfile} ({len(old)})")
    swaps.append((old, new + b"\0" * (len(old) - len(new)), ico))

for arch in sorted(os.listdir(tooldir)):
    for name in ("Ventoy2Disk.gtk2", "Ventoy2Disk.gtk3", "Ventoy2Disk.qt5"):
        path = os.path.join(tooldir, arch, name)
        if not os.path.isfile(path):
            continue
        data = open(path, "rb").read()
        done = []
        for old, new, ico in swaps:
            if data.count(old) == 1:
                data = data.replace(old, new)
                done.append(ico)
        # version number colour: red -> AstroBoot pink (same length)
        red = b"<span weight='bold' foreground='red' size='xx-large'>"
        pink = b"<span weight='bold' color='#ff0aa0'  size='xx-large'>"
        if data.count(red) == 1:
            data = data.replace(red, pink)
            done.append("pink version")
        # the Qt front-end keeps its window icon as a single 64x64 PNG
        if name.endswith(".qt5") and data.count(b"\x89PNG\r\n\x1a\n") == 1:
            start = data.index(b"\x89PNG\r\n\x1a\n")
            end = data.index(b"IEND", start) + 8
            png = open(os.path.join(icons, "app64.png"), "rb").read()
            if len(png) <= end - start:
                data = data[:start] + png + b"\0" * (end - start - len(png)) + data[end:]
                done.append("app64.png")
        open(path, "wb").write(data)
        print(f"  {arch}/{name}: {', '.join(done) or 'no icon found'}")
