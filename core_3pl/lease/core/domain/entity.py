from .enum import LeaseStatus, BoxSize
from math import floor
from decimal import Decimal
from datetime import timedelta

MAX_TERM_MONTHS = 36

class Lease:
    def __init__(
        self,
        tenant_id,
        box_combination,
        total_boxes,
        minimum_required_space,
        total_volume,
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
        self.status = status
        self.selected_space = selected_space
        self.term_months = term_months
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def create_quote(cls, tenant_id, books):
        box_combo = cls.greedy_box_allocation(books)
        return cls(
            tenant_id=tenant_id,
            box_combination=box_combo,
            total_boxes=sum(box_combo.values()),
            minimum_required_space=cls.calculate_minimum_required_space(box_combo),
            total_volume=cls.calculate_total_volume(books),
        )

    def activate_lease(self, selected_space, term_months: int, start_date):
        # logic needs to be changed for end date as time delta approach is not accurate 
        if self.status != LeaseStatus.PENDING:
            raise ValueError("only pending lease can be activated")
        if selected_space < self.minimum_required_space or selected_space > 3 * self.minimum_required_space:
            raise ValueError("Selected space cannot be less than the minimum required space or more than triple the minimum required space")

        if not (1 <= term_months <= MAX_TERM_MONTHS):
            raise ValueError(f"Term must be between 1 and {MAX_TERM_MONTHS} months")

        self.selected_space = selected_space
        self.term_months = term_months
        self.start_date = start_date
        self.end_date = start_date + timedelta(days= 30 * term_months)
        self.status = LeaseStatus.ACTIVE

    @staticmethod
    def books_per_box(books: list) -> dict:
        results = {}
        for book in books:
            results[book.id] = {}
            for box in BoxSize:
                results[book.id][box.name] = (
                    floor(box.value.length / book.length)
                    * floor(box.value.width / book.width)
                    * floor(box.value.height / book.thickness)
                )
        return results

    @staticmethod
    def greedy_box_allocation(books: list) -> dict:
        capacities = Lease.books_per_box(books)

        box_combo = {}
        for book in books:
            quantity = book.quantity
            for box in reversed(BoxSize):
                capacity_per_box = capacities[book.id][box.name]
                if capacity_per_box == 0:
                    continue
                if quantity // capacity_per_box != 0:
                    current_combo = quantity // capacity_per_box
                    box_combo[box.name] = box_combo.get(box.name, 0) + current_combo
                    quantity = quantity - (capacity_per_box * current_combo)
            if quantity > 0:
                for box in BoxSize:
                    if capacities[book.id][box.name] >= quantity:
                        box_combo[box.name] = box_combo.get(box.name, 0) + 1
                        break
                else:
                    raise ValueError(f"Book {book.id} does not fit in any box")
        return box_combo

    @staticmethod
    def calculate_minimum_required_space(box_combo: dict) -> Decimal:
        total = Decimal("0")
        for name, count in box_combo.items():
            total += BoxSize[name].value.volume * count
        return total

    @staticmethod
    def calculate_total_volume(books: list) -> Decimal:
        total = Decimal("0")
        for book in books:
            total += book.length * book.width * book.thickness * book.quantity
        return total