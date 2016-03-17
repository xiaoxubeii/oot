__author__ = 'tardis'
from oot.resource import BaseResource
from oot.common import utils


class Cluster(BaseResource):
    def __init__(self):
        super(Cluster, self).__init__()
        self.cluster_model = self.db_model_import('ClusterModel')

    def create(self, m):
        self.db.create(self.cluster_model(**m))

    def get(self, id):
        return self._service_model(self.db.get(self.cluster_model, id))

    def list(self, **kwargs):
        return self._service_model(self.db.list(self.cluster_model, **kwargs))

    def delete(self, id):
        self.db.delete(self.cluster_model, id)

    def update(self, m):
        self.db.update(self.cluster_model, m)

    def _service_model(self, db_model):
        def _to(model):
            return utils.cp_dict(model.__dict__,
                                 ['id', 'name', 'conf'])

        if not db_model:
            return

        return [_to(m) for m in db_model] if isinstance(db_model, list) else _to(db_model)
