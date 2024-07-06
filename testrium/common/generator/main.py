import os
import shutil
from colorama import Fore

def resolve_template(type: str, path: str):
    if type == "config-template":
        file_path = os.path.join(os.path.dirname(__file__), "config.toml")
        if not os.path.isdir(path):
            print(f"{Fore.RED} path argument is invalid")
            return
        if os.path.isfile(os.path.join(path, "config.toml")):
            print(f"{Fore.BLUE} config.toml already exists")
            return
        shutil.copy2(file_path, path)

