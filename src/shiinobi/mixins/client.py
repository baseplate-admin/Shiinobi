from shiinobi.utilities.session import session

__all__ = ["ClientMixin"]


class ClientMixin:
    """
    Base mixin that includes:
        - session
    """

    def __init__(self, *args, **kwargs) -> None:
        # Client
        self.client = session
