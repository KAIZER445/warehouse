class User:
    def __init__(self, id, email, role, is_active, last_login, created_at, updated_at):
        self.id = id
        self.email = email
        self.role = role
        self.is_active = is_active
        self.last_login = last_login
        self.created_at = created_at
        self.updated_at = updated_at
