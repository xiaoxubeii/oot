# encoding: utf-8
from dalek.api.openstack import wsgi
from oot.resource import server


class Controller(wsgi.Controller):
    def __init__(self, **kwargs):
        self.server = server.Server()
        super(Controller, self).__init__(**kwargs)

    def register(self, req, body):
        def_conf = self._get_def_conf()
        body = def_conf.update(body)
        self.server.register(body)

    # TODO oft
    def _get_def_conf(self):
        return {
            'stack_user': 'stack', 'service_password': 'openstack', 'mysql_password': 'openstack',
            'service_token': 'openstack', 'dest': '/opt/openstack',
            'neutron_ml2_tenant_network_type': 'vxlan', 'ovs_enable_tunneling': 'true'
        }


def create_resource():
    return wsgi.Resource(Controller())
