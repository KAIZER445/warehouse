# Book Storage Lease: Flow Summary

## Design

- **Entities:** `USERS`, `TENANT`, `OPS`, `BOOK`, `SPACE_LEASE`, `WAREHOUSE_CAPACITY`
- **Relations:** Tenant 1-N Lease, Lease 1-N Book (`BOOK.space_lease_id`)
- **Boxes:** `BoxSize` enum (small, medium, large) with inside dimensions and max weight, no table
- **Packing:** greedy function on `lease.books` returns a box combination
- **Statuses:** `PENDING`, `ACTIVE`, `EXPIRED`, `ENDED`

## Endpoint 1: Quote

1. Tenant sends books (title, format, length, width, thickness, weight, quantity)
2. Validate input (positive numbers, non-empty list)
3. In one transaction: create lease as `PENDING` and create its `BOOK` rows
4. Run greedy packing and set `box_combination`, `total_boxes`, `minimum_required_space`, `total_volume`, `total_weight`
5. Return `lease_id`, `status`, `minimum_required_space`, `box_combination`
6. `current_allocated_space` is **not** changed

## Endpoint 2: Activate

1. Tenant sends `lease_id`, `selected_space`, `term_months`
2. Check lease belongs to tenant and is `PENDING`
3. Check `selected_space >= minimum_required_space`
4. Check `selected_space <= total_capacity - current_allocated_space` and `term_months` is allowed
5. Any failure: return error, lease stays `PENDING`
6. All pass, in one transaction: set `ACTIVE`, set `start_date` and `end_date`, add `selected_space` to `current_allocated_space`

## Later events

- **Pending lease too old:** mark `EXPIRED`, subtract nothing
- **Active lease ends or is cancelled:** mark `ENDED`, subtract `selected_space`

## Logic mistakes

None in the flow itself. These must be handled in the implementation:

1. `selected_space`, `term_months`, `start_date`, `end_date` must be nullable (lease is created before they are known)
2. Use one unit for minimum space, selected space and capacity
3. A book too big for the large box must raise a clear error, not be skipped
4. Endpoint 2 must check tenant ownership and `PENDING` status
5. Activation (status + capacity update) must be a single transaction

## Can wait

- `CANCELLED` status
- Choices fields for `status` and `format_type`
- Expiry job for old pending leases
- Packing margin as a constant in the packing code