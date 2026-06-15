import os
import importlib.util
import requests
import json
from colorama import init, Fore, Style
import pyfiglet
import sys
import shutil
import platform

init()

PGR_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.join(PGR_DIR, "plugins")
BASE_URL = "https://raw.githubusercontent.com/rusher-code-330/PGR-Tools-Plugin/main"
INSTALLED_FILE = os.path.join(PGR_DIR, "installed.json")
CONFIG_FILE = os.path.join(PGR_DIR, "config.json")

if not os.path.exists(PLUGIN_DIR):
    os.makedirs(PLUGIN_DIR)

if not os.path.exists(INSTALLED_FILE):
    with open(INSTALLED_FILE, "w") as f:
        json.dump([], f)

DEFAULT_CONFIG = {
    "platform": "auto",   # auto, termux, linux, windows
    "pip_command": None   # override de la commande pip si besoin
}

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)


# ============================================================
# CONFIG
# ============================================================

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)


def detect_platform():
    """Détecte automatiquement la plateforme : termux, windows, linux"""
    cfg = load_config()

    if cfg.get("platform") and cfg["platform"] != "auto":
        return cfg["platform"]

    if "ANDROID_ROOT" in os.environ or "com.termux" in os.environ.get("PREFIX", ""):
        return "termux"

    system = platform.system().lower()
    if system == "windows":
        return "windows"

    return "linux"


def get_pip_command():
    """Retourne la commande pip adaptée selon l'OS / config"""
    cfg = load_config()

    if cfg.get("pip_command"):
        return cfg["pip_command"]

    return f"{sys.executable} -m pip install"


def config_menu():
    """Configuration interactive de PGR Tools"""
    cfg = load_config()
    detected = detect_platform()

    print(Fore.CYAN + "\n___ PGR CONFIG ___" + Style.RESET_ALL)
    print(f"| platform configurée : {cfg.get('platform')}")
    print(f"| platform détectée   : {detected}")
    print(f"| pip command         : {cfg.get('pip_command') or 'auto'}")
    print(Fore.CYAN + "___________________" + Style.RESET_ALL)
    print("| commandes :")
    print("|   pgr config platform <termux|linux|windows|auto>")
    print("|   pgr config pip <commande personnalisée>")
    print("|   pgr config reset")
    print("|   pgr config show")


# ============================================================
# SYSTEM REQUIREMENTS (ffmpeg, git, etc.)
# ============================================================

# Mapping des noms de paquets système qui changent selon l'OS
SYSTEM_PKG_MAP = {
    "ffmpeg": {
        "termux": "ffmpeg",
        "linux": "ffmpeg",
        "windows": "Gyan.FFmpeg"
    },
    "git": {
        "termux": "git",
        "linux": "git",
        "windows": "Git.Git"
    }
}


def get_system_install_command(pkg, plat):
    """Retourne la commande d'installation système selon l'OS"""
    if plat == "termux":
        return f"pkg install -y {pkg}"

    elif plat == "linux":
        if shutil.which("apt"):
            return f"sudo apt install -y {pkg}"
        elif shutil.which("pacman"):
            return f"sudo pacman -S --noconfirm {pkg}"
        elif shutil.which("dnf"):
            return f"sudo dnf install -y {pkg}"
        elif shutil.which("yum"):
            return f"sudo yum install -y {pkg}"
        else:
            return None

    elif plat == "windows":
        if shutil.which("winget"):
            return f"winget install -e --id {pkg}"
        elif shutil.which("choco"):
            return f"choco install {pkg} -y"
        else:
            return None

    return None


def install_system_requirements(data):
    """Installe les dépendances système (ffmpeg, git, etc.) selon l'OS"""
    if "requires_system" not in data:
        return

    plat = detect_platform()

    for pkg in data["requires_system"]:
        # check binaire (utilise le nom générique pour le check, pas le nom mappé)
        if shutil.which(pkg):
            print(Fore.CYAN + f"| {pkg} déjà installé" + Style.RESET_ALL)
            continue

        real_pkg = SYSTEM_PKG_MAP.get(pkg, {}).get(plat, pkg)
        cmd = get_system_install_command(real_pkg, plat)

        if cmd is None:
            print(Fore.RED + f"| impossible d'installer {pkg} automatiquement sur cette plateforme ({plat})" + Style.RESET_ALL)
            print(f"| installe-le manuellement : {pkg}")
            continue

        print(f"| installation système : {pkg} ({plat})")
        print(f"| commande : {cmd}")
        ret = os.system(cmd)

        if ret != 0:
            print(Fore.RED + f"| échec de l'installation de {pkg}" + Style.RESET_ALL)
            if plat == "termux":
                print("| essaie : pkg update && pkg upgrade puis réessaie")
            elif plat == "windows":
                if pkg == "ffmpeg":
                    print("| télécharge manuellement : https://ffmpeg.org/download.html")
            elif plat == "linux":
                print("| vérifie que tu as les droits sudo")
        else:
            if shutil.which(pkg):
                print(Fore.CYAN + f"| {pkg} installé avec succès" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"| {pkg} installé mais introuvable dans le PATH (redémarre le terminal)" + Style.RESET_ALL)


def check_ffmpeg():
    plat = detect_platform()
    print(Fore.CYAN + "\n___ FFMPEG CHECK ___" + Style.RESET_ALL)
    print(f"| platform : {plat}")

    if shutil.which("ffmpeg"):
        print(Fore.CYAN + "| ffmpeg : OK (trouvé dans le PATH)" + Style.RESET_ALL)
        os.system("ffmpeg -version")
    else:
        print(Fore.RED + "| ffmpeg : NON TROUVÉ" + Style.RESET_ALL)
        real_pkg = SYSTEM_PKG_MAP["ffmpeg"].get(plat, "ffmpeg")
        cmd = get_system_install_command(real_pkg, plat)
        if cmd:
            print(f"| pour l'installer : {cmd}")
        else:
            print("| installe-le manuellement depuis https://ffmpeg.org/download.html")

    print(Fore.CYAN + "_____________________" + Style.RESET_ALL)


# ============================================================
# PIP REQUIREMENTS
# ============================================================

def install_requirements(data):
    """Installe les dépendances système puis pip"""
    try:
        install_system_requirements(data)

        if "requires" not in data:
            return

        pip_cmd = get_pip_command()
        for pkg in data["requires"]:
            print(f"| installing dependency: {pkg}")
            ret = os.system(f"{pip_cmd} {pkg}")

            if ret != 0:
                print(Fore.RED + f"| échec de l'installation de {pkg}" + Style.RESET_ALL)
    except Exception as e:
        print("| dependency error:", e)


# ============================================================
# PLUGINS
# ============================================================

def load_plugins():
    plugins = {}

    for folder in os.listdir(PLUGIN_DIR):
        plugin_path = os.path.join(PLUGIN_DIR, folder)

        if os.path.isdir(plugin_path):
            config_path = os.path.join(plugin_path, "plugin.json")
            main_path = os.path.join(plugin_path, "main.py")

            if not os.path.exists(config_path):
                continue
            if not os.path.exists(main_path):
                continue

            try:
                with open(config_path, "r") as f:
                    data = json.load(f)

                plugin_name = data["name"]

                spec = importlib.util.spec_from_file_location(plugin_name, main_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                plugins[plugin_name] = module

            except Exception as e:
                print(f"| failed loading plugin: {folder}")
                print(e)

    return plugins


def save_installed(data):
    with open(INSTALLED_FILE, "w") as f:
        json.dump(data, f)


def get_installed():
    with open(INSTALLED_FILE, "r") as f:
        return json.load(f)


def sync_installed():
    """Sync installed.json with folders actually present in plugins/"""
    actual = [
        folder for folder in os.listdir(PLUGIN_DIR)
        if os.path.isdir(os.path.join(PLUGIN_DIR, folder))
        and os.path.exists(os.path.join(PLUGIN_DIR, folder, "plugin.json"))
        and os.path.exists(os.path.join(PLUGIN_DIR, folder, "main.py"))
    ]
    save_installed(actual)
    return actual


def install_plugin(name):
    plugin_folder = os.path.join(PLUGIN_DIR, name)

    if os.path.exists(plugin_folder):
        shutil.rmtree(plugin_folder)

    os.makedirs(plugin_folder)

    api_url = f"https://api.github.com/repos/rusher-code-330/PGR-Tools-Plugin/contents/{name}"

    r = requests.get(api_url)

    if r.status_code != 200:
        print("| plugin not found")
        return

    files = r.json()
    plugin_json_data = None

    for file in files:
        if file["type"] == "file":
            file_name = file["name"]
            download_url = file["download_url"]

            file_request = requests.get(download_url)

            if file_request.status_code == 200:
                with open(os.path.join(plugin_folder, file_name), "wb") as f:
                    f.write(file_request.content)

                if file_name == "plugin.json":
                    plugin_json_data = json.loads(file_request.text)

    if plugin_json_data:
        install_requirements(plugin_json_data)

    sync_installed()
    print(Fore.CYAN + f"| {name} installed")
    if plugin_json_data and "description" in plugin_json_data:
        print(f"| {plugin_json_data['description']}")

    if plugin_json_data and "developer" in plugin_json_data:
        print(f"| {plugin_json_data['developer']}")

    if plugin_json_data and "version" in plugin_json_data:
        print(f"| {plugin_json_data['version']}" + Style.RESET_ALL)


def uninstall_plugin(name):
    plugin_folder = os.path.join(PLUGIN_DIR, name)

    if os.path.exists(plugin_folder):
        shutil.rmtree(plugin_folder)
        sync_installed()
        print(f"| {name} removed")
    else:
        print("| plugin not installed")


def update_plugin(name):
    uninstall_plugin(name)
    install_plugin(name)


def info_plugin(name):
    api_url = f"https://api.github.com/repos/rusher-code-330/PGR-Tools-Plugin/contents/{name}"

    r = requests.get(api_url)

    if r.status_code != 200:
        print(Fore.RED + "| error" + Style.RESET_ALL)
        return

    files = r.json()

    for file in files:
        if file["name"] == "plugin.json":
            file_request = requests.get(file["download_url"])
            plugin_json_data = json.loads(file_request.text)

            print(Fore.CYAN + f"| name              : {plugin_json_data.get('name', 'N/A')}")
            print(f"| developer         : {plugin_json_data.get('developer', 'N/A')}")
            print(f"| version           : {plugin_json_data.get('version', 'N/A')}")
            print(f"| description       : {plugin_json_data.get('description', 'N/A')}")
            print(f"| requires (pip)    : {plugin_json_data.get('requires', [])}")
            print(f"| requires (system) : {plugin_json_data.get('requires_system', [])}" + Style.RESET_ALL)
            return

    print(Fore.RED + "| no plugin.json found" + Style.RESET_ALL)


def list_index():
    api_url = "https://api.github.com/repos/rusher-code-330/PGR-Tools-Plugin/contents"

    r = requests.get(api_url)

    if r.status_code != 200:
        print("| github error")
        return

    data = r.json()

    print(Fore.CYAN + "\n___AVAILABLE PLUGIN___")
    for item in data:
        if item["type"] == "dir":
            print("-", item["name"])

    print("________________________" + Style.RESET_ALL)


def list_plugins():
    installed = sync_installed()

    print(Fore.CYAN + "\n___ INSTALLED PLUGINS ___")
    for p in installed:
        print("-", p)
    print("_________________________" + Style.RESET_ALL)


# ============================================================
# SYSTEM COMMANDS (process, sysinfo, etc.)
# ============================================================

def search_process(name):
    """Recherche un processus selon l'OS"""
    plat = detect_platform()

    if plat == "windows":
        cmd = f'tasklist | findstr /I "{name}"'
    else:  # linux, termux
        cmd = f'pgrep -fl "{name}"'

    os.system(cmd)


def kill_process(target):
    """Tue un processus par PID ou nom selon l'OS"""
    plat = detect_platform()

    if plat == "windows":
        if target.isdigit():
            cmd = f'taskkill /PID {target} /F'
        else:
            cmd = f'taskkill /IM "{target}" /F'
    else:  # linux, termux
        if target.isdigit():
            cmd = f'kill -9 {target}'
        else:
            cmd = f'pkill -9 -f "{target}"'

    os.system(cmd)


def list_processes():
    """Liste tous les processus selon l'OS"""
    plat = detect_platform()

    if plat == "windows":
        cmd = 'tasklist'
    else:  # linux, termux
        cmd = 'ps aux'

    os.system(cmd)


def clear_screen():
    """Clear l'écran selon l'OS"""
    plat = detect_platform()

    if plat == "windows":
        os.system('cls')
    else:
        os.system('clear')


def show_sysinfo():
    """Affiche les infos système selon l'OS"""
    plat = detect_platform()

    print(Fore.CYAN + "\n___ SYSTEM INFO ___" + Style.RESET_ALL)
    print(f"| platform détectée : {plat}")
    print(f"| OS                : {platform.system()} {platform.release()}")
    print(f"| python            : {sys.version.split()[0]}")

    if plat == "windows":
        os.system('systeminfo | findstr /C:"OS Name" /C:"OS Version" /C:"Total Physical Memory"')
    elif plat == "termux":
        os.system('uname -a')
        os.system('df -h /data')
    else:
        os.system('uname -a')
        os.system('free -h')

    print(Fore.CYAN + "____________________" + Style.RESET_ALL)


def open_path(path):
    """Ouvre un fichier/dossier selon l'OS"""
    plat = detect_platform()

    if plat == "windows":
        os.system(f'start "" "{path}"')
    elif plat == "termux":
        os.system(f'termux-open "{path}"')
    else:
        os.system(f'xdg-open "{path}"')


def network_info():
    """Affiche les infos réseau selon l'OS"""
    plat = detect_platform()

    if plat == "windows":
        os.system('ipconfig')
    else:  # linux, termux
        os.system('ifconfig 2>/dev/null || ip addr')


# ============================================================
# MAIN
# ============================================================

plugins = load_plugins()

text = pyfiglet.figlet_format(" WELCOME TO PGR TOOLS  V2.1.3 BETA", font="standard")
print(Fore.CYAN + text + Style.RESET_ALL)

print("write " + Fore.CYAN + "pgr help" + Style.RESET_ALL + " to view all pgr")
print(Fore.RED + "created by rusher" + Style.RESET_ALL)
print(Fore.CYAN + f"| platform détectée : {detect_platform()}" + Style.RESET_ALL)

while True:

    pgr = input("|> ")

    if pgr.startswith("pgr install "):
        name = pgr.split(" ")[2]
        install_plugin(name)
        plugins = load_plugins()

    elif pgr.startswith("pgr uninstall "):
        name = pgr.split(" ")[2]
        uninstall_plugin(name)
        plugins = load_plugins()

    elif pgr.startswith("pgr update "):
        name = pgr.split(" ")[2]
        update_plugin(name)
        plugins = load_plugins()

    elif pgr == "pgr list":
        list_plugins()

    elif pgr.startswith("pgr config"):
        parts = pgr.split(" ")
        cfg = load_config()

        if pgr == "pgr config" or pgr == "pgr config show":
            config_menu()

        elif len(parts) == 4 and parts[2] == "platform":
            value = parts[3]
            if value in ["termux", "linux", "windows", "auto"]:
                cfg["platform"] = value
                save_config(cfg)
                print(Fore.CYAN + f"| platform réglée sur : {value}" + Style.RESET_ALL)
            else:
                print(Fore.RED + "| valeur invalide (termux/linux/windows/auto)" + Style.RESET_ALL)

        elif len(parts) >= 4 and parts[2] == "pip":
            cmd = " ".join(parts[3:])
            cfg["pip_command"] = cmd
            save_config(cfg)
            print(Fore.CYAN + f"| pip command réglée sur : {cmd}" + Style.RESET_ALL)

        elif pgr == "pgr config reset":
            save_config(DEFAULT_CONFIG.copy())
            print(Fore.CYAN + "| config réinitialisée" + Style.RESET_ALL)

        else:
            config_menu()

    elif pgr in plugins:
        try:
            plugins[pgr].run()
        except Exception as e:
            print("| plugin error:", e)

    elif pgr.startswith("pgr info "):
        name = pgr.split(" ")[2]
        info_plugin(name)

    elif pgr == "pgr cli uninstall":
        print(Fore.RED + "| uninstalling PGR Tools..." + Style.RESET_ALL)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.system(f"rm -rf '{current_dir}'")
        print(Fore.CYAN + "| PGR Tools removed" + Style.RESET_ALL)
        exit()

    elif pgr == "pgr cli restart":
        print(Fore.CYAN + "| PGR Tools restart. . ." + Style.RESET_ALL)
        os.execl(sys.executable, sys.executable, *sys.argv)

    elif pgr == "pgr cli update":
        print("| updating PGR tools...")
        os.system("cd ~/pgr-tools && git pull")
        print(Fore.CYAN + "| PGR Tools restart. . ." + Style.RESET_ALL)
        os.execl(sys.executable, sys.executable, *sys.argv)

    elif pgr == "pgr v":
        print(Fore.CYAN + "| PGRTools v2.1.3 BETA" + Style.RESET_ALL)

    elif pgr == "pgr index":
        list_index()

    elif pgr == "pgr ffmpeg check":
        check_ffmpeg()

    elif pgr.startswith("pgr ps "):
        name = pgr.split(" ", 2)[2]
        search_process(name)

    elif pgr == "pgr ps":
        list_processes()

    elif pgr.startswith("pgr kill "):
        target = pgr.split(" ", 2)[2]
        kill_process(target)

    elif pgr == "pgr clear":
        clear_screen()

    elif pgr == "pgr sysinfo":
        show_sysinfo()

    elif pgr.startswith("pgr open "):
        path = pgr.split(" ", 2)[2]
        open_path(path)

    elif pgr == "pgr net":
        network_info()

    elif pgr == "pgr help":
        print(Fore.CYAN + "| PROGRAMME :\n")
        print("| pgr install {name}")
        print("| pgr uninstall {name}")
        print("| pgr update {name}")
        print("| pgr list")
        print("| pgr info {name}")
        print("| pgr index")
        print("| pgr config")
        print("| pgr ffmpeg check")
        print("| pgr ps")
        print("| pgr ps {name}")
        print("| pgr kill {pid|name}")
        print("| pgr clear")
        print("| pgr sysinfo")
        print("| pgr open {path}")
        print("| pgr net")
        print("| pgr cli restart")
        print("| pgr cli update")
        print("| pgr cli uninstall")
        print("| pgr v")
        print("| pgr exit" + Style.RESET_ALL)

    elif pgr == "pgr exit":
        break

    else:
        print("| unknown command")
