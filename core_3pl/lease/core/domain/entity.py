from .enum import LeaseStatus, BoxSize
from math import floor
class Lease:
    def __init__( self, id, tenant_id, box_combination, total_boxes, minimum_required_space, total_volume, status=LeaseStatus.PENDING, selected_space=None, term_months=None, start_date=None, end_date=None):
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
        for box in BoxSize:
            results[box.name] = {
                book.id: floor(box.value.length / book.length)
                         * floor(box.value.width / book.width)
                         * floor(box.value.height / book.thickness)
                for book in books
            }
        return results
    
