# Entity Relationship Diagram

```mermaid
erDiagram
    USERS ||--o| TENANT : "profile of"
    USERS ||--o| OPS : "profile of"
    TENANT ||--o{ SPACE_LEASE : holds
    SPACE_LEASE ||--o{ BOOK : contains

    USERS {
        uuid id PK
        string email
        string password_hash
        string role
        datetime created_at
        datetime last_login
    }

    TENANT {
        uuid id PK
        uuid user_id FK
        string company_name
        datetime created_at
    }

    OPS {
        uuid id PK
        uuid user_id FK
        string full_name
        string department
        datetime created_at
    }

    BOOK {
        uuid id PK
        uuid space_lease_id FK
        string title
        string author
        string description
        string format_type
        decimal length
        decimal width
        decimal thickness
        decimal unit_weight
        decimal unit_volume "derived: length x width x thickness"
        int quantity
        decimal total_weight "derived: unit_weight x quantity"
        decimal total_volume "derived: unit_volume x quantity"
    }

    SPACE_LEASE {
        uuid id PK
        uuid tenant_id FK
        json box_combination "e.g. LARGE:2, SMALL:1 (keys from BoxSize enum)"
        int total_boxes
        decimal selected_space
        decimal minimum_required_space "sum of volumes of boxes in box_combination"
        decimal total_volume "sum of book total_volume"
        decimal total_weight "sum of book total_weight"
        int term_months
        string status
        date start_date
        date end_date
        datetime created_at
    }

    WAREHOUSE_CAPACITY {
        uuid id PK
        decimal total_capacity
        decimal current_allocated_space
    }
```

## App ownership

| App | Tables |
|---|---|
| `users` | `USERS`, `TENANT`, `OPS` |
| `inventory` | `BOOK` |
| `lease` | `SPACE_LEASE` (also holds the `BoxSize` enum and the greedy packing function) |
| `capacity` | `WAREHOUSE_CAPACITY` |