from testrium.common.utils import verify_condition

def test_example():
    print("Running test_example")
    result = 1 + 1
    verify_condition(result == 2, "1 + 1 should be 2")

# def test_failure():
#     print("Running test_failure")
#     result = 1 + 1
#     verify_condition(result == 3, "1 + 1 should be 3")

