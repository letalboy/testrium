import os
import time
import importlib.util
import toml
from colorama import init, Fore, Style
import shutil

# Initialize colorama
init(autoreset=True)

def load_config(config_path):
    print(f"{Fore.CYAN}Loading config from {config_path}")
    with open(config_path, 'r') as file:
        config = toml.load(file)
    return config

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
            func = getattr(module, attr)
            if callable(func) and not attr.startswith('_'):
                test_functions[attr] = func
    return test_functions

def print_banner(message, color=Fore.GREEN):
    term_width = shutil.get_terminal_size().columns
    message_length = len(message)
    padding_length = (term_width - message_length) // 2
    banner = "=" * padding_length + message + "=" * padding_length

    # Ensure the banner fits exactly in the terminal width
    if len(banner) < term_width:
        banner += "=" * (term_width - len(banner))

    print(color + banner)

def main():
    base_dir = os.getcwd()
    print(f"{Fore.GREEN}Current working directory: {base_dir}")

    dir_names = os.listdir(base_dir)
    valid_test_dirs = []
        
    for dir_name in dir_names:
        dir_path = os.path.join(base_dir, dir_name)
        
        if not os.path.isdir(dir_path):
            print(f"{Fore.RED} File: {dir_name} is not a folder")
            continue
        
        setup_path = os.path.join(dir_path, 'setup.py')
        config_path = os.path.join(dir_path, 'config.toml')

        if not (os.path.exists(setup_path) and os.path.exists(config_path)):
            print(f"{Fore.RED} File: {dir_name} invalid test")
            continue
        
        print(f"{Fore.MAGENTA}Found test directory: {dir_name}")
        valid_test_dirs.append(dir_name)
        
    tests_finded = len(valid_test_dirs)
    
    if tests_finded > 0:
        print(f"{Fore.GREEN} Find: {tests_finded:.0f} valid test groups!")
        for test_group in valid_test_dirs:
            print(f"{Fore.GREEN} - {test_group}")
    else:
        print(f"{Fore.RED} No valid test groups finded!")
        return
    
    # -> RUN THE VALID TESTS:
    
    for dir_name in valid_test_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        setup_path = os.path.join(dir_path, 'setup.py')
        
        print(f"{Fore.BLUE}Loading tests for {dir_name}...")
        test_functions = load_test_functions(dir_path)
        
        all_tests_passed = True
        
        for test_name, test_func in test_functions.items():
            print(f"{Fore.YELLOW}Running test: {test_name}")
            start_time = time.time()
            try:
                if test_name == 'log_test_time':
                    test_func(dummy_function)  # Pass a dummy function if required
                elif test_name == 'verify_condition':
                    test_func(lambda: True)  # Pass a lambda function if required
                else:
                    test_func()
                elapsed_time = time.time() - start_time
                print(f"{Fore.GREEN}{test_name}: PASSED in {elapsed_time:.2f} seconds")
            except Exception as e:
                all_tests_passed = False
                elapsed_time = time.time() - start_time
                print(f"{Fore.RED}{test_name}: FAILED in {elapsed_time:.2f} seconds\nError: {e}")

        if all_tests_passed:
            print_banner(" PASS ", Fore.GREEN)
        else:
            print_banner(" FAILURE ", Fore.RED)

# Extra validation step that user migh want to define
def dummy_function():
    """
    - This will allow to define a extra step in the verification
    for example, read a file and validate if the test was a success.
    see if the code did what it was suposed to do. etc..
    """
    pass

if __name__ == "__main__":
    main()
