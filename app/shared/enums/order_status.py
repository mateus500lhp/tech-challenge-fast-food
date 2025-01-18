from enum import Enum as PyEnum
class OrderStatus(PyEnum):
    RECEIVED = "Recebido"
    IN_PROGRESS = "Em Preparação"
    READY = "Pronto"
    COMPLETED = "Finalizado"