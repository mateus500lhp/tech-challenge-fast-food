from typing import List, Optional

from app.core.entities.order import Order
from app.core.ports.order_repository_port import OrderRepositoryPort


class ListOrdersService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.order_repository = order_repository

    def execute(self) -> List[Order]:
        return self.order_repository.find_all()

class GetOrderByIdService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.order_repository = order_repository

    def execute(self, order_id: int) -> Optional[Order]:
        return self.order_repository.find_by_id(order_id)

class ListOrdersByStatusService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.order_repository = order_repository

    def execute(self, status: str) -> List[Order]:
        return self.order_repository.find_by_status(status)

class ListOrdersByClientService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.order_repository = order_repository

    def execute(self, client_id: int) -> List[Order]:
        return self.order_repository.find_by_client(client_id)
