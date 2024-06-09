from spectrum.utils import log_test_time, verify_condition, Events_Manager

@log_test_time
def test_example():
    print("Running test_example")
    result = 1 + 1
    
    Events_Manager(Unit="Primary", path="Logs").Set_Event(
        step=f"Test example completed", event_type="Default"
    )
    
    verify_condition(result == 2, "1 + 1 should be 2")

# @log_test_time
# def test_failure():
#     print("Running test_failure")
#     result = 1 + 1
#     verify_condition(result == 3, "1 + 1 should be 3")

