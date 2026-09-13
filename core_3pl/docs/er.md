# Entity Relationship Diagram

```mermaid
erDiagram
    USERS ||--o| TENANT : "profile of"
    USERS ||--o| OPS : "profile of"
    TENANT ||--o{ SPACE_LEASE : holds
    TENANT ||--o{ INVENTORY_LINE : owns
    SPACE_LEASE ||--o{ INVENTORY_LINE : contains
    BOOK ||--o{ INVENTORY_LINE : "used by"
 
    USERS {
        uuid id PK
        string email
        string password_hash
        string role
        datetime created_at
    }
 
    TENANT {
        uuid id PK
        uuid user_id FK
        string company_name
        string contact_name
        datetime created_at
    }
 
    OPS {
        uuid id PK
        uuid user_id FK
        string full_name
        string department
        string permission_level
        datetime created_at
    }
 
    BOOK {
        uuid id PK
        string title
        string author
        string description
        string format_type
        decimal unit_weight
        decimal unit_volume
    }
 
    SPACE_LEASE {
        uuid id PK
        uuid tenant_id FK
        decimal selected_space
        decimal minimum_required_space
        decimal total_volume
        decimal total_weight
        int term_months
        string status
        date start_date
        date end_date
        datetime created_at
    }
 
    INVENTORY_LINE {
        uuid id PK
        uuid space_lease_id FK
        uuid tenant_id FK
        uuid book_id FK
        int quantity
        decimal total_weight
        decimal total_volume
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
| `inventory` | `BOOK_FORMAT`, `INVENTORY_LINE` |
| `lease` | `SPACE_LEASE` |
| `capacity` | `WAREHOUSE_CAPACITY` |