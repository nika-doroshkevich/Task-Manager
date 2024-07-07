from enum import Enum


class TaskStatuses(Enum):
    PENDING = 'ОЖИДАЕТ_ИСПОЛНЕНИЯ'
    IN_PROGRESS = 'В_ПРОЦЕССЕ'
    DONE = 'ВЫПОЛНЕНА'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
