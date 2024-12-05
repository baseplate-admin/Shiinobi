import functools
from typing import Any, Callable
from shiinobi.utilities.logger import get_logger

__all__ = ["return_on_error"]

logger = get_logger()


def return_on_error[T](return_type: T) -> Callable[[Callable], T]:
    """
    These decorators catch :
        - **AttributeError** : In case `selectolax` fails to find the dom node
        - **IndexError** : In case `selectolax` finds empty dom node
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
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
