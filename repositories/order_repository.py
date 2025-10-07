import sqlite3
import json
from typing import List, Optional

from models.order import Order
from models.order_item import OrderItem
from models.customer import Customer
from interfaces.iorder_repository import IOrderRepository




class SQLiteOrderRepository(IOrderRepository):
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS ped (
                id INTEGER PRIMARY KEY,
                cli TEXT,
                itens TEXT,
                tot REAL,
                st TEXT,
                dt TEXT,
                tp TEXT
            )'''
        )
        self.conn.commit()

    def create_order(self, order: Order) -> int:
        items_json = json.dumps([item.__dict__ for item in order.items])
        self.cursor.execute(
            'INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)',
            (order.customer.name, items_json, order.total, order.status, order.date, order.customer.client_type)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def _row_to_order(self, row) -> Order:
        items = [OrderItem(**item) for item in json.loads(row[2])]
        customer = Customer(name=row[1], client_type=row[6])  # cli, tp
        return Order(id=row[0], customer=customer, items=items,
                     total=row[3], status=row[4], date=row[5])

    def get_order(self, order_id: int) -> Optional[Order]:
        self.cursor.execute('SELECT * FROM ped WHERE id=?', (order_id,))
        row = self.cursor.fetchone()
        return self._row_to_order(row) if row else None

    def update_status(self, order_id: int, new_status: str) -> None:
        self.cursor.execute('UPDATE ped SET st=? WHERE id=?', (new_status, order_id))
        self.conn.commit()

    def get_all_orders(self) -> List[Order]:
        self.cursor.execute('SELECT * FROM ped')
        return [self._row_to_order(r) for r in self.cursor.fetchall()]

    def get_distinct_clients(self) -> List[tuple[str, str]]:
        self.cursor.execute('SELECT DISTINCT cli, tp FROM ped')
        return self.cursor.fetchall()

    def get_total_by_client(self, client_name: str) -> float:
        self.cursor.execute('SELECT SUM(tot) FROM ped WHERE cli=?', (client_name,))
        r = self.cursor.fetchone()
        return float(r[0]) if r and r[0] else 0.0

    def close(self) -> None:
        self.conn.close()
