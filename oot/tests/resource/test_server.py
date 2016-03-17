__author__ = 'tardis'
import unittest
import mock
import random
from oot.resource.server import Server
from oot.baremetal.fake.driver import Manager
from oot.db.fake.model import ServerModel
import copy


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server()
        self.test_server_model = {
            'name': 'test',
            'host_name': 'test',
            'interfaces': {
                'eth0': {
                    'mac': self._random_mac(),
                    'ip': '192.168.1.2'
                }
            },
            'host_ip': '192.168.0.2',
            'service_host': '192.168.0.2',
            'tunnel_endpoint_ip': '192.168.1.2',
            'rabbit_hosts': '192.168.0.2'
        }

    @mock.patch.object(Manager, 'init_server')
    @mock.patch('oot.db.fake.create')
    def test_init_server(self, mock_db_create, mock_init_server):
        new_server = {'name': 'test'}
        init_server_param = copy.deepcopy(new_server)
        self.server.init(new_server)
        init_server_param.update({'profile': 'centos7-openstack'})
        mock_init_server.assert_called_once_with(init_server_param)

        db_create_param = ServerModel(**init_server_param)
        mock_db_create.assert_called_once_with(db_create_param)

    @mock.patch.object(Manager, 'register_server')
    @mock.patch('oot.db.fake.update')
    def test_register_server(self, mock_db_update, mock_register_server):
        self.server.update(self._get_def_conf())

        self.server.register(copy.deepcopy(self.test_server_model))
        mock_register_server.assert_called_once_with(self.test_server_model)

        mock_db_update.assert_called_once_with(ServerModel(**self.test_server_model))

    def test_server_model(self):
        model = None
        return_value = self.server._server_model(model)
        self.assertIsNone(return_value)

        model = self.test_server_model
        model.update({
            'id': 'test',
            'disk': 'test',
            'cpu': 'test',
            'memory': 'test',
            'ipmi': 'test',
            'cluster': '123',
            'cluster_id': '123',
            'conf': '123'
        })

        db_server_model = mock.create_autospec(ServerModel)
        db_server_model.__dict__ = model

        keys = set(['id', 'name', 'host_name', 'interfaces', 'disk', 'cpu', 'memory', 'ipmi', 'cluster', 'conf',
                    'cluster_id'])

        def _valid_rv(value):
            self.assertIsInstance(value, dict)
            self.assertTrue(set(keys) == set(value.keys()))

        return_value = self.server._server_model(db_server_model)
        _valid_rv(return_value)

        return_value = self.server._server_model([db_server_model, db_server_model])
        self.assertIsInstance(return_value, list)
        for l in return_value:
            _valid_rv(l)

    @mock.patch('oot.db.fake.list')
    def test_exist_server(self, mock_list):
        mock_list.return_value = None
        server_name = 'test'
        return_value = self.server._exist_server(server_name)
        mock_list.assert_called_once_with(ServerModel, name=server_name)
        self.assertFalse(return_value)

        mock_list.return_value = [{'test': 'test'}]
        self.assertTrue(self.server._exist_server('test'))

    def _random_mac(self):
        mac = [0x00, 0x16, 0x3e,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff)]
        return ':'.join(map(lambda x: "%02x" % x, mac))

    def _get_def_conf(self):
        return {
            'stack_user': 'stack', 'service_password': 'openstack', 'mysql_password': 'openstack',
            'service_token': 'openstack', 'dest': '/opt/openstack',
            'neutron_ml2_tenant_network_type': 'vxlan', 'ovs_enable_tunneling': 'true'
        }
