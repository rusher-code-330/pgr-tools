import os
import importlib
import requests
import json
from colorama import init, Fore
from colorama import init, Style
import pyfiglet
import sys

PLUGIN_DIR = "plugins"
BASE_URL = "https://raw.github.com/rusher-code-330/PGR-Tools-Plugin/main/"
INSTALLED_FILE = "installed.json"


if not os.path.exists(PLUGIN_DIR):
    os.makedirs(PLUGIN_DIR)

if not os.path.exists(INSTALLED_FILE):
    with open(INSTALLED_FILE, "w") as f:
        json.dump([], f)



def load_plugins():

    plugins = {}

    for file in os.listdir(PLUGIN_DIR):

        if file.endswith(".py"):

            name = file[:-3]

            try:

                module_name = f"plugins.{name}"

                # reload si déjà chargé
                if module_name in sys.modules:
                    module = importlib.reload(sys.modules[module_name])

                else:
                    module = importlib.import_module(module_name)

                plugins[name] = module

            except Exception as e:
                print(f"| failed loading plugin: {name}")
                print(e)

    return plugins



def save_installed(data):
    with open(INSTALLED_FILE, "w") as f:
        json.dump(data, f)


def get_installed():
    with open(INSTALLED_FILE, "r") as f:
        return json.load(f)



def install_plugin(name):
    url = f"{BASE_URL}/{name}.py"
    r = requests.get(url)

    if r.status_code == 200:
        with open(f"{PLUGIN_DIR}/{name}.py", "w") as f:
            f.write(r.text)

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




text = pyfiglet.figlet_format (" WELCOME TO PGR TOOLS  V2.0.1 BETA",  font="standard")
print(Fore.CYAN + text + Style.RESET_ALL)

print ("write " + Fore.CYAN + "pgr help"+	Style.RESET_ALL +" to view all pgr")
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
        plugins[pgr].run()
        
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
        print(Fore.CYAN + "| PGRTools	v2.0.1 BETA" + Style.RESET_ALL)
        
        
    elif pgr == "pgr help":
    	print(Fore.CYAN + "| PROGRAMME :\n")
    	print("| pgr install {name}")
    	print("| pgr uninstall {name}")
    	print("| pgr update {name}")
    	print("| pgr list")
    	print("| pgr cli restart")
    	print("| pgr cli update")
    	print("| pgr cli uninsinstall")
    	print("| pgr exit" + Style.RESET_ALL)

    elif pgr == "pgr exit":
        break

    else:
        print("| unknown command")