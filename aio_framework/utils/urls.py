from importlib import import_module
from aiohttp import web

class URL:
    arg = None
    kwarg = None

    def __init__(self, *args, **kwargs):
        assert args, 'Plzzz give args'
        self.arg = args
        if kwargs:
            self.kwarg = kwargs


def init_urls(urls):
    url_dispatcher = web.UrlDispatcher()
    for url_list in urls:
        url_list = import_module('urls', url_list)
        for url in url_list:
            url_dispatcher.add_route(*url.arg, **url.kwarg)

    return url_dispatcher
