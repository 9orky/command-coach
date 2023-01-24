from dataclasses import dataclass

from command_coach.query import Query, QueryHandler


@dataclass(frozen=True)
class TestQuery(Query):
    property: str


class TestQueryHandler(QueryHandler):
    def handle(self, query: TestQuery) -> str:
        return query.property


@dataclass(frozen=True)
class TestQueryAsync(Query):
    property: str


class TestQueryAsyncHandler(QueryHandler):
    async def handle(self, query: TestQueryAsync) -> str:
        return query.property
