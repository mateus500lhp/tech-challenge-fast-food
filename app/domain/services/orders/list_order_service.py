from typing import List

from app.domain.entities.order import Order
from app.domain.ports.order_repository_port import OrderRepositoryPort


class ListOrdersService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.order_repository = order_repository

    def execute(self) -> List[Order]:
        return self.order_repository.find_all()


class ListOrdersByStatusService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.order_repository = order_repository

    def execute(self, status: str) -> List[Order]:
        return self.order_repository.find_by_status(status)

