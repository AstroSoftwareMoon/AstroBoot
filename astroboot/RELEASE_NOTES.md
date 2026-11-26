## AstroBoot 1.0.0

Primera versión de AstroBoot, basada en el núcleo de Ventoy 1.1.18.

**Descargas**
- `astroboot-1.0.0-windows.zip` → descomprime y ejecuta `AstroBoot2Disk.exe`
- `astroboot-1.0.0-linux.tar.gz` → `sudo sh AstroBoot2Disk.sh -i /dev/sdX` o `sudo sh AstroBootWeb.sh`

**Novedades**
- Tema nuevo estilo familia Astro: fondo espacial, panel de cristal, selección con degradado violeta→rosa, iconos para cada tipo de imagen y herramienta, fuentes DejaVu.
- Menú **Herramientas AstroBoot** (al final de la lista y dentro de F5): Memtest86+, arranque por red con netboot.xyz, buscador de sistemas instalados (Windows, GRUB, systemd-boot, rEFInd), información del sistema (CPU, RAM, discos, PCI), modos de vídeo, reiniciar/apagar/entrar en UEFI.
- Menú en español por defecto (cambia con **L**) y textos nuevos traducidos a es, en, pt, fr, de, it.
- Instalador web de Linux rediseñado; scripts renombrados a `AstroBoot2Disk.sh`, `AstroBootWeb.sh`, `AstroBootPlugson.sh`, `AstroBootVlnk.sh`.
- Etiqueta por defecto de la partición de datos: `AstroBoot` (Linux).
- Corregido `sr_RS.json` (le faltaba la llave inicial en Ventoy).

**Notas**
- Secure Boot funciona igual que en Ventoy para las ISO. Memtest86+ y netboot.xyz no están firmados: desactiva Secure Boot para usarlos.
- El número de versión que muestran los instaladores (1.1.18) es el del núcleo de arranque.
- Un USB con Ventoy se puede actualizar a AstroBoot con la opción *Actualizar* sin perder tus ISO.

SHA-256 en `SHA256SUMS.txt`.
