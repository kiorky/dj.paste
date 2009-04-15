import logging
import os
import traceback

from webob import Request, exc

from paste.deploy.config import ConfigMiddleware

from django.core.handlers.wsgi import WSGIHandler

def django_factory(global_config, **local_config):
    """
    A paste.httpfactory to wrap a django WSGI based application.
    """
    log = logging.getLogger('makina.django.paste')
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
    def django_app(environ, start_response):
        environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
        req = Request(environ)
        try:
            resp = req.get_response(app)
        except Exception, e:
            log.error('%r: %s', e, e)
            log.error('%r', environ)
            if debug:
                log.error('%r', traceback.format_exc())
            return exc.HTTPServerError(str(e))(environ, start_response)
        app_iter = resp(environ, start_response)
        result = app_iter
        if hasattr(app_iter, 'close'):
            result = [data for data in app_iter]
            app_iter.close()
        return result 
    return django_app

