from app.core.schemas.order_schemas import OrderOut, OrderItemOut
from app.core.entities.order import Order

class OrderPresenter:
    @staticmethod
    def present(order: Order) -> OrderOut:
        """
        Retorna um objeto `OrderOut` formatado para resposta da API.
        """
        return OrderOut(
            id=order.id,
            client_id=order.client_id,
            coupon_hash=order.coupon_hash,
            status=order.status,
            items=[
                OrderItemOut(
                    product_id=item.product_id,
                    name=item.name,
                    quantity=item.quantity,
                    price=item.price,
                )
                for item in order.items
            ],
            amount=order.amount,
        )

    @staticmethod
    def present_list(orders: list[Order]) -> list[OrderOut]:
        """
        Retorna uma lista de pedidos formatados.
        """
        return [OrderPresenter.present(order) for order in orders]
