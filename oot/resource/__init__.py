__author__ = 'tardis'
from oot.common.utils import import_class, import_module
from oslo_config import cfg
from json import JSONEncoder

opts = [
    cfg.StrOpt('db_driver',
               default='oot.db.fake')
]

CONF = cfg.CONF
CONF.register_opts(opts)


class BaseResource(JSONEncoder):
    def __init__(self):
        self.db = import_module(CONF.db_driver)

    def default(self, o):
        return o.__dict__

    def db_model_import(self, cls_str):
        return import_class('%s.model.%s' % (CONF.db_driver, cls_str))
