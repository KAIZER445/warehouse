# 3PL Core System: Audit & Bug Report

## 1. Overview
The codebase implements Hexagonal Architecture (Domain Entities, Ports, Services, Repositories, Adapters). The foundation for `users`, `capacity`, and the `lease` quote/activation flow is established.

---

## 2. Fixed Issues
- **App Registry (`config/settings.py`)**: Registered `lease` and `inventory` in `INSTALLED_APPS`. Django system check passes cleanly.
- **Allowed Hosts (`config/settings.py`)**: Updated `ALLOWED_HOSTS = ['*']` to enable API client and test execution.
- **Quote Creation Typo (`lease/core/domain/entity.py`)**: Fixed `toal_volume` typo to `total_volume` in `calculate_total_volume`.
- **Capacity Save Bug (`capacity/adapters/driven/mappers.py`)**: Fixed `id = id` (built-in function) to `id = row.id`, ensuring updates persist to the database.
- **Capacity Operation Case Mismatch (`capacity/core/domain/entities.py`)**: Normalized `operation` (`.upper()`), supporting both lowercase `"addition"` and uppercase `"ADDITION"`.
- **Port Shadowing (`lease/core/domain/ports.py`)**: Renamed port to `LeasePort` (aliasing `Lease`) to prevent shadowing the `Lease` domain entity.
- **Lease Activation 404 Handler (`lease/adapters/driving/views.py`)**: Added `LookupError` catch returning HTTP 404 instead of unhandled 500 when lease is not found.
- **Decimal Unit Consistency (`capacity/models.py`, `entities.py`, `serializers.py`, `enum.py`)**: Replaced integers with `DecimalField(max_digits=14, decimal_places=5)` across `Capacity` model, entity methods, and DRF serializer. Ensured `Dimensions.volume` returns `Decimal`.
- **Capacity Migration Reset & Schema Sync**: Cleaned up the divergent `capacity_warehouse` table and migrated to `capacity_capacity` matching model `Capacity`.
- **Tenant Deactivation Active Lease Guard (`users/adapters/driven/repositories/tenant.py`)**: Wired `count_active_leases` to query `LeaseModel` for `ACTIVE` status leases. Tenants with active leases now correctly raise `ValueError` and cannot be deactivated (returns HTTP 409).
- **Documentation Aligned (`docs/tenantFlow.md`)**: Updated docs to reflect the 3x space upper bound (`selected_space <= 3 * minimum_required_space`) and flexible term selection (1 to 36 months).
- **Migrations Applied**: Generated and applied initial migrations for `capacity`, `lease`, `inventory`, and `logs`.
- **Capacity Seeder Command (`capacity/management/commands/seed_capacity.py`)**: Implemented management command to initialize default warehouse capacity.
- **Automated Test Coverage**: Added test suites in `users/tests.py`, `capacity/tests.py`, and `lease/tests.py` verifying all 13 endpoint scenarios.

---

## 3. Remaining Tasks & Notes

### Critical / Functional
1. **Unconnected Capacity in Lease Activation**
   - *File:* `lease/core/application/services.py:33`
   - *Issue:* `# need to check for allocation space from capacity app` is not yet implemented. Lease activation currently does not verify global capacity availability or increment `current_allocated_space`.

### Deferred Business Rules
1. **Box Weight Limits**:
   - *Note:* Weight limits per box (`BoxSize`) and book total weight restrictions will be implemented in a future update.

### Missing Features & Hardening
1. **Concurrency Control**: No `select_for_update()` lock when checking and updating warehouse capacity during activation.
2. **Public Ops Registration**: Anyone can register with `role: "ops"` at `/user/register/` without admin permissions.
3. **Lease Lifecycle Endpoints**: Expiry background task (releasing space) and cancellation endpoint are unwritten.
