from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass
class QuoteResult:
    lease_id: UUID
    status: str
    minimum_required_space: Decimal
    box_combination: dict
