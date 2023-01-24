from abc import ABC, abstractmethod


class DatabaseTransaction(ABC):
    @abstractmethod
    def begin_transaction(self) -> None:
        ...

    @abstractmethod
    def commit_transaction(self) -> None:
        ...

    @abstractmethod
    def rollback_transaction(self) -> None:
        ...


class DatabaseTransactionAsync(ABC):
    @abstractmethod
    async def begin_transaction(self) -> None:
        ...

    @abstractmethod
    async def commit_transaction(self) -> None:
        ...

    @abstractmethod
    async def rollback_transaction(self) -> None:
        ...
