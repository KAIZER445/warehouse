from datetime import datetime, timezone
from decimal import Decimal

class Capacity:
    def __init__(self, id, updated_at, total_capacity: Decimal, current_allocated_space: Decimal):
        self.id = id
        self.updated_at = updated_at
        self.total_capacity = Decimal(str(total_capacity))
        self.current_allocated_space = Decimal(str(current_allocated_space))

    def update_total_capacity(self, amount: Decimal):
        amount = Decimal(str(amount))
        if self.current_allocated_space > amount:
            raise ValueError("cannot change the total capacity as the current allocated space is more")
        self.total_capacity = amount

    def update_allocated_space(self, amount: Decimal, operation: str):
        amount = Decimal(str(amount))
        normalized_op = str(operation).upper()
        if normalized_op == "ADDITION":
            self._allocate(amount)
        elif normalized_op == "SUBTRACTION":
            self._release(amount)
        else:
            raise ValueError("only ADDITION or SUBTRACTION is allowed")
        self.updated_at = datetime.now(timezone.utc)

    def _allocate(self, amount: Decimal):
        if amount <= Decimal("0"):
            raise ValueError("amount must be positive")
        if self.current_allocated_space + amount > self.total_capacity:
            raise ValueError("exceeds total capacity")
        self.current_allocated_space += amount

    def _release(self, amount: Decimal):
        if amount <= Decimal("0"):
            raise ValueError("amount must be positive")
        if self.current_allocated_space - amount < Decimal("0"):
            raise ValueError("cannot release more than allocated")
        self.current_allocated_space -= amount
