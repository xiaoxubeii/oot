__author__ = 'tardis'
import unittest
from oot.resource import notify
import mock
from oot.msgapi.server import Server


class TestNotify(unittest.TestCase):
    def setUp(self):
        self.notify = notify.Notify()

    @mock.patch.object(Server, 'init')
    def test_create(self, mock_server_init):
        new_server = {'name': 'test'}
        self.notify.create({
            'source_id': '12345',
            'msg': {'pxe_boot': 'success'},
            'opt': {
                'server.init': (new_server,)
            }
        })

        mock_server_init.assert_called_once_with(new_server)
