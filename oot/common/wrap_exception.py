__author__ = 'xiaoxubeii'

import functools
from webob import exc
import inspect
from monitorapi.proxy import translate_exception


def do_wrap_exception():
    """This decorator wraps a method to catch any exceptions that may
    get thrown. It also optionally sends the exception to the notification
    system.
    """

    def inner(f):
        def wrapped(self, *args, **kw):
            try:
                return f(self, *args, **kw)
            except Exception as e:
                if isinstance(e, exc.HTTPError):
                    raise e
                else:
                    cls = exc.status_map.get(e.code, exc.HTTPServerError)
                    raise cls(explanation=e.format_message())

        return functools.wraps(f)(wrapped)

    return inner


def wrap_exception(cls):
    for name, m in inspect.getmembers(cls, inspect.ismethod):
        if not name.startswith('_') or name.startswith('_action'):
            setattr(cls, name, do_wrap_exception()(m))
    return cls