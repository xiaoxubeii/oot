__author__ = 'tardis'

from oslo_config import cfg
from oot.common.utils import import_class
from oot.resource import BaseResource, cluster
from oot.common import utils
import copy

opts = [
    cfg.StrOpt('baremetal_driver',
               default="oot.baremetal.fake.driver.Manager"),
    cfg.StrOpt('def_profile',
               default='centos7-openstack')
]

CONF = cfg.CONF
CONF.register_opts(opts)


class Server(BaseResource):
    def __init__(self):
        super(Server, self).__init__()
        manager_class = import_class(CONF.baremetal_driver)
        self.manager = manager_class()
        self.server_model = self.db_model_import('ServerModel')

    def init(self, m):
        if self._exist_server(m.get('name')):
            return

        init_server_model = {
            'name': m.get('name'),
            'profile': self._get_def_profile(),
            'mac_address': m.pop('master_mac')
        }
        self.manager.init_server(init_server_model)

        m.update({'profile': self._get_def_profile()})
        self.db.create(self.server_model(**m))

    def _exist_server(self, server_name):
        list = self.db.list(self.server_model, name=server_name)
        return bool(list)

    def register(self, m):
        db_model = copy.deepcopy(m)
        self.db.update(self.server_model, db_model)

        detail_server = self.get(m.get('id'))
        clu = cluster.Cluster()

        clu_model = clu.get(detail_server.get('cluster_id'))
        meta_conf = clu_model.get('conf')
        reg_server = copy.deepcopy(detail_server)
        conf = reg_server.get('conf', {})
        meta_conf.update(conf) if conf else meta_conf
        reg_server['conf'] = meta_conf

        self.manager.register_server(reg_server)

    def _get_def_profile(self):
        return CONF.def_profile

    def list(self, **kwargs):
        return self._server_model(self.db.list(self.server_model, **kwargs))

    def get(self, id):
        return self._server_model(self.db.get(self.server_model, id))

    def delete(self, id):
        self.db.delete(self.server_model, id)

    def update(self, m):
        self.db.update(self.server_model, m)

    def _server_model(self, db_model):
        def _to(model):
            return utils.cp_dict(model.__dict__,
                                 ['id', 'name', 'host_name', 'interfaces', 'disk', 'cpu', 'memory', 'ipmi', 'cluster',
                                  'conf', 'cluster_id'])

        if not db_model:
            return

        return [_to(m) for m in db_model] if isinstance(db_model, list) else _to(db_model)
