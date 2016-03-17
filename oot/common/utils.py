__author__ = 'tardis'
import sys
import json
from oslo_config import cfg


def import_class(import_str):
    """Returns a class from a string including module and class."""
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    return getattr(sys.modules[mod_str], class_str)


def import_module(import_str):
    __import__(import_str)
    return sys.modules[import_str]


class ViewBuilder(object):
    def __getattr__(self, item):
        return self._def_fun

    def _def_fun(self, body):
        return json.dumps(body, ensure_ascii=False)


def cp_dict(d, *args):
    if d:
        new_d = {}
        for ks in args:
            if isinstance(ks, list):
                for k in ks:
                    if k in d:
                        new_d[k] = d.get(k)
            elif isinstance(ks, dict):
                for k, v in ks.items():
                    new_d[k] = d.get(k, v)

        return new_d


def cp_dict_list(list, *args):
    if list:
        return [cp_dict(d, *args) for d in list]


def get_ed_by_val(d, val):
    return next((k for k, v in d.items() if v == val))


def avg(list):
    return sum(list) / float(len(list))


def str2bool(v):
    return v.lower() in ('true')


opts = [
    cfg.IntOpt('record_limit',
               default=20)
]

CONF = cfg.CONF
CONF.register_opts(opts)


def tran_fields(search_opts):
    common_fields = {}
    if 'retrieveAll' in search_opts:
        retrieve_all = str2bool(search_opts.pop('retrieveAll'))
        if not retrieve_all:
            common_fields['limit'] = CONF.record_limit
    else:
        common_fields['limit'] = CONF.record_limit

    if 'sortfield' in search_opts:
        common_fields['sortfield'] = search_opts.pop('sortfield')
    if 'sortorder' in search_opts:
        common_fields['sortorder'] = search_opts.pop('sortorder')
    if 'time_from' in search_opts:
        common_fields['time_from'] = search_opts.pop('time_from')
    if 'time_till' in search_opts:
        common_fields['time_till'] = search_opts.pop('time_till')

    common_fields['filter'] = search_opts
    return common_fields

