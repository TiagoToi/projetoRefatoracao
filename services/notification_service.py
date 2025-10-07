from abc import ABC, abstractmethod
from models.order import Order


class INotifier(ABC):
    @abstractmethod
    def send(self, client_name: str, message: str) -> None: ...


class EmailNotifier(INotifier):
    def send(self, client_name: str, message: str) -> None:
        print(f'Email enviado para {client_name}: {message}')


class SMSNotifier(INotifier):
    def send(self, client_name: str, message: str) -> None:
        print(f'SMS enviado para {client_name}: {message}')


class INotificationService(ABC):
    @abstractmethod
    def notify_new_order(self, client_name: str, special: bool = False) -> None: ...
    @abstractmethod
    def notify_status_change(self, order: Order, new_status: str) -> None: ...


class NotificationService(INotificationService):
    def __init__(self, email_notifier: INotifier, sms_notifier: INotifier):
        self.email_notifier = email_notifier
        self.sms_notifier = sms_notifier

    def notify_new_order(self, client_name: str, special: bool = False) -> None:
        msg = 'Pedido especial recebido!' if special else 'Pedido recebido!'
        self.email_notifier.send(client_name, msg)

    def notify_status_change(self, order: Order, new_status: str) -> None:
        name = order.customer.name
        if new_status == 'aprovado':
            self.email_notifier.send(name, 'Pedido aprovado!')
            self.sms_notifier.send(name, 'Pedido aprovado!')
        elif new_status == 'enviado':
            self.email_notifier.send(name, 'Pedido enviado!')
        elif new_status == 'entregue':
            self.email_notifier.send(name, 'Pedido entregue!')

        points = int(order.total * (2 if order.customer.client_type == 'vip' else 1))
        print(f"Cliente {'VIP ' if order.customer.client_type == 'vip' else ''}ganhou {points} pontos!")
