import functools
from typing import Callable, ParamSpec
from shiinobi.utilities.logger import get_logger

__all__ = ["return_on_error"]

logger = get_logger()

P = ParamSpec("P")


def return_on_error[T](return_type: T) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator to handle specific exceptions by returning a default value.

    Catches:
    - AttributeError: When selectolax fails to find DOM node
    - IndexError: When selectolax finds empty DOM node
    - ValueError: Additional error case
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except (AttributeError, IndexError, ValueError) as e:
                func_name = func.__name__
                args_repr = ", ".join(repr(arg) for arg in args)
                kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
                signature = f"{func_name}({args_repr}, {kwargs_repr})"

                logger.warning(f"Found {e} when executing {signature}")
                return return_type

        return wrapper

    return decorator
