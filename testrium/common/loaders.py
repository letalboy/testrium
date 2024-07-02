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


def discover_tests(base_dir: str):
    dir_names = os.listdir(base_dir)
    valid_test_dirs = []

    # -> Discover valid test folders with configs inside
    for dir_name in dir_names:
        dir_path = os.path.join(base_dir, dir_name)

        if not os.path.isdir(dir_path):
            print(f"{Fore.RED} File: {dir_name} is not a folder")
            continue

        setup_path = os.path.join(dir_path, "setup.py")
        config_path = os.path.join(dir_path, "config.toml")

        if not (os.path.exists(setup_path) and os.path.exists(config_path)):
            print(f"{Fore.RED} File: {dir_name} invalid test")
            continue

        print(f"{Fore.MAGENTA}Found test directory: {dir_name}")
        valid_test_dirs.append(dir_name)

    return valid_test_dirs
