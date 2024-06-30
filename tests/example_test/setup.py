from time import sleep


def main():
    print("Setting up the environment for example_test")
    # Setup logic here

    while True:
        print("setup running\n\n")
        sleep(1)


# -> This functill will be called when the test end, and summary of the test will be in the kwargs,
def tests_results(*args, **kwargs):
    """
    kwargs contain a list of the following:
    - test duration
    - test result status (passed or failes)
    - events complete (list)
    - events missing to be complete (list)
    """
    return True


# -> This function will handle a extra verification step in the end of each test, return false fail the test
def validate_test(test: str):
    """
    Adds a extra validation in the end of each test allowing you to do some cleanup or fail the test if needed!
    """
    print(f"extra validation for test: {test}")
    return True


## -> This function will handle a extra verification step in the end of the others that you migh want to add
# def final_test_validation():
#     """
#     Return only accept boolen, none will be false and false fail the test!
#     """
#     return True
