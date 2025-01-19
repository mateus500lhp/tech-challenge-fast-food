import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.driven.models import ProductModel
from app.adapters.driven.repositories.product import ProductRepository
from app.domain.entities.product import Product
from app.shared.enums.categorys import CategoryEnum
from database import Base


# Fixture para configurar uma base de dados SQLite em memória para cada teste
@pytest.fixture(scope="function")
def session():
    # Cria uma engine SQLite em memória
    engine = create_engine("sqlite:///:memory:", echo=False)
    # Cria todas as tabelas definidas pelos modelos
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

# Fixture que fornece uma instância do repositório usando a sessão criada
@pytest.fixture
def repository(session):
    return ProductRepository(session)

### Testes para ProductRepository

def test_create_and_find_by_id(repository):
    # Criação de um produto
    product = Product(
        id=None,
        name="Test Product",
        description="A product for testing",
        price=9.99,
        category=CategoryEnum.LUNCH,
        quantity_available=5
    )
    created = repository.create(product)
    assert created.id is not None
    assert created.name == "Test Product"

    # Busca pelo ID do produto criado
    found = repository.find_by_id(created.id)
    assert found is not None
    assert found.id == created.id

def test_find_by_id_not_found(repository):
    # Deve retornar None para ID inexistente
    result = repository.find_by_id(9999)
    assert result is None

def test_find_all(repository, session):
    # Insere produtos ativos e inativos diretamente na sessão para teste
    product1 = ProductModel(
        name="Active Product",
        description="Desc1",
        price=10.0,
        category=CategoryEnum.LUNCH,
        quantity_available=5,
        active=True
    )
    product2 = ProductModel(
        name="Inactive Product",
        description="Desc2",
        price=20.0,
        category="Cat2",
        quantity_available=10,
        active=False
    )
    session.add_all([product1, product2])
    session.commit()

    # find_all deve retornar apenas produtos ativos
    results = repository.find_all()
    assert len(results) == 1
    assert results[0].name == "Active Product"

def test_find_by_category(repository, session):
    # Insere produtos para teste
    product1 = ProductModel(
        name="Prod A",
        description="Desc A",
        price=15.0,
        category=CategoryEnum.LUNCH,
        quantity_available=3,
        active=True
    )
    product2 = ProductModel(
        name="Prod B",
        description="Desc B",
        price=25.0,
        category=CategoryEnum.DRINK,
        quantity_available=8,
        active=True
    )
    session.add_all([product1, product2])
    session.commit()

    # Busca por categoria
    results = repository.find_by_category(CategoryEnum.LUNCH.value)
    # find_by_category deve retornar apenas produtos ativos e da categoria específica
    assert len(results) == 1
    assert results[0].name == "Prod A"

def test_update_product_success(repository):
    # Cria um produto para atualizar
    product = Product(
        id=None,
        name="Original Product",
        description="Original Desc",
        price=50.0,
        category=CategoryEnum.LUNCH,
        quantity_available=5
    )
    created = repository.create(product)

    # Atualiza o produto
    created.name = "Updated Product"
    updated = repository.update(created)

    assert updated.name == "Updated Product"

def test_update_product_not_found(repository):
    # Tenta atualizar produto inexistente
    non_existing_product = Product(
        id=999,
        name="Doesn't exist",
        description="No Desc",
        price=0.0,
        category="None",
        quantity_available=0
    )
    with pytest.raises(ValueError, match="Product not found"):
        repository.update(non_existing_product)

def test_delete_product_success(repository):
    # Cria um produto para deletar
    product = Product(
        id=None,
        name="To Delete",
        description="Desc",
        price=9.99,
        category=CategoryEnum.LUNCH,
        quantity_available=2
    )
    created = repository.create(product)

    # Verifica se está ativo antes da deleção
    product_model = repository.db_session.query(ProductModel).get(created.id)
    assert product_model.active == True

    # Deleta o produto (marca como inativo)
    repository.delete(created.id)

    # Verifica se o produto foi marcado como inativo
    product_model = repository.db_session.query(ProductModel).get(created.id)
    assert product_model.active == False

def test_delete_product_inactive(repository):
    # Insere um produto inativo para testar o erro
    product_model = ProductModel(
        name="Inactive",
        description="Desc",
        price=5.0,
        category=CategoryEnum.LUNCH,
        quantity_available=1,
        active=False
    )
    repository.db_session.add(product_model)
    repository.db_session.commit()

    with pytest.raises(ValueError, match="Product inactive"):
        repository.delete(product_model.id)
