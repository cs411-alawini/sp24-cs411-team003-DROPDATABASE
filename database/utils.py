from functools import wraps
from termcolor import colored
import sys


def err_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Print the error in red
            print(colored(f"Error: {e}", "red"), file=sys.stderr)

    return wrapper
