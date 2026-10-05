from users.core.domain.ports import OpsPort, OpsServicePort


class OpsService(OpsServicePort):
    def __init__(self, repo: OpsPort):
        self.repo = repo

    def list_all(self):
        return self.repo.list_all()
