from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Book:
    title: str
    author: str
    description: str
    format_type: str
    length: Decimal
    width: Decimal
    thickness: Decimal
    unit_weight: Decimal
    quantity: int

    @property
    def unit_volume(self) -> Decimal:
        return self.length * self.width * self.thickness

    @property
    def total_volume(self) -> Decimal:
        return self.unit_volume * self.quantity

    @property
    def total_weight(self) -> Decimal:
        return self.unit_weight * self.quantity