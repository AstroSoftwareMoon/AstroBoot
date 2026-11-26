AstroBoot - arranca cualquier sistema desde un solo USB
=======================================================

Copia tus archivos ISO / WIM / IMG / VHD(x) / EFI al USB y elige cuál arrancar.

Instalar en un USB (se borrarán sus datos)
  Windows : ejecuta AstroBoot2Disk.exe
  Linux   : sudo sh AstroBoot2Disk.sh -i /dev/sdX      (consola)
            sudo sh AstroBootWeb.sh                     (interfaz web)
            ./AstroBootGUI.x86_64                       (interfaz gráfica)

Teclas en el menú de arranque
  F1 ayuda · F2 explorar · F3 vista árbol · F4 arranque local
  F5 herramientas · F6 menú extendido · L idioma

Herramientas AstroBoot (al final del menú y dentro de F5)
  - Test de memoria RAM (Memtest86+)
  - Arrancar desde Internet (netboot.xyz)
  - Buscar sistemas operativos instalados (Windows / Linux / systemd-boot / rEFInd)
  - Información del sistema (CPU, RAM, discos, PCI) y modos de vídeo
  - Reiniciar, apagar y entrar en la BIOS/UEFI

Web: https://github.com/AstroSoftwareMoon/AstroBoot

AstroBoot es software libre (GPL-3.0) basado en Ventoy de longpanda
(https://www.ventoy.net). Incluye GRUB 2, Memtest86+ (GPL-2.0) y
netboot.xyz/iPXE (GPL-2.0). La carpeta "ventoy" del USB y la partición
"VTOYEFI" mantienen ese nombre porque el núcleo de arranque los necesita.
