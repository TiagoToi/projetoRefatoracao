from dataclasses import dataclass

@dataclass
class OrderItem:
    name: str
    price: float
    quantity: int
    discount_type: str  # 'normal' | 'desc10' | 'desc20'
