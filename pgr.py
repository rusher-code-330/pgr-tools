import os
import importlib.util
import requests
import json
import sys
from colorama import init, Fore, Style
import pyfiglet

init()

PLUGIN_DIR = "plugins"
BASE_URL = "https://raw.githubusercontent.com/rusher-code-330/PGR-Tools-Plugin/main"
INSTALLED_FILE = "installed.json"

if not os.path.exists(PLUGIN_DIR):
    os.makedirs(PLUGIN_DIR)

if not os.path.exists(INSTALLED_FILE):
    with open(INSTALLED_FILE, "w") as f:
        json.dump([], f)

def get_installed():
    with open(INSTALLED_FILE, "r") as f:
        return json.load(f)

def save_installed(data):
    with open(INSTALLED_FILE, "w") as f:
        json.dump(data, f)

def load_plugins():
    plugins = {}

    for file in os.listdir(PLUGIN_DIR):

        if file.endswith(".py"):

            name = file[:-3]
            path = os.path.join(PLUGIN_DIR, file)

            try:
                spec = importlib.util.spec_from_file_location(name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                plugins[name] = module

            except Exception as e:
                print(f"| failed loading plugin: {name}")
                print(e)

    return plugins

def install_requirements(code):
    try:
        import re

        match = re.search(r"REQUIRES\s*=\s*\[(.*?)\]", code)

        if not match:
            return

        raw = match.group(1)

        packages = [
            p.strip().replace('"', '').replace("'", "")
            for p in raw.split(",")
        ]

        for pkg in packages:
            if pkg:
                print(f"| installing dependency: {pkg}")
                os.system(f"{sys.executable} -m pip install {pkg}")

    except Exception as e:
        print("| dependency error:", e)

def install_plugin(name):
    url = f"{BASE_URL}/{name}.py"
    r = requests.get(url)

    if r.status_code == 200:

        code = r.text

        install_requirements(code)

        with open(f"{PLUGIN_DIR}/{name}.py", "w") as f:
            f.write(code)

        installed = get_installed()

        if name not in installed:
            installed.append(name)
            save_installed(installed)

        print(f"| {name} installed")

    else:
        print("| plugin not found")

def uninstall_plugin(name):
    path = f"{PLUGIN_DIR}/{name}.py"

    if os.path.exists(path):
        os.remove(path)

        installed = get_installed()

        if name in installed:
            installed.remove(name)
            save_installed(installed)

        print(f"| {name} removed")

    else:
        print("| plugin not installed")

def update_plugin(name):
    uninstall_plugin(name)
    install_plugin(name)

def list_plugins():
    installed = get_installed()

    print("\n___ INSTALLED PLUGINS ___")
    for p in installed:
        print("-", p)
    print("_________________________")

plugins = load_plugins()

text = pyfiglet.figlet_format("PGR TOOLS v2.0.1", font="standard")
print(Fore.CYAN + text + Style.RESET_ALL)

print("write " + Fore.CYAN + "pgr help" + Style.RESET_ALL + " to view commands")
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

    elif pgr == "pgr cli restart":
        print("| restarting...")
        os.execl(sys.executable, sys.executable, *sys.argv)

    elif pgr == "pgr cli uninstall":
        print("| removing PGR Tools...")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.system(f"rm -rf '{current_dir}'")
        exit()

    elif pgr == "pgr help":
        print(Fore.CYAN + "| COMMANDS:\n")
        print("| pgr install {name}")
        print("| pgr uninstall {name}")
        print("| pgr update {name}")
        print("| pgr list")
        print("| pgr cli restart")
        print("| pgr cli uninstall")
        print("| pgr exit" + Style.RESET_ALL)

    elif pgr == "pgr exit":
        break

    else:
        print("| unknown command")
