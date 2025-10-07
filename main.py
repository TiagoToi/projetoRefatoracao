import sqlite3
from models.order import OrderItem
from repositories.order_repository import SQLiteOrderRepository
from services.order_service import OrderService, SpecialOrderService
from services.payment_service import PaymentService
from services.notification_service import EmailNotifier, SMSNotifier, NotificationService
from strategies.discount_strategy import StandardPricingStrategy
from services.order_service import BasicStockValidator


def main():
    conn = sqlite3.connect('loja.db')
    repo = SQLiteOrderRepository(conn)

    stock_validator = BasicStockValidator()
    email_notifier = EmailNotifier()
    sms_notifier = SMSNotifier()
    notifier_service = NotificationService(email_notifier, sms_notifier)

    # Estratégia padrão aplica VIP -5%
    order_service = OrderService(
        repository=repo,
        stock_validator=stock_validator,
        pricing_strategy=StandardPricingStrategy(),
        notifier=notifier_service
    )

    # Serviço especial: NÃO aplica VIP; apenas taxa +15%
    special_order_service = SpecialOrderService(
        repository=repo,
        stock_validator=stock_validator,
        notifier=notifier_service
    )

    payment_service = PaymentService(repo, notifier_service)

    # Pedido normal
    items1 = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'}
    ]
    if stock_validator.validate_items([OrderItem(name=i['nome'], price=i['p'],
                                                 quantity=i['q'], discount_type=i['tipo']) for i in items1]):
        id1 = order_service.add_order('João Silva', items1, 'normal')
        print(f'Pedido {id1} criado!')
        try:
            payment_service.process_payment(id1, 'cartao', 250)
        except ValueError as e:
            print(e)
        order_service.update_status(id1, 'enviado')
        order_service.update_status(id1, 'entregue')

    # Pedido VIP ESPECIAL (ignora VIP, aplica só +15%)
    items2 = [{'nome': 'produto3', 'p': 200, 'q': 1, 'tipo': 'desc20'}]
    if stock_validator.validate_items([OrderItem(name=i['nome'], price=i['p'],
                                                 quantity=i['q'], discount_type=i['tipo']) for i in items2]):
        id2 = special_order_service.add_order('Maria Santos', items2, 'vip')
        try:
            payment_service.process_payment(id2, 'pix', 160)
        except ValueError as e:
            print(e)

    order_service.generate_sales_report()
    print()
    order_service.generate_clients_report()
    repo.close()


if __name__ == '__main__':
    main()
