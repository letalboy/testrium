import time

def log_test_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print(f"{func.__name__} took {elapsed_time:.2f} seconds")
        return result
    return wrapper

def verify_condition(condition, message="Verification failed"):
    if not condition:
        raise AssertionError(message)

