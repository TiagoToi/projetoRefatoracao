
from models.order import Order
from interfaces.ipayment_method import IPaymentMethod


class CardPayment(IPaymentMethod):
    def pay(self, order: Order) -> str:
        print('Processando pagamento com cartão...')
        return 'aprovado'


class PixPayment(IPaymentMethod):
    def pay(self, order: Order) -> str:
        print('Gerando QR Code PIX...')
        return 'aprovado'


class BoletoPayment(IPaymentMethod):
    def pay(self, order: Order) -> str:
        print('Gerando boleto...')
        return 'pendente'
