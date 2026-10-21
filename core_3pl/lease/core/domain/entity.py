from .enum import LeaseStatus, BoxSize
from math import floor


class Lease:
    def __init__(
        self,
        id,
        tenant_id,
        box_combination,
        total_boxes,
        minimum_required_space,
        total_volume,
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

    def greedy_box_allocation(books: list):
        # books_per_box = books_per_box(books)
        books_per_box = {
            "b1": {"SMALL": 6, "MEDIUM": 40, "LARGE": 117},
            "b2": {"SMALL": 0, "MEDIUM": 7,  "LARGE": 20},
        }

        for book in books:
            quantity = book.quanity
            box_combo = []
            for box in BoxSize:
                capacity_per_box = books_per_box[book.id][box.name]
                if capacity_per_box == 0:
                    continue
                if quantity < capacity_per_box:
                    box_combo.append(box)
                    return
                elif quantity > capacity_per_box:
                    box_combo.append(box)
                    quantity = quantity - capacity_per_box
                    return



