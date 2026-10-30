from abc import ABC, abstractmethod
from .book import Book
from .dto import QuoteResult


class LeaseServicePort(ABC):
    @abstractmethod
    def create_quote(self, tenant_id, books: list[Book]) -> QuoteResult: ...

    @abstractmethod
    def activate_lease(self, lease_id, tenant_id, selected_space, term_months, start_date): ...
