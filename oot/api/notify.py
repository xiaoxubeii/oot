# encoding: utf-8
from dalek.api.openstack import wsgi
from oot.resource import notify


class Controller(wsgi.Controller):
    def __init__(self, **kwargs):
        self.notify = notify.Notify()
        super(Controller, self).__init__(**kwargs)

    def create(self, req, body):
        self.notify.create(body)


def create_resource():
    return wsgi.Resource(Controller())
