# Books 3PL — Space Leasing System

## About the Project

This is a Third-Party Logistics (3PL) platform focused exclusively on **book storage**. Tenants — publishers, resellers, independent bookstores, or anyone needing to store book inventory — come to the platform to lease warehouse space for their books.

Unlike a general-purpose 3PL that handles arbitrary products (apparel, electronics, mixed SKUs), narrowing the scope to books simplifies the domain significantly:

- Book formats (Hardcover, Paperback, Mass Market Paperback, etc.) have fairly predictable dimensions and weight, which makes space calculation more reliable than with arbitrary product categories.
- The business model is deliberately kept simple and self-service: **no manual approval step**. A tenant declares their inventory, the system calculates how much space they need, they choose a space size and a fixed rental term, pay upfront, and they're active — no human in the loop.
- Every space lease is a **fully independent entity**. A tenant may hold multiple leases over time, but each one is validated, priced, and lifecycled entirely on its own, with no shared state or relationship to any other lease — even ones held by the same tenant. This keeps the core domain object simple and avoids cross-entity consistency problems.
- Leasing is fixed-term only (1, 3, 6, or 12 months), paid upfront, with no refunds and no renewals. When a term ends, the space is released outright — a tenant who wants to continue must submit a brand new request.

This document lays out the full process flow, including every validation rule, from tenant registration through to lease expiry or cancellation. This is the backend business logic only — no UI, physical warehouse operations, or payment gateway integration details are covered here.

---

## Full Process Flow (with Validations)

### Step 1: Tenant Registration
- Tenant creates an account (no approval needed to register)

### Step 2: Inventory Declaration
- Tenant enters book inventory:
  - Title
  - Format (Hardcover / Paperback / Mass Market Paperback, etc.)
  - Quantity per title/format
- **Validation 2a:** Required fields must be present for every entry (title, format, quantity)
- **Validation 2b:** Quantities must be positive integers

### Step 3: Space Calculation
- System calculates:
  - `total_volume` and `total_weight` from quantity × unit dimensions/weight per format
  - `minimum_required_space` derived from the above

### Step 4: Space Selection
- Tenant selects a space size
- **Validation 4a:** `selected_space >= minimum_required_space`
  - Reject if below: *"Selected space is below the minimum required for your declared inventory."*
- **Validation 4b:** `selected_space <= 2 × minimum_required_space`
  - Reject if above: *"Requested space significantly exceeds your declared inventory. Please review your quantities."*

### Step 5: Term Selection
- Tenant selects a fixed term: 1, 3, 6, or 12 months
- **Validation 5a:** Term must be one of the allowed fixed values (no custom durations)

### Step 6: Global Capacity Check
- System checks: `current_allocated_space + selected_space <= global_capacity`
- **Validation 6a:** Reject if it doesn't fit: *"We're currently at capacity and can't accept new space requests. Please try again later."*

### Step 7: Submission Lock
- Once the request passes all validations above and is submitted, it becomes **immutable** — no further edits to inventory, space size, or term

### Step 8: Payment
- Tenant pays the full amount upfront for the selected space + term
- **Validation 8a:** Payment must succeed before any allocation occurs — no partial or pending allocations exist in the system

### Step 9: Space Allocation
- On successful payment:
  - Random `space_id` generated
  - `SpaceLease` entity created and marked **Active**
  - `current_allocated_space` incremented globally
- Tenant is now fully set up — no approval step, no further action needed

### Step 10: Lease Lifecycle — Expiry
- When the term ends:
  - `SpaceLease` is automatically deactivated/released
  - `space_id` retired
  - `current_allocated_space` decremented globally
  - **No renewal path** — tenant must submit a brand new request (back to Step 2) if they want to continue

### Step 11: Lease Lifecycle — Cancellation
- Tenant can cancel anytime before term ends
- On cancellation:
  - `SpaceLease` immediately deactivated/released
  - `space_id` retired
  - `current_allocated_space` decremented globally
  - **No refund**

### Cross-cutting Rule (applies throughout)
- Every `SpaceLease` is a fully independent entity — no relationship, aggregation, or shared state with any other lease, even under the same tenant
