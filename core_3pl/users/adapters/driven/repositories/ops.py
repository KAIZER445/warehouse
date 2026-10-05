from users.core.domain.ports import OpsPort
from users.models import Ops as OpsModel

from ..mappers.ops import to_entity


class OpsRepository(OpsPort):
    def create(self, user_id, full_name, department=None):
        kwargs = {"user_id": user_id, "full_name": full_name}
        if department is not None:
            kwargs["department"] = department
        row = OpsModel.objects.create(**kwargs)
        return to_entity(row)

    def list_all(self):
        return [to_entity(row) for row in OpsModel.objects.all()]
