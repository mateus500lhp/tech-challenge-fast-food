from datetime import date
from app.core.entities.order import Order
from app.core.entities.item import OrderItem
from app.core.ports.coupon_repository_port import CouponRepositoryPort
from app.core.ports.order_repository_port import OrderRepositoryPort
from app.core.ports.products_repository_port import ProductRepositoryPort
from app.core.schemas.order_schemas import OrderIn
from app.shared.enums.order_status import OrderStatus

class CreateOrderService:
    def __init__(
        self,
        order_repository: OrderRepositoryPort,
        product_repository: ProductRepositoryPort,
        coupon_repository: CouponRepositoryPort,
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.coupon_repository = coupon_repository

    def execute(self, order_in: OrderIn, client_id: int) -> Order:
        """Cria um pedido a partir dos dados do `OrderIn`."""
        order = Order(
            client_id=client_id,
            coupon_hash=order_in.coupon_hash,
            status=OrderStatus.RECEIVED,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                )
                for item in order_in.items
            ],
        )

        # Validações, cálculos e criação do pedido no repositório
        created_order = self._process_order(order)
        return  created_order

    def _process_order(self, order: Order) -> Order:
        """Processa todas as validações, cálculos e a criação do pedido."""
        existing_coupon = None
        if order.coupon_hash:
            existing_coupon = self._validate_coupon(order)
        self._calculate_amount(order)

        # Em seguida, valida o estoque e atualiza a quantidade disponível
        self._validate_stock(order)

        # Aplica desconto, se houver cupom válido
        self._apply_discount(order, existing_coupon)

        created_order = self.order_repository.create(order)

        # Atualiza os nomes dos itens no pedido retornado
        for item in created_order.items:
            product = self.product_repository.find_by_id(item.product_id)
            item.name = product.name

        return created_order

    def _validate_coupon(self, order: Order):
        """Valida se o cupom é válido."""
        coupon = self.coupon_repository.find_by_hash(order.coupon_hash)
        if order.client_id is None:
            raise ValueError(f"Para utilizar um cupom, é necessário que o cliente esteja autenticado"
                             f" e devidamente identificado.")
        if not coupon:
            raise ValueError("Cupom não encontrado.")
        if not coupon.active:
            raise ValueError("O cupom informado não está ativo.")
        if coupon.expires_at and coupon.expires_at < date.today():
            raise ValueError("O cupom informado já expirou.")
        return coupon

    def _calculate_amount(self, order: Order):
        """Calcula o valor total do pedido e atualiza os preços dos itens."""
        total = 0
        for item in order.items:
            if item.quantity <= 0:
                raise ValueError("A quantidade do item deve ser maior que zero.")
            product = self.product_repository.find_by_id(item.product_id)
            if not product:
                raise ValueError(f"Produto com ID {item.product_id} não encontrado.")
            # Calcula o preço do item e atualiza o nome
            item.price = product.price * item.quantity
            item.name = product.name
            total += item.price
        order.amount = total

    def _validate_stock(self, order: Order):
        """Verifica se há estoque suficiente para cada item e atualiza o estoque."""
        for item in order.items:
            product = self.product_repository.find_by_id(item.product_id)
            if not product:
                raise ValueError(f"Produto com ID {item.product_id} não encontrado.")
            if product.quantity_available < item.quantity:
                raise ValueError(f"Estoque insuficiente para o produto {product.name}.")

            # Reduz o estoque do produto
            product.quantity_available -= item.quantity
            self.product_repository.update(product)

    def _apply_discount(self, order: Order, coupon):
        """Aplica o desconto do cupom ao valor total do pedido, se aplicável."""
        if coupon:
            discount = (order.amount * coupon.discount_percentage) / 100
            discount = min(discount, coupon.max_discount)
            order.amount -= discount
