from abc import ABC, abstractmethod


class SyncDatabase(ABC):
    @abstractmethod
    def begin_transaction(self) -> None:
        pass

    @abstractmethod
    def commit_transaction(self) -> None:
        pass

    @abstractmethod
    def rollback_transaction(self) -> None:
        pass


class AsyncDatabase(ABC):
    @abstractmethod
    async def begin_transaction(self) -> None:
        pass

    @abstractmethod
    async def commit_transaction(self) -> None:
        pass

    @abstractmethod
    async def rollback_transaction(self) -> None:
        pass
