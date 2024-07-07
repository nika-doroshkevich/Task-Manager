from enum import Enum


class UserRoles(Enum):
    EMPLOYEE = 'СОТРУДНИК'
    CUSTOMER = 'ЗАКАЗЧИК'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
