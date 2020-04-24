import pytest
from datetime import date

from model import Batch, OrderLine


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch('batch-001', sku, batch_qty, eta=date.today()),
        OrderLine('order-123', sku, line_qty)
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    quantity_batch = 20
    quantity_order = 2
    batch, order = make_batch_and_line('table', quantity_batch, quantity_order)
    batch.allocate(order)
    assert batch.available_quantity == quantity_batch - quantity_order


def test_can_allocate_if_available_greater_than_required():
    batch, order = make_batch_and_line('table', 20, 2)
    assert batch.can_allocate(order)


def test_cannot_allocate_if_available_smaller_than_required():
    batch, order = make_batch_and_line('table', 2, 20)
    assert batch.can_allocate(order) is False


def test_can_allocate_if_available_equal_to_required():
    batch, order = make_batch_and_line('table', 2, 2)
    assert batch.can_allocate(order)

def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch('batch-001', 'UNCOMFORTABLE-CHAIR', 100, eta=None)
    different_sku_line = OrderLine('order-123', 'EXPENSIVE-TOASTER', 10)
    assert batch.can_allocate(different_sku_line) is False

def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line('DECORATIVE-TRINKET', 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20

def test_allocation_is_idempotent():
    batch, line = make_batch_and_line('table', 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18

