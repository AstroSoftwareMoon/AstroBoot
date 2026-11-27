## AstroBoot 1.0.2 · netboot.xyz con teclado USB

**Corregido en 1.0.2**
- **netboot.xyz y el teclado USB**: en algunas placas (p. ej. ASUS) el menú de netboot.xyz no respondía al teclado y solo avanzaba la cuenta atrás. "Arrancar desde Internet" usa ahora la versión SNP de netboot.xyz, que trabaja con los drivers de red de la placa y no toma los controladores USB, que es la causa conocida de ese bloqueo.
- Nueva entrada **"Arrancar desde Internet - modo compatibilidad"** con la versión completa, para PCs cuya BIOS no expone la tarjeta de red en UEFI (opción "Network Stack" desactivada).

---

### Incluye todo lo de 1.0.1 · logos de AstroBoot en todas partes

**Descargas**
- `astroboot-1.0.2-windows.zip` → descomprime y ejecuta `AstroBoot2Disk.exe`
- `astroboot-1.0.2-linux.tar.gz` → `./AstroBootGUI.x86_64`, `sudo sh AstroBootWeb.sh` o `sudo sh AstroBoot2Disk.sh -i /dev/sdX`

**Novedades en 1.0.1**
- **Instalador de Windows nuevo** (`AstroBoot2Disk.exe`), recompilado desde el código fuente: tema oscuro AstroBoot, cabecera con el logo, tarjetas, botón Instalar con degradado violeta→rosa, barra de título y menús oscuros, fuente Segoe UI.
- **Logo de AstroBoot en todos los ejecutables de Windows**: `AstroBoot2Disk.exe` (x86, x64, ARM64 y ARM), `AstroBootPlugson.exe` y `AstroBootVlnk.exe`. Icono de refrescar y candado de Secure Boot nuevos.
- **Plugson** (configurador de plugins en el navegador) con logo, favicon, título y colores de AstroBoot.
- **Linux**: la GUI gráfica usa el tema AstroBoot y sus iconos; el instalador web también.

> Si Windows sigue enseñando el icono viejo, es su caché de iconos: descomprime esta versión en una carpeta nueva (o reinicia el Explorador).

**Incluye (desde 1.0.0)**
- Menú de arranque con tema AstroBoot, 52 iconos, en español por defecto.
- Herramientas AstroBoot: Memtest86+, netboot.xyz, buscador de sistemas instalados, información del sistema, modos de vídeo, reiniciar/apagar/UEFI.

**Notas**
- Secure Boot funciona igual que en Ventoy para las ISO. Memtest86+ y netboot.xyz no están firmados.
- El número 1.1.18 que muestran los instaladores es la versión del núcleo de arranque (Ventoy 1.1.18).
- Un USB con Ventoy o AstroBoot 1.0.0 se actualiza con *Update* sin perder tus ISO.

SHA-256 en `SHA256SUMS.txt`.
