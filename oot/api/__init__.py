# encoding: utf-8
import dalek.api.openstack
from dalek.api.openstack.compute import extensions
from oot.api import server, notify


class APIRouter(dalek.api.openstack.APIRouter):
    ExtensionManager = extensions.ExtensionManager

    def _setup_routes(self, mapper, ext_mgr, init_only):
        self.resources['servers'] = server.create_resource()
        mapper.resource("server", "servers",
                        controller=self.resources['servers'], no_need_project=True)

        self.resources['notifies'] = notify.create_resource()
        mapper.resource("notify", "notifies",
                        controller=self.resources['notifies'], no_need_project=True)

