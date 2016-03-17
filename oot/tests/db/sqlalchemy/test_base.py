__author__ = 'tardis'
import unittest
import oot.db.sqlalchemy as db
import mock
from oot.db.sqlalchemy.model import ServerModel


class TestBase(unittest.TestCase):
    def test_create(self):
        server = {
            'name': 'test',
            'interfaces': {
                'eth0': {
                    'mac': '123',
                    'ip': '192.168.0.1'
                }
            }
        }
        db.create(ServerModel(**server))
