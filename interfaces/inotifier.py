from abc import ABC, abstractmethod

class INotifier(ABC):
    @abstractmethod
    def send(self, client_name: str, message: str) -> None:
        ...
