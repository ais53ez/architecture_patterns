from dataclasses import dataclass
from typing import Optional
from datetime import date


class OutOfStock(Exception):
    pass


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: date):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # type: Set[OderLine]

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def can_allocate(self, line: OrderLine):
        return self.sku == line.sku and self.available_quantity >= line.qty
    
    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    
    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity


def allocate(line, batches):
    try:
        batch_picked = next(b for b in sorted(batches) if b.can_allocate(line))
        batch_picked.allocate(line)
        return batch_picked.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')

