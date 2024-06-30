from testrium.common.utils import verify_condition
from testrium.modules.events import Events_Manager
import os

THIS_DIR = os.path.dirname(__file__)

def test_example():
    print("Running test_example")
    result = 1 + 1
    
    Events_Manager(Unit="Primary", path=THIS_DIR).Set_Event(
        step=f"Test example completed", event_type="Default"
    )
    
    verify_condition(result == 2, "1 + 1 should be 2")

# def test_failure():
#     print("Running test_failure")
#     result = 1 + 1
#     verify_condition(result == 3, "1 + 1 should be 3")

