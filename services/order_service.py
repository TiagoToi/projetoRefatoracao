from datetime import datetime
from typing import List

from models.order import Order
from models.order_item import OrderItem
from models.customer import Customer
from interfaces.iorder_repository import IOrderRepository
from interfaces.istock_validator import IStockValidator
from interfaces.discount_strategy import DiscountStrategy
from strategies.discount_strategy import SpecialPricingStrategyNoVip
from interfaces.inotification_service import INotificationService


# ============================ ESTOQUE (VALIDADOR) ============================


class BasicStockValidator(IStockValidator):
    """
    Classe responsável por validar se os itens do pedido existem e têm estoque suficiente.
    Simula um pequeno inventário interno.
    """
    def validate_items(self, items: List[OrderItem]) -> bool:
        inventory = {'produto1': 100, 'produto2': 50, 'produto3': 75}
        for item in items:
            if item.name not in inventory:
                raise ValueError(f"Produto {item.name} não encontrado!")
            if inventory[item.name] < item.quantity:
                raise ValueError(f"Estoque insuficiente para {item.name}!")
        return True


# ============================ SERVIÇOS DE PEDIDO ============================
class OrderService:
    def __init__(self, repository: IOrderRepository, stock_validator: IStockValidator,
                 pricing_strategy: DiscountStrategy, notifier: INotificationService):
        self.repository = repository
        self.stock_validator = stock_validator
        self.pricing_strategy = pricing_strategy
        self.notifier = notifier

    def add_order(self, client_name: str, items: List[dict] | List[OrderItem], client_type: str) -> int:
        order_items = [
            item if isinstance(item, OrderItem)
            else OrderItem(name=item['nome'], price=item['p'],
                           quantity=item['q'], discount_type=item['tipo'])
            for item in items
        ]
        self.stock_validator.validate_items(order_items)
        total_value = self.pricing_strategy.compute_total(order_items, client_type)
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        customer = Customer(name=client_name, client_type=client_type)
        order = Order(id=None, customer=customer, items=order_items,
                      total=total_value, status='pendente', date=now_str)
        order_id = self.repository.create_order(order)
        self._notify_new_order(client_name)
        return order_id

    def _notify_new_order(self, client_name: str) -> None:
        self.notifier.notify_new_order(client_name, special=False)

    def update_status(self, order_id: int, new_status: str) -> None:
        order = self.repository.get_order(order_id)
        if not order:
            raise ValueError(f"Pedido {order_id} não encontrado.")
        self.repository.update_status(order_id, new_status)
        order.status = new_status
        self.notifier.notify_status_change(order, new_status)

    def calculate_total_by_client(self, client_name: str) -> float:
        return self.repository.get_total_by_client(client_name)

    def generate_sales_report(self) -> None:
        orders = self.repository.get_all_orders()
        print("=== RELATÓRIO DE VENDAS ===")
        total_sales = sum(o.total for o in orders)
        for o in orders:
            print(f"Pedido #{o.id} - Cliente: {o.customer.name} - Total: R${o.total:.2f} - Status: {o.status}")
        print(f"Total Geral: R${total_sales:.2f}")
        with open('rel_vendas.txt', 'w') as f:
            f.write(f"Total de vendas: {total_sales}")

    def generate_clients_report(self) -> None:
        clients = self.repository.get_distinct_clients()
        print("=== RELATÓRIO DE CLIENTES ===")
        for name, ctype in clients:
            total = self.calculate_total_by_client(name)
            print(f"Cliente: {name} ({ctype}) - Total gasto: R${total:.2f}")
        with open('rel_clientes.txt', 'w') as f:
            for name, ctype in clients:
                f.write(f"{name},{ctype}\n")




class SpecialOrderService(OrderService):
    """
    Serviço especial que usa a estratégia "SpecialPricingStrategyNoVip":
    - ignora desconto VIP
    - aplica +15%
    """
    def __init__(self, repository: IOrderRepository, stock_validator: IStockValidator,
                 notifier: INotificationService):
        super().__init__(repository, stock_validator, SpecialPricingStrategyNoVip(), notifier)

    def _notify_new_order(self, client_name: str) -> None:
        self.notifier.notify_new_order(client_name, special=True)
