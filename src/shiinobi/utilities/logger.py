import logging

__all__ = ["get_logger"]


def get_logger() -> logging.Logger:
    return logging.getLogger("shiinobi")
