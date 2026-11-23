import functools
import time


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper


def timer_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cur_time = time.perf_counter()
        result = func(*args, **kwargs)
        timer_time = time.perf_counter() - cur_time
        print(f"slow_sum took {timer_time:.4f} s")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b


# total = add(2, 3)
# print(total)
# print(add.__name__)
# add(10, b=5)
# print(add.__name__)

@timer_log
def slow_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total


print(slow_sum(1_000_000))
print(slow_sum.__name__)