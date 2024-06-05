import os
import time
import importlib.util
import toml
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def load_config(config_path):
    print(f"{Fore.CYAN}Loading config from {config_path}")
    with open(config_path, 'r') as file:
        config = toml.load(file)
    return config

def run_setup(setup_path):
    print(f"{Fore.YELLOW}Running setup script: {setup_path}")
    spec = importlib.util.spec_from_file_location("setup", setup_path)
    setup_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(setup_module)
    setup_module.main()

def load_test_functions(test_dir):
    print(f"{Fore.CYAN}Loading test functions from {test_dir}")
    functions = {}
    for file_name in os.listdir(test_dir):
        if file_name.endswith(".py") and file_name != "setup.py":
            module_name = file_name[:-3]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(test_dir, file_name))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for attr in dir(module):
                if callable(getattr(module, attr)) and attr.startswith("test_"):
                    functions[attr] = getattr(module, attr)
    return functions

def main():
    base_dir = os.getcwd()
    print(f"{Fore.GREEN}Current working directory: {base_dir}")
    for dir_name in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.isdir(dir_path):
            setup_path = os.path.join(dir_path, 'setup.py')
            config_path = os.path.join(dir_path, 'config.toml')

            if os.path.exists(setup_path) and os.path.exists(config_path):
                print(f"{Fore.MAGENTA}Found test directory: {dir_name}")
                run_setup(setup_path)

                print(f"{Fore.BLUE}Loading tests for {dir_name}...")
                test_functions = load_test_functions(dir_path)
                
                for test_name, test_func in test_functions.items():
                    print(f"{Fore.YELLOW}Running test: {test_name}")
                    start_time = time.time()
                    try:
                        test_func()
                        elapsed_time = time.time() - start_time
                        print(f"{Fore.GREEN}{test_name}: PASSED in {elapsed_time:.2f} seconds")
                    except Exception as e:
                        elapsed_time = time.time() - start_time
                        print(f"{Fore.RED}{test_name}: FAILED in {elapsed_time:.2f} seconds\nError: {e}")

if __name__ == "__main__":
    main()
