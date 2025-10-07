from dataclasses import dataclass
from typing import List, Optional
from .order_item import OrderItem
from .customer import Customer

@dataclass
class Order:
    id: Optional[int]
    customer: Customer
    items: List[OrderItem]
    total: float
    status: str
    date: str
