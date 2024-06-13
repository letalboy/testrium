# Loads the config for each test:
import os
import importlib.util
import toml
from colorama import Fore

def load_config(config_path):
    print(f"{Fore.CYAN}Loading config from {config_path}")
    with open(config_path, 'r') as file:
        config = toml.load(file)
    return config

# Loads the test functions:
def load_test_functions(dir_path):
    test_functions = {}
    for filename in os.listdir(dir_path):
        if filename.startswith('_') or not filename.endswith('.py'):
            continue
        module_name = filename[:-3]
        file_path = os.path.join(dir_path, filename)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for attr in dir(module):
            if attr == "Events_Manager":
                continue
            if attr == "extra_test_validation":
                continue
            if attr == "test_results_handler":
                continue
            func = getattr(module, attr)
            if callable(func) and not attr.startswith('_'):
                test_functions[attr] = func
    return test_functions

def load_special_callbakcs (dir_path):
    
    """
    This method is used to load the special functions that are:
    - extra_test_validation
    - test_results_handler
    
    This helper callbacks allows more dinamic patterns to emerge
    """
    
    def get_fn (module, attr):
        func = getattr(module, attr)
        if callable(func) and not attr.startswith('_'):
            return func
    
    special_callbacks = {
        "extra_test_validation": None,
        "test_results_handler": None,
    }
    
    for filename in os.listdir(dir_path):
        if filename.startswith('_') or not filename.endswith('.py'):
            continue
        module_name = filename[:-3]
        file_path = os.path.join(dir_path, filename)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        for attr in dir(module):
            if attr == "extra_test_validation":
                special_callbacks[attr] = get_fn(module, attr)
            elif attr == "test_results_handler":
                special_callbacks[attr] = get_fn(module, attr)
            else:
                continue
    
    return special_callbacks