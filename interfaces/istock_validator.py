from abc import ABC, abstractmethod
from typing import List
from models.order_item import OrderItem

class IStockValidator(ABC):
    @abstractmethod
    def validate_items(self, items: List[OrderItem]) -> bool:
        ...
