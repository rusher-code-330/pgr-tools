import os
import importlib.util
import requests
import json
from colorama import init, Fore, Style
import pyfiglet
import sys
import shutil

init()

PGR_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.join(PGR_DIR, "plugins")
BASE_URL = "https://raw.githubusercontent.com/rusher-code-330/PGR-Tools-Plugin/main"
INSTALLED_FILE = os.path.join(PGR_DIR, "installed.json")

if not os.path.exists(PLUGIN_DIR):
    os.makedirs(PLUGIN_DIR)

if not os.path.exists(INSTALLED_FILE):
    with open(INSTALLED_FILE, "w") as f:
        json.dump([], f)

def install_requirements(data):
    try:
        if "requires" not in data:
            return
        for pkg in data["requires"]:
            print(f"| installing dependency: {pkg}")
            os.system(f"{sys.executable} -m pip install {pkg}")
    except Exception as e:
        print("| dependency error:", e)


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
    print(f"| {name} installed")


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


def list_plugins():
    installed = sync_installed()

    print("\n___ INSTALLED PLUGINS ___")
    for p in installed:
        print("-", p)
    print("_________________________")


plugins = load_plugins()

text = pyfiglet.figlet_format(" WELCOME TO PGR TOOLS  V2.1.2 BETA", font="standard")
print(Fore.CYAN + text + Style.RESET_ALL)

print("write " + Fore.CYAN + "pgr help" + Style.RESET_ALL + " to view all pgr")
print(Fore.RED + "created by rusher" + Style.RESET_ALL)

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

    elif pgr in plugins:
        try:
            plugins[pgr].run()
        except Exception as e:
            print("| plugin error:", e)

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
        print(Fore.CYAN + "| PGRTools v2.1.2 BETA" + Style.RESET_ALL)

    elif pgr == "pgr help":
        print(Fore.CYAN + "| PROGRAMME :\n")
        print("| pgr install {name}")
        print("| pgr uninstall {name}")
        print("| pgr update {name}")
        print("| pgr list")
        print("| pgr cli restart")
        print("| pgr cli update")
        print("| pgr cli uninstall")
        print("| pgr exit" + Style.RESET_ALL)

    elif pgr == "pgr exit":
        break

    else:
        print("| unknown command")
