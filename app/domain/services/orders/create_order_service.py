from datetime import date

from app.domain.entities.order import Order
from app.domain.ports.coupon_repository_port import CouponRepositoryPort
from app.domain.ports.order_repository_port import OrderRepositoryPort
from app.domain.ports.products_repository_port import ProductRepositoryPort


class CreateOrderService:
    def __init__(
        self,
        order_repository: OrderRepositoryPort,
        product_repository: ProductRepositoryPort,
        coupon_repository: CouponRepositoryPort
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.coupon_repository = coupon_repository

    def execute(self, order: Order) -> Order:
        amount = 0

        existing_coupon = None
        if order.coupon_hash:
            if order.client_id is None:
                raise ValueError(f"Para utilizar um cupom, é necessário que o cliente esteja autenticado"
                                 f" e devidamente identificado.")
            existing_coupon = self.coupon_repository.find_by_hash(order.coupon_hash)

            if not existing_coupon:
                raise ValueError("Cupom não encontrado.")

            if not existing_coupon.active:
                raise ValueError("O cupom informado não está ativo.")

            if existing_coupon.expires_at and existing_coupon.expires_at <  date.today():
                raise ValueError("O cupom informado já expirou.")



        for item in order.items:
            product = self.product_repository.find_by_id(item.product_id)

            if not product:
                raise ValueError(f"Product with ID {item.product_id} not found.")

            if product.quantity_available < item.quantity:
                raise ValueError(
                    f"Not enough stock for product {product.name}. "
                    f"Available: {product.quantity_available}, Requested: {item.quantity}"
                )

            # Calcula o preço do item baseado no banco
            item.price = product.price * item.quantity
            item.name = product.name
            amount += item.price

            # Atualiza o estoque do produto
            product.quantity_available -= item.quantity
            self.product_repository.update(product)

        # Define o valor total do pedido
        order.amount = amount

        if order.coupon_hash and existing_coupon:
            discount = (order.amount * existing_coupon.discount_percentage) / 100
            discount = min(discount, existing_coupon.max_discount)
            order.amount -= discount

        # Cria o pedido no repositório
        created_order = self.order_repository.create(order)

        # Atualiza os nomes dos itens no pedido retornado
        for item in created_order.items:
            product = self.product_repository.find_by_id(item.product_id)
            item.name = product.name  # Adiciona o nome do produto

        return created_order