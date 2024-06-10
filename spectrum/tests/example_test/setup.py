def main():
    print("Setting up the environment for example_test")
    # Setup logic here

# -> This functill will be called when the test end, and summary of the test will be in the kwargs
def end_callback(**kwargs):
    """
    kwargs contain:
    - test duration
    - test that passed
    - test that failed
    - events complete
    - events missing to be complete
    """
    pass

# -> This function will handle a extra verification step in the end of the others that you migh want to add
def extra_step():
    """
    Return only accept boolen, none will be false and false fail the test!
    """
    pass