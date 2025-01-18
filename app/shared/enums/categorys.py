from enum import Enum as PyEnum


class CategoryEnum(str, PyEnum):
    LUNCH = "Lanche"
    SIDES = "Acompanhamento"
    DRINK = "Bebida"
    DESSERT = "Sobremesa"