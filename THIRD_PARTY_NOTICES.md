# Avisos de terceros

AstroBoot es un fork de **[Ventoy](https://github.com/ventoy/Ventoy)** (longpanda, GPL-3.0).
Todo el código fuente de Ventoy 1.1.18 está incluido en este repositorio; el README
original se conserva en [`DOC/UPSTREAM_README.md`](DOC/UPSTREAM_README.md) y las
licencias de cada componente en [`License/`](License/).

Los paquetes publicados incluyen sin modificar los binarios de bajo nivel de la versión
oficial Ventoy 1.1.18 (GRUB 2 con los módulos de Ventoy, shim / MokManager, iPXE,
wimboot, herramientas EFI y los ejecutables de instalación), para conservar la firma
de Secure Boot. `astroboot/build.sh` los descarga desde la release oficial y comprueba
su SHA-256.

Herramientas añadidas por AstroBoot (`astroboot/tools/`):

| Herramienta | Versión | Licencia | Origen |
|---|---|---|---|
| Memtest86+ (`memtest86+x64.bin/.efi`) | 7.00 | GPL-2.0 | https://memtest.org (paquete `memtest86+` de Ubuntu 24.04) |
| netboot.xyz (`netboot.xyz.efi/.lkrn`) | 3.0.3 (iPXE 2.0.0+) | GPL-2.0 | https://github.com/netbootxyz/netboot.xyz |

Fuentes del tema: DejaVu Sans (licencia Bitstream Vera / dominio público).
Iconos, fondo y logo del tema AstroBoot: creados para este proyecto
(`astroboot/branding/make_theme.py`).

Las etiquetas internas `VTOYEFI` y la carpeta `ventoy/` del USB mantienen su nombre
porque el núcleo de arranque las necesita. La línea de créditos
"`<versión> <modo>  www.ventoy.net`" la dibuja el binario GRUB firmado y no puede
quitarse sin perder Secure Boot; AstroBoot solo cambia su posición y color.
