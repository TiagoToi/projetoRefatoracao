from dataclasses import dataclass

@dataclass
class Customer:
    name: str            # ex.: 'João Silva'
    client_type: str     # 'normal' | 'vip'
