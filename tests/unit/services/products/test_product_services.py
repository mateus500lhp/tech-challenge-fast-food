import pytest
from unittest.mock import MagicMock
from app.domain.entities.product import Product
from app.domain.services.products.create_product_service import CreateProductService
from app.domain.services.products.update_product_service import UpdateProductService
from app.domain.services.products.delete_product_service import DeleteProductService
from app.domain.services.products.list_products_service import ListProductsService, ListProductsByCategoryService
from app.domain.ports.products_repository_port import ProductRepositoryPort


@pytest.fixture
def mock_repository():
    """
    Retorna um mock do ProductRepositoryPort,
    para ser injetado nos services.
    """
    return MagicMock(spec=ProductRepositoryPort)


# ----------------------------------------------------------------------------
# CREATE PRODUCT SERVICE
# ----------------------------------------------------------------------------

def test_create_product_service_success(mock_repository):
    service = CreateProductService(mock_repository)
    input_product = Product(
        name="Produto Teste",
        description="Descrição Teste",
        price=10.0,
        category="CategoriaTeste",
        quantity_available=5
    )

    # Configura o mock para retornar o mesmo produto (com ID, simulando DB)
    output_product = Product(
        id=1,
        name="Produto Teste",
        description="Descrição Teste",
        price=10.0,
        category="CategoriaTeste",
        quantity_available=5
    )
    mock_repository.create.return_value = output_product

    result = service.execute(input_product)

    # Verifica se o repository.create foi chamado
    mock_repository.create.assert_called_once_with(input_product)
    # Verifica se retornou o produto com ID
    assert result.id == 1
    assert result.name == "Produto Teste"


def test_create_product_service_negative_price(mock_repository):
    service = CreateProductService(mock_repository)
    input_product = Product(
        name="Produto inválido",
        description="Teste",
        price=-5.0,
        category="CategoriaTeste",
        quantity_available=1
    )

    # Esperamos que lance ValueError
    with pytest.raises(ValueError) as exc:
        service.execute(input_product)

    assert "Price cannot be negative." in str(exc.value)
    # Verifica se o repository.create NÃO foi chamado
    mock_repository.create.assert_not_called()


# ----------------------------------------------------------------------------
# UPDATE PRODUCT SERVICE
# ----------------------------------------------------------------------------

def test_update_product_service_success(mock_repository):
    service = UpdateProductService(mock_repository)

    # Produto que existe no BD
    existing_product = Product(
        id=1,
        name="Produto Original",
        description="Desc",
        price=100.0,
        category="CatA",
        quantity_available=10
    )
    # Novo dado
    new_data = Product(
        name="Produto Editado",
        description="Desc Editada",
        price=200.0,
        category="CatB",
        quantity_available=20
    )

    mock_repository.find_by_id.return_value = existing_product
    # Simula que o repositório retorna o produto atualizado
    updated_product = Product(
        id=1,
        name="Produto Editado",
        description="Desc Editada",
        price=200.0,
        category="CatB",
        quantity_available=20
    )
    mock_repository.update.return_value = updated_product

    result = service.execute(product_id=1, new_data=new_data)

    # Verifica se find_by_id foi chamado com 1
    mock_repository.find_by_id.assert_called_once_with(1)
    # Verifica se update foi chamado com o produto "existing_product" (já modificado)
    mock_repository.update.assert_called_once()
    assert result.id == 1
    assert result.name == "Produto Editado"
    assert result.price == 200.0


def test_update_product_service_not_found(mock_repository):
    service = UpdateProductService(mock_repository)
    # Simula que o produto não existe
    mock_repository.find_by_id.return_value = None

    new_data = Product(
        name="Novo nome",
        description="Nova desc",
        price=300.0,
        category="CatC",
        quantity_available=5
    )
    with pytest.raises(ValueError) as exc:
        service.execute(product_id=99, new_data=new_data)

    assert "Product not found" in str(exc.value)
    # update não deve ter sido chamado
    mock_repository.update.assert_not_called()


def test_update_product_service_negative_price(mock_repository):
    service = UpdateProductService(mock_repository)
    existing_product = Product(
        id=1,
        name="Produto Original",
        description="Desc",
        price=100.0,
        category="CatA",
        quantity_available=10
    )

    # Simula que o produto existe
    mock_repository.find_by_id.return_value = existing_product

    # Tenta atualizar com preço negativo
    new_data = Product(
        name="Tentativa de update inválida",
        description="Desc",
        price=-10.0,  # Negativo
        category="CatA",
        quantity_available=10
    )

    with pytest.raises(ValueError) as exc:
        service.execute(product_id=1, new_data=new_data)

    assert "Price cannot be negative." in str(exc.value)
    mock_repository.update.assert_not_called()


# ----------------------------------------------------------------------------
# DELETE PRODUCT SERVICE
# ----------------------------------------------------------------------------

def test_delete_product_service_success(mock_repository):
    service = DeleteProductService(mock_repository)

    # Produto que existe
    existing_product = Product(
        id=1,
        name="Produto A",
        description="Desc",
        price=10.0,
        category="CatA",
        quantity_available=1
    )
    mock_repository.find_by_id.return_value = existing_product

    service.execute(product_id=1)

    mock_repository.find_by_id.assert_called_once_with(1)
    mock_repository.delete.assert_called_once_with(1)


def test_delete_product_service_not_found(mock_repository):
    service = DeleteProductService(mock_repository)
    # Simula que não encontrou
    mock_repository.find_by_id.return_value = None

    with pytest.raises(ValueError) as exc:
        service.execute(99)

    assert "Product not found" in str(exc.value)
    mock_repository.delete.assert_not_called()


# ----------------------------------------------------------------------------
# LIST PRODUCTS SERVICE
# ----------------------------------------------------------------------------

def test_list_products_service_success(mock_repository):
    service = ListProductsService(mock_repository)

    mock_repository.find_all.return_value = [
        Product(id=1, name="P1", description="", price=10.0, category="Cat1", quantity_available=5),
        Product(id=2, name="P2", description="", price=20.0, category="Cat2", quantity_available=10),
    ]

    result = service.execute()

    mock_repository.find_all.assert_called_once()
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


# ----------------------------------------------------------------------------
# LIST PRODUCTS BY CATEGORY SERVICE
# ----------------------------------------------------------------------------

def test_list_products_by_category_service_success(mock_repository):
    service = ListProductsByCategoryService(mock_repository)

    mock_repository.find_by_category.return_value = [
        Product(id=1, name="P1", description="", price=10.0, category="CatX", quantity_available=5),
        Product(id=2, name="P2", description="", price=20.0, category="CatX", quantity_available=10),
    ]

    result = service.execute("CatX")

    mock_repository.find_by_category.assert_called_once_with("CatX")
    assert len(result) == 2
    assert all(p.category == "CatX" for p in result)
