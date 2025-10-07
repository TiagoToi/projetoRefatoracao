from abc import ABC, abstractmethod
from models.order import Order

class INotificationService(ABC):
    @abstractmethod
    def notify_new_order(self, client_name: str, special: bool = False) -> None:
        ...
    @abstractmethod
    def notify_status_change(self, order: Order, new_status: str) -> None:
        ...
