import abc
import json
from typing import Any


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния."""

    @abc.abstractmethod
    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict[str, Any]:
        """Получить состояние из хранилища."""
        pass


class JsonFileStorage(BaseStorage):
    """
    Реализация хранилища, использующего локальный файл.
    Формат хранения: JSON
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        with open(self.file_path, 'w') as files:
            json.dump(state, files)

    def retrieve_state(self) -> dict[str, Any] | None:
        """Получить состояние из хранилища."""
        try:
            with open(self.file_path, 'r') as files:
                return json.load(files)
        except FileNotFoundError:
            return None


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        self.storage.save_state(state={key: value})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        if self.storage.retrieve_state() is None:
            return None
        return self.storage.retrieve_state().get(key)
