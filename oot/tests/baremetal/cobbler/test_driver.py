__author__ = 'tardis'
import unittest
from oot.baremetal.cobbler.driver import CobblerManager
import mock


class TestCobblerManager(unittest.TestCase):
    def setUp(self):
        self.manager = CobblerManager()

    def _is_same(self, m1, m2):
        for k, v in m1.items():
            self.assertEqual(v, m2[k])

    def test_init_server(self):
        m = {
            'name': 'test',
            'ipmi_address': '192.168.1.1',
            'ipmi_user': 'test',
            'ipmi_pass': 'test',
            'interfaces': {
                'eth0': {
                    'mac': 'ff:ff:ff:ff:ff:ff',
                    'ip': '192.168.1.1'
                }
            }
        }
        self.manager.init_server(m)

        new_m = self.manager.get_server(m.get('name'))
        self.assertIsNotNone(new_m)
        self._is_same(m, new_m)

    def test_register_server(self):
        m = {
            'name': 'test',
            'host_name': 'test',
            'interfaces': {
                'eth0': {
                    'mac': 'ff:ff:ff:ff:ff:ff',
                    'ip': '192.168.1.1'
                }
            }
        }
        self.manager.register_server(m)
        new_m = self.manager.get_server(m.get('name'))
        self.assertIsNotNone(new_m)
        self._is_same(m, new_m)
