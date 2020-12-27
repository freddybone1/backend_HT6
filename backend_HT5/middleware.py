from django.utils.deprecation import MiddlewareMixin
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s', filename='log.txt')


class LogMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        logging.info('request = {}'.format(request))
        return view_func(request, *view_args, **view_kwargs)


class RawDataMiddleware(MiddlewareMixin):
    pass


class IdentifyResponseMiddleware(MiddlewareMixin):
    pass
