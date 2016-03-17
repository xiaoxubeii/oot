import sys
from oslo_config import cfg
from dalek.openstack.common import log as logging
from dalek import service, utils, config
from oot import DEFAULT_CONFIG

opts = [
    cfg.StrOpt('oot_listen',
               default="0.0.0.0"),
    cfg.IntOpt('oot_listen_port',
               default=8900),
    cfg.IntOpt('oot_workers',
               default=1)
]

CONF = cfg.CONF
CONF.register_opts(opts)


def main():
    config.parse_args(sys.argv, default_config_files=[DEFAULT_CONFIG])
    logging.setup("oot")
    utils.monkey_patch()

    launcher = service.process_launcher()
    api = 'oot'
    server = service.WSGIService(api, use_ssl=False)
    launcher.launch_service(server, CONF.oot_workers)
    launcher.wait()


if __name__ == '__main__':
    main()
