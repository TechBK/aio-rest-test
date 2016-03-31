#
# Copyright 2016 - Nguyen Quang "TechBK" Binh.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from aiohttp import web
from . import jinja_config, settings
# from aio_rest_test import urls
# import aiohttp_session
# from aiohttp_session.cookie_storage import EncryptedCookieStorage
import aiohttp_cors
from motor.motor_asyncio import AsyncIOMotorClient
from aio_framework.utils.urls import init_urls


@asyncio.coroutine
def mongo_setup(ioloop, app, test=True):
    st = settings.MONGO_DB
    assert st['host'], 'MONGO host'
    assert st['port'], 'MONGO port'

    app['client'] = AsyncIOMotorClient(st['host'], st['port'], io_loop=ioloop)
    if test:
        yield from app['client'].drop_database('test')
        db = 'test'
    assert st['db'] and isinstance(st['db'], str), 'MONGO DB'
    app['db'] = app['client'][st['db']]


# @asyncio.coroutine
# def init(ioloop, ip='127.0.0.1', port=8080, test=False):
#     """
#     - Khoi tao handler
#     - Tao handler va run service
#     :param test:
#     :param port:
#     :param ip:
#     :param ioloop:
#     """
#
#     app = web.Application(loop=ioloop, debug=True)
#     cors = aiohttp_cors.setup(app, defaults={
#         "*": aiohttp_cors.ResourceOptions(
#                 allow_credentials=True,
#                 expose_headers="*",
#                 allow_headers="*",
#         )
#     })
#
#
#     yield from mongo_setup(ioloop, app, test)
#
#     jinja_config.setup(app)
#     urls.urls(app)
#     # Configure CORS on all routes.
#     for route in list(app.router.routes()):
#         cors.add(route)
#     handler = app.make_handler()
#     srv = yield from ioloop.create_server(handler, ip, port)
#     print("Server started at http://{}:{}".format(ip, port))
#     return srv, app, handler

ioloop = asyncio.get_event_loop()

router = init_urls(settings.URLS)
app = web.Application(loop=ioloop, debug=True, router=router)

jinja_config.setup(app)

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)