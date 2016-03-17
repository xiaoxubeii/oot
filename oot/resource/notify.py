__author__ = 'tardis'
from oot.common import utils
from oot.resource import BaseResource


class Notify(BaseResource):
    def create(self, body):
        msg = body.get('msg')
        source_id = body.get('source_id')
        self._save_msg(source_id, msg)
        self._run_opt(source_id, msg.get('opt'))

    def _save_msg(self, src_id, msg):
        # TODO
        pass

    def _run_opt(self, src_id, opt):
        if opt:
            for k, v in opt.items():
                oper = k.split('.')
                cls_name = oper[0]
                meth_name = oper[1]

                cls = utils.import_class('oot.msgapi.%s.%s' % (cls_name, cls_name.title()))
                obj = cls()

                meth = getattr(obj, meth_name)
            if isinstance(v, dict):
                meth(**v)
            elif isinstance(v, list):
                meth(*v)

