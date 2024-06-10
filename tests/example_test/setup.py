def main():
    print("Setting up the environment for example_test")
    # Setup logic here

# -> This functill will be called when the test end, and summary of the test will be in the kwargs
def test_results_handler (*args, **kwargs):
    """
    kwargs contain a list of the following:
    - test duration 
    - test result status (passed or failes)
    - events complete (list)
    - events missing to be complete (list)
    """
    return True

# -> This function will handle a extra verification step in the end of the others that you migh want to add
def extra_test_validation ():
    """
    Return only accept boolen, none will be false and false fail the test!
    """
    return True