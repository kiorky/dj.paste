import logging
import os
import traceback

from webob import Request, exc

from paste.deploy.config import ConfigMiddleware

import pkg_resources
dv = pkg_resources.working_set.by_key.get('django').version
MIN_VERSION = '1.0.3'

from django.core.handlers.wsgi import WSGIHandler
from werkzeug import DebuggedApplication
def debug_factory(global_config, **local_config):
    debug = True
    if 'true' in [global_config.get('evalex', '').lower(),
                  global_config.get('debug', '').lower(),
                  local_config.get('evalex', '').lower()]:
        debug = True
    def filter(app):
        return DebuggedApplication(app, debug)
    return filter

def django_factory(global_config, **local_config):
    """
    A paste.httpfactory to wrap a django WSGI based application.
    """
    log = logging.getLogger('dj.paste')
    conf = global_config.copy()
    conf.update(**local_config)
    dmk = 'django_settings_module'
    if dmk in local_config:
        os.environ['DJANGO_SETTINGS_MODULE'] = local_config[dmk].strip()
        del local_config[dmk]
    app = ConfigMiddleware(WSGIHandler(), conf)
    debug = False
    if global_config.get('debug', 'False').lower() == 'true':
        debug = True
    if debug:
        if dv < MIN_VERSION:
            # This is only needed for Django versions < [7537]:
            def null_500_response(request, exc_type, exc_value, tb):
                raise exc_type, exc_value, tb
            from django.views import debug
            debug.technical_500_response = null_500_response

    def django_app(environ, start_response):
        environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
        req = Request(environ)
        try:
            resp = req.get_response(app)
            return resp(environ, start_response)
        except Exception, e:
            if not debug:
                log.error('%r: %s', e, e)
                log.error('%r', environ)
                return exc.HTTPServerError(str(e))(environ, start_response)
            else:
                raise
    return django_app
