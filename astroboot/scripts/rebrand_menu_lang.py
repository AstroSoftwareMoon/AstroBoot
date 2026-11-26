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
])
TR = {
    "es_ES": ["Herramientas AstroBoot", "Test de memoria RAM (Memtest86+)", "Arrancar desde Internet (netboot.xyz)",
              "Buscar sistemas operativos instalados", "No se encontró ningún sistema operativo instalado",
              "Información del sistema (CPU, RAM, discos, PCI)", "Modos de vídeo", "Acerca de AstroBoot",
              "Secure Boot está activo: esta herramienta no está firmada y puede ser rechazada. Desactiva Secure Boot si no arranca.",
              "Esta herramienta solo está disponible en PC x86/x64."],
    "pt_BR": ["Ferramentas AstroBoot", "Teste de memória (Memtest86+)", "Inicializar pela Internet (netboot.xyz)",
              "Procurar sistemas operacionais instalados", "Nenhum sistema operacional instalado foi encontrado",
              "Informações do sistema (CPU, RAM, discos, PCI)", "Modos de vídeo", "Sobre o AstroBoot",
              "O Secure Boot está ativo: esta ferramenta não é assinada e pode ser recusada. Desative o Secure Boot se ela não iniciar.",
              "Esta ferramenta só está disponível em PCs x86/x64."],
    "fr_FR": ["Outils AstroBoot", "Test de la mémoire (Memtest86+)", "Démarrer depuis Internet (netboot.xyz)",
              "Rechercher les systèmes installés", "Aucun système d'exploitation installé n'a été trouvé",
              "Informations système (CPU, RAM, disques, PCI)", "Modes vidéo", "À propos d'AstroBoot",
              "Secure Boot est actif : cet outil n'est pas signé et peut être refusé. Désactivez Secure Boot s'il ne démarre pas.",
              "Cet outil n'est disponible que sur les PC x86/x64."],
    "de_DE": ["AstroBoot-Werkzeuge", "Speichertest (Memtest86+)", "Aus dem Internet starten (netboot.xyz)",
              "Installierte Betriebssysteme suchen", "Kein installiertes Betriebssystem gefunden",
              "Systeminformationen (CPU, RAM, Laufwerke, PCI)", "Videomodi", "Über AstroBoot",
              "Secure Boot ist aktiv: dieses Werkzeug ist nicht signiert und kann abgelehnt werden. Secure Boot deaktivieren, falls es nicht startet.",
              "Dieses Werkzeug ist nur auf x86/x64-PCs verfügbar."],
    "it_IT": ["Strumenti AstroBoot", "Test della memoria (Memtest86+)", "Avvia da Internet (netboot.xyz)",
              "Cerca sistemi operativi installati", "Nessun sistema operativo installato trovato",
              "Informazioni di sistema (CPU, RAM, dischi, PCI)", "Modalità video", "Informazioni su AstroBoot",
              "Secure Boot è attivo: questo strumento non è firmato e potrebbe essere rifiutato. Disattiva Secure Boot se non si avvia.",
              "Questo strumento è disponibile solo su PC x86/x64."],
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
