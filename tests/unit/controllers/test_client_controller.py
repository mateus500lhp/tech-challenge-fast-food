import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.core.schemas.client_schemas import ClientIn, ClientUpdateIn
from main import app

client = TestClient(app)

# 🔹 POST /api/clients - sucesso
@patch("app.adapters.controllers.client_controller.CreateClientService")
def test_create_client_success(mock_service):
    mock_instance = mock_service.return_value

    mock_client = MagicMock()
    mock_client.id = 1
    mock_client.name = "John Doe"
    mock_client.email = "john@example.com"
    mock_client.cpf = "12345678900"
    mock_client.active = True

    mock_instance.execute.return_value = mock_client

    response = client.post("/api/clients", json={
        "cpf": "12345678900",
        "name": "John Doe",
        "email": "john@example.com",
        "password": "senhaSegura123"
    })

    assert response.status_code == 201
    assert response.json()["cpf"] == "123.456.789-00"

# 🔹 POST /api/clients - CPF duplicado
@patch("app.adapters.controllers.client_controller.CreateClientService")
def test_create_client_cpf_duplicado(mock_service):
    mock_instance = mock_service.return_value
    mock_instance.execute.side_effect = ValueError("CPF já cadastrado no sistema.")

    response = client.post("/api/clients", json={
        "cpf": "12345678900",
        "name": "John Doe",
        "email": "john@example.com",
        "password": "senhaSegura123"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "CPF já cadastrado no sistema."

# 🔹 GET /api/clients/cpf/{cpf} - identificar
@patch("app.adapters.controllers.client_controller.IdentifyClientService")
def test_get_client_by_cpf(mock_service):
    mock_instance = mock_service.return_value
    mock_instance.execute.return_value = "fake-jwt-token"

    response = client.get("/api/clients/cpf/12345678900")

    assert response.status_code == 200
    assert response.json()["jwt"] == "fake-jwt-token"

# 🔹 PUT /api/clients/{cpf} - atualizar cliente
@patch("app.adapters.controllers.client_controller.UpdateClientService")
def test_update_client_success(mock_service):
    mock_instance = mock_service.return_value

    mock_client = MagicMock()
    mock_client.id = 1
    mock_client.name = "John Atualizado"
    mock_client.email = "john@example.com"
    mock_client.cpf = "12345678900"
    mock_client.active = True

    mock_instance.execute.return_value = mock_client

    response = client.put("/api/clients/12345678900", json={
        "name": "John Atualizado"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "John Atualizado"
    assert response.json()["cpf"] == "123.456.789-00"

# 🔹 DELETE /api/clients/{cpf} - soft delete
@patch("app.adapters.controllers.client_controller.UpdateClientService")
def test_delete_client_success(mock_service):
    mock_instance = mock_service.return_value
    mock_instance.execute.return_value = None  # não retorna nada na exclusão

    response = client.delete("/api/clients/12345678900")

    assert response.status_code == 204
    assert response.content == b""
