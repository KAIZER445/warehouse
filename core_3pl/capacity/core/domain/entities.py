from datetime import datetime, timezone

class Capacity:
    def __init__(self, id, updated_at, total_capacity, current_allocated_space):
        self.id = id
        self.updated_at = updated_at
        self.total_capacity = total_capacity
        self.current_allocated_space = current_allocated_space

    def update_total_capacity(self, amount: int):
        if self.current_allocated_space > amount:
            raise ValueError("cannot change the total capacity as the current allocated space is more")
        self.current_allocated_space = amount

    def update_allocated_space(self, amount: int, operation: str):
        if operation == "ADDITION":
            self._allocate(amount)
        elif operation == "SUBTRACTION":
            self._release(amount)
        else:
            raise ValueError("only ADDITION or SUBTRACTION is allowed")
        self.updated_at = datetime.now(timezone.utc)

    def _allocate(self, amount: int):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if self.current_allocated_space + amount > self.total_capacity:
            raise ValueError("exceeds total capacity")
        self.current_allocated_space += amount

    def _release(self, amount: int):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if self.current_allocated_space - amount < 0:
            raise ValueError("cannot release more than allocated")
        self.current_allocated_space -= amount
