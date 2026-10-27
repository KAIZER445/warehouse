from .enum import LeaseStatus, BoxSize
from math import floor
from decimal import Decimal
from datetime import timedelta
from .book import Book

MAX_TERM_MONTHS = 36


class Lease:
    def __init__(
        self,
        tenant_id,
        box_combination,
        total_boxes,
        minimum_required_space,
        total_volume,
        total_weight,
        id=None,
        status=LeaseStatus.PENDING,
        selected_space=None,
        term_months=None,
        start_date=None,
        end_date=None,
    ):
        self.id = id
        self.tenant_id = tenant_id
        self.box_combination = box_combination
        self.total_boxes = total_boxes
        self.minimum_required_space = minimum_required_space
        self.total_volume = total_volume
        self.total_weight = total_weight
        self.status = status
        self.selected_space = selected_space
        self.term_months = term_months
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def create_quote(cls, tenant_id, books: list[Book]):
        box_combo = cls.greedy_box_allocation(books)
        return cls(
            tenant_id=tenant_id,
            box_combination=box_combo,
            total_boxes=sum(box_combo.values()),
            minimum_required_space=cls.calculate_minimum_required_space(box_combo),
            total_volume=cls.calculate_total_volume(books),
            total_weight=cls.calculate_total_weight(books),
        )

    def activate_lease(self, selected_space, term_months: int, start_date):
        # end_date logic needs to change, the timedelta approach is not accurate
        if self.status != LeaseStatus.PENDING:
            raise ValueError("Only pending lease can be activated")
        if (
            selected_space < self.minimum_required_space
            or selected_space > 3 * self.minimum_required_space
        ):
            raise ValueError(
                "Selected space must be between 1x and 3x the minimum required space"
            )
        if not (1 <= term_months <= MAX_TERM_MONTHS):
            raise ValueError(f"Term must be between 1 and {MAX_TERM_MONTHS} months")

        self.selected_space = selected_space
        self.term_months = term_months
        self.start_date = start_date
        self.end_date = start_date + timedelta(days=30 * term_months)
        self.status = LeaseStatus.ACTIVE

    @staticmethod
    def books_per_box(book: Book) -> dict:
        return {
            box.name: (
                floor(box.value.length / book.length)
                * floor(box.value.width / book.width)
                * floor(box.value.height / book.thickness)
            )
            for box in BoxSize
        }

    @staticmethod
    def greedy_box_allocation(books: list[Book]) -> dict:
        box_combo = {}
        for book in books:
            capacities = Lease.books_per_box(book)
            quantity = book.quantity
            for box in reversed(BoxSize):
                capacity_per_box = capacities[box.name]
                if capacity_per_box == 0:
                    continue
                if quantity // capacity_per_box != 0:
                    current_combo = quantity // capacity_per_box
                    box_combo[box.name] = box_combo.get(box.name, 0) + current_combo
                    quantity = quantity - (capacity_per_box * current_combo)
            if quantity > 0:
                for box in BoxSize:
                    if capacities[box.name] >= quantity:
                        box_combo[box.name] = box_combo.get(box.name, 0) + 1
                        break
                else:
                    raise ValueError(f"Book '{book.title}' does not fit in any box")
        return box_combo

    @staticmethod
    def calculate_minimum_required_space(box_combo: dict) -> Decimal:
        total = Decimal("0")
        for name, count in box_combo.items():
            total += BoxSize[name].value.volume * count
        return total

    @staticmethod
    def calculate_total_volume(books: list[Book]) -> Decimal:
        total = Decimal("0")
        for book in books:
            total += book.toal_volume
        return total

    @staticmethod
    def calculate_total_weight(books: list[Book]) -> Decimal:
        total = Decimal("0")
        for book in books:
            total += book.total_weight
        return total
