from abc import ABC, abstractmethod
from .book import Book
from .dto import QuoteResult


class LeaseServicePort(ABC):
    @abstractmethod
    def create_quote(self, tenant_id, books: list[Book]) -> QuoteResult: ...
