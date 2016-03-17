__author__ = 'tardis'

from oslo_config import cfg
from dalek.openstack.common import log as logging
import xmlrpclib
from datetime import datetime
from oot.common.utils import cp_dict

opts = [
    cfg.StrOpt('cobbler_username',
               default="cobbler"),
    cfg.StrOpt('cobbler_password',
               default="cobbler"),
    cfg.StrOpt('cobbler_url',
               default="http://localhost/cobbler_api")
]

CONF = cfg.CONF
CONF.register_opts(opts)


class CobblerManager():
    def __init__(self):
        self.server = xmlrpclib.Server(CONF.cobbler_url, allow_none=True)
        self.token_time = None
        self.token_str = None

    @property
    def token(self):
        now = datetime.utcnow()
        if self.token_time and self.token_str and now.minute - self.token_time.minute < 60:
            return self.token_str
        else:
            self.token_str = self.server.login(CONF.cobbler_username, CONF.cobbler_password)
            self.token_time = datetime.utcnow()
            return self.token_str

    def _exist_server(self, name):
        list = self.server.find_system({'name': name})
        return list is not None and len(list) > 0

    def init_server(self, m):
        if self._exist_server(m.get('name')):
            return

        id = self.server.new_system(self.token)
        self.server.modify_system(id, 'name', m.get('name'), self.token)
        self.server.modify_system(id, 'profile', m.get('profile'), self.token)
        self.server.modify_system(id, 'mac-address', m.get('mac_address'), self.token)

        # server ipmi
        # self.server.modify_system(id, 'power_address', m.get('ipmi_address'), self.token)
        # self.server.modify_system(id, 'power_user', m.get('ipmi_user'), self.token)
        # self.server.modify_system(id, 'power_pass', m.get('ipmi_pass'), self.token)
        # self.server.modify_system(id, 'power_type', 'ipmilan', self.token)

        # server interfaces
        # ifs = m.get('interfaces')
        # if ifs:
        # for k, v in m.get('interfaces').items():
        # self.server.modify_system(id, 'modify_interface',
        # {
        # 'macaddress-%s' % k: v.get('mac'),
        # 'ipaddress-%s' % k: v.get('ip')
        # },
        # self.token)

        self.server.save_system(id, self.token)
        self.server.sync(self.token)

    def register_server(self, m):
        handle = self.server.get_system_handle(m.get('name'), self.token)
        self.server.modify_system(handle, 'hostname', m.get('host_name'), self.token)

        ifs = m.get('interfaces')
        if ifs:
            for k, v in m.get('interfaces').items():
                ip = v.get('ip')
                ifa = {
                    'macaddress-%s' % k: v.get('mac')
                }
                if ip:
                    ifa['ipaddress-%s' % k] = ip
                self.server.modify_system(handle, 'modify_interface',
                                          ifa,
                                          self.token)

        ksmeta = cp_dict(m.get('conf'),
                         ['admin_password', 'tunnel_endpoint_ip', 'host_ip', 'service_host', 'service_password',
                          'mysql_host', 'mysql_password', 'rabbit_hosts', 'service_token', 'dest',
                          'neutron_ml2_tenant_network_type', 'ovs_enable_tunneling', 'enabled_services',
                          'op_pkg_url', 'op_dep_pkg'])
        ksmeta_str = ''
        for k, v in ksmeta.items():
            ksmeta_str += '%s=%s ' % (k, v)
        self.server.modify_system(handle, 'ksmeta', ksmeta_str, self.token)

        self.server.save_system(handle, self.token)
        self.server.sync(self.token)

    def list_server(self):
        return self.server.get_systems()

    def get_server(self, name):
        return self._co_to_bs_server(self.server.get_system(name))

    def delete_server(self, name):
        self.server.remove_system(name)

    def _bs_to_co_server(self, bs):
        # TODO
        return bs

    def _co_to_bs_server(self, co):
        bs = {}
        bs['name'] = co['name']
        bs['host_name'] = co['hostname']
        bs['ipmi_user'] = co['power_user']
        bs['ipmi_pass'] = co['power_pass']
        bs['ipmi_address'] = co['power_address']

        ifs = co['interfaces']
        new_ifs = {}
        if ifs and len(ifs) > 0:
            for k, v in ifs.items():
                new_ifs[k] = {
                    'mac': v['mac_address'],
                    'ip': v['ip_address']
                }
        bs['interfaces'] = new_ifs

        return bs
