from abc import ABC, abstractmethod
from typing import List
from models.order_item import OrderItem

class DiscountStrategy(ABC):
    @abstractmethod
    def compute_total(self, items: List[OrderItem], client_type: str) -> float:
        ...
