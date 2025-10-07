from abc import ABC, abstractmethod
from typing import List
from models.order_item import OrderItem


class DiscountStrategy(ABC):
    @abstractmethod
    def compute_total(self, items: List[OrderItem], client_type: str) -> float:
        ...


class _ItemsOnlyPricingMixin:
    # Calcula total com descontos por item (desc10/desc20), SEM considerar VIP
    def _compute_items_total(self, items: List[OrderItem]) -> float:
        total = 0.0
        for item in items:
            if item.discount_type == 'desc10':
                total += item.price * item.quantity * 0.9
            elif item.discount_type == 'desc20':
                total += item.price * item.quantity * 0.8
            else:
                total += item.price * item.quantity
        return total


class StandardPricingStrategy(DiscountStrategy, _ItemsOnlyPricingMixin):
    # Aplica descontos por item e, se client_type == 'vip', aplica -5% no total
    def compute_total(self, items: List[OrderItem], client_type: str) -> float:
        total = self._compute_items_total(items)
        if client_type == 'vip':
            total *= 0.95
        return total


class SpecialPricingStrategyNoVip(DiscountStrategy, _ItemsOnlyPricingMixin):
    # Replica o legado: ignora VIP e aplica +15% ao final
    def compute_total(self, items: List[OrderItem], client_type: str) -> float:
        base = self._compute_items_total(items)   # sem VIP
        return base * 1.15
