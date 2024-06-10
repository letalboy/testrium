import os
import time
import importlib.util
import toml
from colorama import init, Fore, Style
import shutil
from .utils import Events_Manager

# Initialize colorama
init(autoreset=True)

# Loads the config for each test:
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
            func = getattr(module, attr)
            if callable(func) and not attr.startswith('_'):
                test_functions[attr] = func
    return test_functions

# Run setup of the test group
def run_setup(setup_path):
    spec = importlib.util.spec_from_file_location("setup", setup_path)
    setup_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(setup_module)
    setup_module.main()

# Print the nice Pass or Fail banners
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
    
    # -> Discover valid test folders with configs inside
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
    
    # -> Early retun if not find any test:
    if tests_finded > 0:
        print(f"{Fore.GREEN} Find: {tests_finded:.0f} valid test groups!")
        for test_group in valid_test_dirs:
            print(f"{Fore.GREEN} - {test_group}")
    else:
        print(f"{Fore.RED} No valid test groups finded!")
        return

    # TODO >>> Find a way to log the milestones completed for each test and with this understand what they relate to
    
    tests_passed = {}
    
    # -> Run the valid tests:
    for dir_name in valid_test_dirs:
        
        Events_Manager(Unit="", path=base_dir).drop_events_table()
        
        dir_path = os.path.join(base_dir, dir_name)
        setup_path = os.path.join(dir_path, 'setup.py')
        
        #> Load test configs
        config_path = os.path.join(dir_path, 'config.toml')
        configs = load_config(config_path)
        
        #> Load Units
        confs = configs['Configs']
        units = confs['units']
        
        #> Load Units Predefinitions
        total_units = 0
        units_index = {}
        for unit in units:
            un = configs[f"{unit}"]
            units_index[un["init"]] = {"name":f"{unit}", "events": f"{un['events']}"}
            total_units += 1
            
        print(f"Units loaded: {units_index}")
        
        # TODO >>> Use the units order to setup the units one by one
        # TODO >>> Create a meachanism to verify the events when they are required
            
        print(f"{Fore.BLUE}Loading tests for {dir_name}...")
        test_functions = load_test_functions(dir_path)
        
        all_tests_passed = True
        tests_completed = []
        
        #> Run each test found in the test group
        for test_name, test_func in test_functions.items():
            print(f"{Fore.YELLOW}Running test: {test_name}")
            start_time = time.time()
            
            try:
                if test_name == 'log_test_time':
                    test_func(dummy_function)  # Pass a dummy function if required
                elif test_name == 'verify_condition':
                    # TODO >>> Use this as a condition to verify if the requirements was completed for the test case
                    test_func(lambda: True)  # Pass a lambda function if required
                else:
                    test_func()
                elapsed_time = time.time() - start_time
                print(f"{Fore.GREEN}{test_name}: PASSED in {elapsed_time:.2f} seconds")
                tests_completed.append({"name":test_name, "passed":True})
            except Exception as e:
                all_tests_passed = False
                elapsed_time = time.time() - start_time
                print(f"{Fore.RED}{test_name}: FAILED in {elapsed_time:.2f} seconds\nError: {e}")
                tests_completed.append({"name":test_name, "passed":False})
        
        tests_passed[f"{dir_name}"] = tests_completed
        
        #> Verify Events Completed By The Unit
        for i in range(total_units):
            unit = units_index[i]
            unit_name = unit["name"]
            if unit_name == "":
                continue
            unit_events = Events_Manager(Unit=unit_name, path=base_dir).List_Events()
            for event in eval(unit["events"]):
                if event not in unit_events:
                    print(f"event: [{event}] was not completed!")
                    all_tests_passed = False
                    
        if all_tests_passed:
            print_banner(" PASS ", Fore.GREEN)
        else:
            print_banner(" FAILURE ", Fore.RED)
            
    for name, tests in tests_passed.items():
        print("-="*15)
        print(f"{Fore.CYAN}{name}:")
        all_p = True
        for test in tests:
            if test["passed"]:
                print(f"✅ {Fore.GREEN}{test['name']}")
            else:
                print(f"🟥 {Fore.RED}{test['name']}")
                all_p = False
        if all_p:
            print(f"🚀 {Fore.GREEN}All Tests Passed!")
        

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
