from abc import ABC, abstractmethod


class ChatModel(ABC):
    """
    Abstract base class for chat models.
    """

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def send_message(self, message: str, stream: bool = False, **kwargs) -> str:
        raise NotImplementedError
