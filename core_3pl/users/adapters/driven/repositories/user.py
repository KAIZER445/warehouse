from users.core.domain.ports import UserPort
from users.models import User as UserModel

from ..mappers.user import to_entity


class UserRepository(UserPort):
    def create(self, email, password, role):
        row = UserModel.objects.create_user(email=email, password=password, role=role)
        return to_entity(row)

    def list_all(self):
        return [to_entity(row) for row in UserModel.objects.all()]
