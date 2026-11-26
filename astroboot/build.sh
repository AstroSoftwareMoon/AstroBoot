#!/bin/bash
#
# AstroBoot release builder
#
# Builds astroboot-<ver>-linux.tar.gz and astroboot-<ver>-windows.zip.
#
# The signed low-level binaries (GRUB core/EFI images, shim, Windows/Linux
# GUI executables) are taken unmodified from the official Ventoy release this
# fork is based on, so Secure Boot keeps working exactly as upstream. Everything
# else (boot menu, theme, fonts, tools, translations, scripts, WebUI) comes from
# this repository.
#
# Needs: bash, curl, xz, tar, unzip, zip, mtools, dosfstools (mkfs.fat), python3
# Usage: astroboot/build.sh            (outputs into astroboot/out/)
#
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
SELF=$ROOT/astroboot
UPVER=1.1.18
UPSHA_LINUX=d86ff9de63d94c8b8f1f6b14d23c55af4b88e8207bf2893890892a6a97b1ad54
UPSHA_WIN=082c478e8c432e1ac653899fcf50e3a4077a2851bc6112b5ddd30545962164a9
UPURL=https://github.com/ventoy/Ventoy/releases/download/v$UPVER

VER=$(sed -n 's/^set ASTROBOOT_VERSION="\(.*\)"/\1/p' "$ROOT/INSTALL/grub/grub.cfg")
CFGVER=$(sed -n 's/^set VENTOY_VERSION="\(.*\)"/\1/p' "$ROOT/INSTALL/grub/grub.cfg")
[ "$CFGVER" = "$UPVER" ] || { echo "grub.cfg core version $CFGVER != $UPVER"; exit 1; }

WORK=$SELF/build
CACHE=$SELF/cache
OUT=$SELF/out
NAME=astroboot-$VER

log() { printf '\033[1;35m==>\033[0m %s\n' "$*"; }

for t in curl xz tar unzip zip mcopy mmd mkfs.fat python3 sha256sum; do
    command -v $t >/dev/null || { echo "missing tool: $t"; exit 1; }
done

rm -rf "$WORK" && mkdir -p "$WORK" "$CACHE" "$OUT"

#----------------------------------------------------------------- upstream ---
fetch() {
    local file=$1 sum=$2
    if [ ! -f "$CACHE/$file" ] || ! echo "$sum  $CACHE/$file" | sha256sum -c --status; then
        log "download $file"
        curl -fL --retry 4 -o "$CACHE/$file" "$UPURL/$file"
    fi
    echo "$sum  $CACHE/$file" | sha256sum -c --status || { echo "checksum mismatch: $file"; exit 1; }
}
fetch ventoy-$UPVER-linux.tar.gz   $UPSHA_LINUX
fetch ventoy-$UPVER-windows.zip    $UPSHA_WIN

log "extract upstream $UPVER"
mkdir -p "$WORK/up-linux" "$WORK/up-win"
tar xzf "$CACHE/ventoy-$UPVER-linux.tar.gz" -C "$WORK/up-linux"
unzip -q "$CACHE/ventoy-$UPVER-windows.zip" -d "$WORK/up-win"
UPL=$WORK/up-linux/ventoy-$UPVER
UPW=$WORK/up-win/ventoy-$UPVER

#----------------------------------------------------------- VTOYEFI files ----
log "unpack VTOYEFI partition"
EFI=$WORK/efi
mkdir -p "$EFI"
xz -dc "$UPL/ventoy/ventoy.disk.img.xz" > "$WORK/upstream.disk.img"
MTOOLS_SKIP_CHECK=1 mcopy -s -n -m -i "$WORK/upstream.disk.img" ::/ "$EFI/"

log "overlay AstroBoot boot menu"
G=$EFI/grub
rm -rf "$G/themes" "$G/help.tar.gz" "$G/menu.tar.gz" "$G/menulang.cfg"
cp "$ROOT"/INSTALL/grub/*.cfg "$G/"
rm -f "$G/menulang.cfg"
cp -r "$ROOT/INSTALL/grub/distro" "$ROOT/INSTALL/grub/fonts" "$G/"
mkdir -p "$G/themes"
cp -r "$ROOT/INSTALL/grub/themes/astroboot" "$G/themes/"

# help + menu translations are packed exactly like ventoy_pack.sh does
(cd "$ROOT/INSTALL/grub" && tar czf "$G/help.tar.gz" ./help/ && tar czf "$G/menu.tar.gz" ./menu/)

# menulang.cfg
cp "$ROOT/INSTALL/grub/menulang.cfg" "$G/menulang.cfg"
{
    title=$(grep VTLANG_LANGUAGE_NAME "$ROOT/INSTALL/grub/menu/zh_CN.json" | awk -F\" '{print $4}')
    echo "menuentry \"zh_CN  -  $title\" --class=menu_lang_item --class=debug_menu_lang --class=F5tool {"
    echo "    vt_load_menu_lang zh_CN"
    echo "}"
    ls -1 "$ROOT/INSTALL/grub/menu/" | grep -v zh_CN | sort | while read -r f; do
        lang=${f%.*}
        title=$(grep VTLANG_LANGUAGE_NAME "$ROOT/INSTALL/grub/menu/$f" | awk -F\" '{print $4}')
        echo "menuentry \"$lang  -  $title\" --class=menu_lang_item --class=debug_menu_lang --class=F5tool {"
        echo "    vt_load_menu_lang $lang"
        echo "}"
    done
    echo "menuentry \"\$VTLANG_RETURN_PREVIOUS\" --class=vtoyret VTOY_RET {"
    echo "        echo \"Return ...\""
    echo "}"
} >> "$G/menulang.cfg"

log "add AstroBoot tools"
mkdir -p "$EFI/astroboot"
cp "$SELF"/tools/memtest86+x64.bin "$SELF"/tools/memtest86+x64.efi \
   "$SELF"/tools/netboot.xyz.efi "$SELF"/tools/netboot.xyz.lkrn "$EFI/astroboot/"
echo "$VER" > "$EFI/astroboot/version"

#------------------------------------------------------- new 32MB FAT image ---
log "build ventoy.disk.img (VTOYEFI, FAT16, 32MB)"
IMG=$WORK/ventoy.disk.img
rm -f "$IMG"
mkfs.fat -F 16 -n VTOYEFI -s 1 -S 512 -h 0 -g 255/63 -C "$IMG" 32768 >/dev/null
export MTOOLS_SKIP_CHECK=1
# grub.cfg goes first so it sits at the front of the partition (as upstream)
mmd -i "$IMG" ::/grub
mcopy -m -i "$IMG" "$G/grub.cfg" ::/grub/
for f in "$G"/*; do
    [ "$(basename "$f")" = grub.cfg ] && continue
    mcopy -s -m -i "$IMG" "$f" ::/grub/
done
for f in "$EFI"/*; do
    [ "$(basename "$f")" = grub ] && continue
    mcopy -s -m -i "$IMG" "$f" ::/
done
FREE=$(mdir -/ -i "$IMG" :: | grep "bytes free" | tail -1 | tr -dc "0-9")
log "VTOYEFI free space: $FREE bytes"

#--------------------------------------------------------------- linux pkg ----
log "assemble $NAME-linux.tar.gz"
L=$WORK/linux/$NAME
mkdir -p "$L"
cp -a "$UPL/boot" "$UPL/plugin" "$UPL/tool" "$L/"
mkdir -p "$L/ventoy"
cp "$UPL/ventoy/ventoy_4k.disk.img.xz" "$L/ventoy/"
xz --check=crc32 -c "$IMG" > "$L/ventoy/ventoy.disk.img.xz"
echo "$UPVER" > "$L/ventoy/version"
echo "$VER" > "$L/ventoy/astroboot_version"

# scripts from this repo
cp "$ROOT/INSTALL/AstroBoot2Disk.sh" "$ROOT/INSTALL/AstroBootWeb.sh" "$ROOT/INSTALL/AstroBootPlugson.sh" \
   "$ROOT/INSTALL/CreatePersistentImg.sh" "$ROOT/INSTALL/ExtendPersistentImg.sh" "$L/"
sed -e 's/VentoyVlnk\.sh/AstroBootVlnk.sh/g' -e '/^ *echo/s/\bVentoy\b/AstroBoot/g' \
    "$UPL/VentoyVlnk.sh" > "$L/AstroBootVlnk.sh"
cp "$ROOT/INSTALL/tool/VentoyWorker.sh" "$ROOT/INSTALL/tool/ventoy_lib.sh" \
   "$ROOT/INSTALL/tool/VentoyGTK.glade" "$ROOT/INSTALL/tool/distro_gui_type.json" "$L/tool/"
cp "$ROOT/LANGUAGES/languages.json" "$L/tool/languages.json"
for a in i386 x86_64 aarch64 mips64el; do
    cp "$UPL/VentoyGUI.$a" "$L/AstroBootGUI.$a"
done

# WebUI
cp -r "$ROOT/LinuxGUI/WebUI" "$L/WebUI"
sed 's/.*SCRIPT_DEL_THIS \(.*\)/\1/g' -i "$L/WebUI/index.html"
{ echo "var vtoy_language_data = "; cat "$ROOT/LANGUAGES/languages.json"; echo ";"; } > "$L/WebUI/static/js/languages.js"

cp "$SELF/README.txt" "$L/README"
cp "$ROOT/COPYING" "$L/COPYING"

find "$L" -type d -exec chmod 755 {} +
find "$L" -type f -exec chmod 644 {} +
chmod +x "$L"/*.sh "$L"/AstroBootGUI.* "$L"/tool/*.sh
for a in i386 x86_64 aarch64 mips64el; do
    chmod +x "$L/tool/$a/xzcat" "$L"/tool/$a/Ventoy2Disk.*
done
rm -f "$OUT/$NAME-linux.tar.gz"
tar -C "$WORK/linux" --owner=0 --group=0 -czf "$OUT/$NAME-linux.tar.gz" "$NAME"

#------------------------------------------------------------- windows pkg ----
log "assemble $NAME-windows.zip"
Wd=$WORK/windows/$NAME
mkdir -p "$Wd/ventoy" "$Wd/altexe"
cp -a "$UPW/boot" "$UPW/plugin" "$Wd/"
cp "$UPW/Ventoy2Disk.exe"   "$Wd/AstroBoot2Disk.exe"
cp "$UPW/VentoyPlugson.exe" "$Wd/AstroBootPlugson.exe"
cp "$UPW/VentoyVlnk.exe"    "$Wd/AstroBootVlnk.exe"
cp "$UPW/FOR_X64_ARM.txt"   "$Wd/"
for f in "$UPW"/altexe/*.exe; do
    b=$(basename "$f"); cp "$f" "$Wd/altexe/${b/Ventoy/AstroBoot}"
done
cp "$L/ventoy/ventoy.disk.img.xz" "$L/ventoy/ventoy_4k.disk.img.xz" "$L/ventoy/version" \
   "$L/ventoy/astroboot_version" "$Wd/ventoy/"
cp "$UPW/ventoy/plugson.tar.xz" "$Wd/ventoy/"
cp "$ROOT/LANGUAGES/languages.json" "$Wd/ventoy/languages.json"
cp "$SELF/README.txt" "$Wd/README.txt"
cp "$ROOT/COPYING" "$Wd/COPYING.txt"
rm -f "$OUT/$NAME-windows.zip"
(cd "$WORK/windows" && zip -qr -X "$OUT/$NAME-windows.zip" "$NAME")

#---------------------------------------------------------------- checksums ---
(cd "$OUT" && sha256sum "$NAME-linux.tar.gz" "$NAME-windows.zip" > SHA256SUMS.txt)
cp "$IMG" "$OUT/ventoy.disk.img"   # handy for tests, not published
log "done:"
ls -la "$OUT"
