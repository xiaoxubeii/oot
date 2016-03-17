from oslo_config import cfg
import webob.dec
import webob.exc

from dalek.openstack.common import log as logging
from dalek import wsgi

auth_opts = [
]

CONF = cfg.CONF
CONF.register_opts(auth_opts)

LOG = logging.getLogger(__name__)


class WSGIContext(wsgi.Middleware):
    """Make a request context from keystone headers."""

    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        ctx = RequestContext()
        req.environ['context'] = ctx
        return self.application


class RequestContext(object):
    """Security context and request information.

    Represents the user taking a given action within the system.

    """

    def __init__(self, **kwargs):
        pass
