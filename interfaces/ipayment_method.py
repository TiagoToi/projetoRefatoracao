from abc import ABC, abstractmethod
from models.order import Order

class IPaymentMethod(ABC):
    @abstractmethod
    def pay(self, order: Order) -> str:
        ...
