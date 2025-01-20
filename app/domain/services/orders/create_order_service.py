from app.domain.entities.order import Order
from app.domain.ports.order_repository_port import OrderRepositoryPort
from app.domain.ports.products_repository_port import ProductRepositoryPort


class CreateOrderService:
    def __init__(self, order_repository: OrderRepositoryPort, product_repository: ProductRepositoryPort):
        self.order_repository = order_repository
        self.product_repository = product_repository

    def execute(self, order: Order) -> Order:
        amount = 0

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

        # Cria o pedido no repositório
        created_order = self.order_repository.create(order)

        # Atualiza os nomes dos itens no pedido retornado
        for item in created_order.items:
            product = self.product_repository.find_by_id(item.product_id)
            item.name = product.name  # Adiciona o nome do produto

        return created_order
