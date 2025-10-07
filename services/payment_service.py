from repositories.order_repository import IOrderRepository
from services.notification_service import INotificationService
from strategies.payment_strategy import IPaymentMethod, CardPayment, PixPayment, BoletoPayment


class PaymentService:
    def __init__(self, repository: IOrderRepository, notifier: INotificationService):
        self.repository = repository
        self.notifier = notifier
        self.methods: dict[str, IPaymentMethod] = {
            'cartao': CardPayment(),
            'pix': PixPayment(),
            'boleto': BoletoPayment()
        }

    def process_payment(self, order_id: int, method: str, amount: float) -> bool:
        order = self.repository.get_order(order_id)
        if not order:
            raise ValueError(f'Pedido {order_id} não encontrado.')
        if amount < order.total:
            raise ValueError('Valor insuficiente!')

        method_key = method.lower()
        if method_key not in self.methods:
            raise ValueError('Método de pagamento inválido!')

        status_result = self.methods[method_key].pay(order)

        if status_result == 'aprovado':
            self.repository.update_status(order_id, 'aprovado')
            order.status = 'aprovado'
            self.notifier.notify_status_change(order, 'aprovado')

        # boleto permanece 'pendente'
        return True
