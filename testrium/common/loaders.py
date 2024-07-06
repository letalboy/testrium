# Loads the config for each test:
import os
import importlib.util
import toml
from colorama import Fore


def load_config(config_path):
    print(f"{Fore.CYAN}Loading config from {config_path}")
    with open(config_path, "r") as file:
        config = toml.load(file)
    return config


# Loads the test functions:
def load_test_functions(dir_path):
    test_functions = {}
    for filename in os.listdir(dir_path):
        if filename.startswith("_") or not filename.endswith(".py"):
            continue
        if filename == "setup.py":
            continue

        module_name = filename[:-3]
        file_path = os.path.join(dir_path, filename)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for attr in dir(module):
            if attr == "Events_Manager":
                continue

            func = getattr(module, attr)
            if callable(func) and not attr.startswith("_"):
                test_functions[attr] = func

    return test_functions


def load_special_callbakcs(dir_path):
    """
    This method is used to load the special functions that are:
    - test_validation
    - test_results_handler

    This helper callbacks allows more dinamic patterns to emerge
    """

    def get_fn(module, attr):
        func = getattr(module, attr)
        if callable(func) and not attr.startswith("_"):
            return func

    special_callbacks = {
        "validate_test": None,
        "tests_results": None,
    }

    for filename in os.listdir(dir_path):
        if filename.startswith("_") or not filename.endswith(".py"):
            continue
        module_name = filename[:-3]
        file_path = os.path.join(dir_path, filename)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for attr in dir(module):
            if attr == "validate_test":
                special_callbacks[attr] = get_fn(module, attr)

            elif attr == "tests_results":
                special_callbacks[attr] = get_fn(module, attr)

            else:
                continue

    return special_callbacks


def discover_tests(base_dir: str, exclude_tests: list):
    dir_names = os.listdir(base_dir)
    valid_tests = []

                    
    # -> Discover valid test folders with configs inside
    for dir_name in dir_names:
        if dir_name in exclude_tests:
        # Se estiver na lista de exclusão, imprime uma mensagem informando que foi excluído
         print(f"Excluded test directory: {dir_name}")
        # Continua para o próximo diretório sem adicionar à lista de diretórios válidos
         continue
         
        dir_path = os.path.join(base_dir, dir_name)

        if "test" not in dir_name:
            continue

        if not os.path.isdir(dir_path):
            print(f"{Fore.RED} File: {dir_name} is not a folder")
            continue

        setup_path = os.path.join(dir_path, "setup.py")
        config_path = os.path.join(dir_path, "config.toml")
        unit_path = os.path.join(dir_path, "units")
        
       
        if not os.path.isdir(unit_path):
            continue
        
        # ! TODO: Valid units to use later on.
        units = resolve_units(unit_path, config_path)

        if not (os.path.exists(setup_path) and os.path.exists(config_path)):
            print(f"{Fore.RED} File: {dir_name} invalid test")
            continue

        print(f"{Fore.MAGENTA}Found unit directory: {dir_name}")
        valid_tests.append((dir_name, units))

    return valid_tests


def validate_unit(config):
    validations = {
        "config": type(config) is dict,
        "init": config.get("init") is not None and type(config.get("init")) is int and config.get("init") >= 0,
        "in-except": config.get("in-except") is not None and config.get("in-except") in ["Resume", "Reload", "Resume-ALL"],
        "events": config.get("events") is not None and type(config["events"]) is list and all(isinstance(event, str) for event in config["events"]),
        "use_setup": config.get("use_setup") is None or type(config.get("use_setup")) is bool,
        "unit_dependencies": config.get("unit_dependencies") is None or type(config.get("unit_dependencies"))\
                            is list and all(isinstance(event, str) for event in config.get("unit_dependencies")),
    }
    return all(validations.values())

def resolve_units(path: str, config_path):
    units = []
    config = load_config(config_path)

    for file in os.listdir(path):
        if not file.endswith(".toml"):
            continue

        filename = file.replace(".toml", "")
        if filename not in config["Configs"]["units"]:
            continue

        unit_path = os.path.join(path, file)
        unit_config = load_config(unit_path)[filename]
        unit_config["name"] = filename
        if not validate_unit(unit_config):
            print(f" {Fore.GREEN}{file} is invalid")
            continue

        print(f" {Fore.GREEN}{file} is valid")
        units.append(unit_config)
    return units




