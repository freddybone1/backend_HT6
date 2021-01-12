import uuid  # noqa

from django.utils.deprecation import MiddlewareMixin  # noqa
import logging  # noqa

"""
We make logs using logging library and save all logs
in log.txt with specific format time/level(INFO)/message text
"""
logging.basicConfig(level=logging.INFO, format='%(asctime)s'
                    ' :: %(levelname)s :: %(message)s', filename='log.txt')


class LogMiddleware(MiddlewareMixin):
    """
    This middleware save request data in log, each time we make request
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        logging.info('request = {}'.format(request))
        return view_func(request, *view_args, **view_kwargs)


class RawDataMiddleware(MiddlewareMixin):
    """
    This middleware wait for any request and
    generate unique hash value for request.
    Then save it in request object META dict.
    Shows it in log file
    """
    def process_request(self, request):

        request.META['uuid'] = uuid.uuid4()

        logging.info(' request uuid = {}'.format(request.META['uuid']))


class IdentifyResponseMiddleware(MiddlewareMixin):
    """
    This middleware get hash value from request.META
    and set in new header 'uuid' in response object
    Shows it in log file
    """

    def process_response(self, request, response):

        response['uuid'] = request.META['uuid']

        logging.info('response uuid = {}'.format(request.META['uuid']))
        return response
