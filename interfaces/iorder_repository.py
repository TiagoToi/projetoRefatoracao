from abc import ABC, abstractmethod
from typing import List, Optional
from models.order import Order
from models.order_item import OrderItem
from models.customer import Customer

class IOrderRepository(ABC):
    @abstractmethod
    def create_order(self, order: Order) -> int:
        ...
    @abstractmethod
    def get_order(self, order_id: int) -> Optional[Order]:
        ...
    @abstractmethod
    def update_status(self, order_id: int, new_status: str) -> None:
        ...
    @abstractmethod
    def get_all_orders(self) -> List[Order]:
        ...
    @abstractmethod
    def get_distinct_clients(self) -> List[tuple[str, str]]:
        ...
    @abstractmethod
    def get_total_by_client(self, client_name: str) -> float:
        ...
    @abstractmethod
    def close(self) -> None:
        ...
