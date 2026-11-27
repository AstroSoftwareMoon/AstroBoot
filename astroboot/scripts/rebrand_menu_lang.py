#!/usr/bin/env python3
"""Add AstroBoot strings to every GRUB menu language file and rebrand
user-visible "Ventoy" words. File names such as ventoy.json are lowercase and
are left untouched on purpose (they are required by the boot core)."""
import json, os, re, sys
from collections import OrderedDict

MENU = sys.argv[1] if len(sys.argv) > 1 else "INSTALL/grub/menu"

EN = OrderedDict([
    ("VTLANG_ASTRO_TOOLS", "AstroBoot Tools"),
    ("VTLANG_ASTRO_MEMTEST", "Memory test (Memtest86+)"),
    ("VTLANG_ASTRO_NETBOOT", "Boot from the Internet (netboot.xyz)"),
    ("VTLANG_ASTRO_DETECT_OS", "Find installed operating systems"),
    ("VTLANG_ASTRO_NO_OS", "No installed operating system was found"),
    ("VTLANG_ASTRO_SYSINFO", "System information (CPU, RAM, disks, PCI)"),
    ("VTLANG_ASTRO_VIDEO", "Video modes"),
    ("VTLANG_ASTRO_ABOUT", "About AstroBoot"),
    ("VTLANG_ASTRO_SB_NOTE", "Secure Boot is on: this tool is not signed and may be refused. Turn Secure Boot off if it does not start."),
    ("VTLANG_ASTRO_ONLY_X64", "This tool is only available on x86/x64 PCs."),
    ("VTLANG_ASTRO_NETBOOT_COMPAT", "Boot from the Internet - compatibility mode (if no network is found)"),
    ("VTLANG_ASTRO_NETBOOT_COMPAT_NOTE", "Compatibility mode uses its own drivers: on some PCs the USB keyboard stops working. If so, wait for the countdown or hold the power button."),
])
TR = {
    "es_ES": ["Herramientas AstroBoot", "Test de memoria RAM (Memtest86+)", "Arrancar desde Internet (netboot.xyz)",
              "Buscar sistemas operativos instalados", "No se encontró ningún sistema operativo instalado",
              "Información del sistema (CPU, RAM, discos, PCI)", "Modos de vídeo", "Acerca de AstroBoot",
              "Secure Boot está activo: esta herramienta no está firmada y puede ser rechazada. Desactiva Secure Boot si no arranca.",
              "Esta herramienta solo está disponible en PC x86/x64.",
              "Arrancar desde Internet - modo compatibilidad (si no detecta la red)",
              "El modo compatibilidad usa sus propios drivers: en algunos PC el teclado USB deja de responder. Si pasa, espera la cuenta atrás o mantén pulsado el botón de encendido."],
    "pt_BR": ["Ferramentas AstroBoot", "Teste de memória (Memtest86+)", "Inicializar pela Internet (netboot.xyz)",
              "Procurar sistemas operacionais instalados", "Nenhum sistema operacional instalado foi encontrado",
              "Informações do sistema (CPU, RAM, discos, PCI)", "Modos de vídeo", "Sobre o AstroBoot",
              "O Secure Boot está ativo: esta ferramenta não é assinada e pode ser recusada. Desative o Secure Boot se ela não iniciar.",
              "Esta ferramenta só está disponível em PCs x86/x64.",
              "Inicializar pela Internet - modo de compatibilidade (se não encontrar a rede)",
              "O modo de compatibilidade usa drivers próprios: em alguns PCs o teclado USB para de responder. Se acontecer, aguarde a contagem ou segure o botão de energia."],
    "fr_FR": ["Outils AstroBoot", "Test de la mémoire (Memtest86+)", "Démarrer depuis Internet (netboot.xyz)",
              "Rechercher les systèmes installés", "Aucun système d'exploitation installé n'a été trouvé",
              "Informations système (CPU, RAM, disques, PCI)", "Modes vidéo", "À propos d'AstroBoot",
              "Secure Boot est actif : cet outil n'est pas signé et peut être refusé. Désactivez Secure Boot s'il ne démarre pas.",
              "Cet outil n'est disponible que sur les PC x86/x64.",
              "Démarrer depuis Internet - mode compatibilité (si aucun réseau n'est trouvé)",
              "Le mode compatibilité utilise ses propres pilotes : sur certains PC le clavier USB ne répond plus. Dans ce cas, attendez le compte à rebours ou maintenez le bouton d'alimentation."],
    "de_DE": ["AstroBoot-Werkzeuge", "Speichertest (Memtest86+)", "Aus dem Internet starten (netboot.xyz)",
              "Installierte Betriebssysteme suchen", "Kein installiertes Betriebssystem gefunden",
              "Systeminformationen (CPU, RAM, Laufwerke, PCI)", "Videomodi", "Über AstroBoot",
              "Secure Boot ist aktiv: dieses Werkzeug ist nicht signiert und kann abgelehnt werden. Secure Boot deaktivieren, falls es nicht startet.",
              "Dieses Werkzeug ist nur auf x86/x64-PCs verfügbar.",
              "Aus dem Internet starten - Kompatibilitätsmodus (falls kein Netzwerk gefunden wird)",
              "Der Kompatibilitätsmodus nutzt eigene Treiber: auf manchen PCs reagiert die USB-Tastatur nicht mehr. Dann den Countdown abwarten oder den Netzschalter gedrückt halten."],
    "it_IT": ["Strumenti AstroBoot", "Test della memoria (Memtest86+)", "Avvia da Internet (netboot.xyz)",
              "Cerca sistemi operativi installati", "Nessun sistema operativo installato trovato",
              "Informazioni di sistema (CPU, RAM, dischi, PCI)", "Modalità video", "Informazioni su AstroBoot",
              "Secure Boot è attivo: questo strumento non è firmato e potrebbe essere rifiutato. Disattiva Secure Boot se non si avvia.",
              "Questo strumento è disponibile solo su PC x86/x64.",
              "Avvia da Internet - modalità compatibilità (se non trova la rete)",
              "La modalità compatibilità usa driver propri: su alcuni PC la tastiera USB smette di rispondere. In tal caso attendi il conto alla rovescia o tieni premuto il pulsante di accensione."],
}
TR["pt_PT"] = TR["pt_BR"]

BRAND = re.compile(r"\bVentoy\b(?![._])")

for name in sorted(os.listdir(MENU)):
    if not name.endswith(".json"):
        continue
    lang = name[:-5]
    path = os.path.join(MENU, name)
    with open(path, "rb") as f:
        raw = f.read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=OrderedDict)
    for k, v in list(data.items()):
        if isinstance(v, str):
            data[k] = BRAND.sub("AstroBoot", v)
    values = TR.get(lang)
    out = OrderedDict()
    for k, v in data.items():
        if k == "MENU_STR_XXX":
            for i, (ak, av) in enumerate(EN.items()):
                out[ak] = values[i] if values else av
        if not k.startswith("VTLANG_ASTRO_"):
            out[k] = v
    with open(path, "w", encoding="utf-8-sig" if bom else "utf-8") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=4) + "\n")
print("menu languages updated")
