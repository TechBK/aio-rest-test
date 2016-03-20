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
from aio_rest_test import jinja_config
from aio_rest_test import urls
import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aio_rest_test import config
from motor.motor_asyncio import AsyncIOMotorClient
import aiohttp_cors


__author__ = 'techbk'


@asyncio.coroutine
def shutdown(server, _app, _handler):
    sock = server.sockets[0]
    _app.loop.remove_reader(sock.fileno())
    sock.close()

    yield from _handler.finish_connections(1.0)
    server.close()
    yield from server.wait_closed()
    yield from _app.finish()


@asyncio.coroutine
def mongo_setup(ioloop, _app, test, db, host, port):
    assert host, 'MONGO host'
    assert port, 'MONGO port'
    assert db and isinstance(db, str), 'MONGO DB'

    _app['client'] = AsyncIOMotorClient(host, port, io_loop=ioloop)
    if test:
        yield from _app['client'].drop_database('test')
        db = 'test'
    _app['db'] = _app['client'][db]


@asyncio.coroutine
def init(ioloop, ip='127.0.0.1', port=8080, test=False):
    """
    - Khoi tao handler
    - Tao handler va run service
    :param test:
    :param port:
    :param ip:
    :param ioloop:
    """

    _app = web.Application(loop=ioloop, debug=True)
    cors = aiohttp_cors.setup(_app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
        )
    })
    aiohttp_session.setup(_app,
                          EncryptedCookieStorage(b'Thirty  two  length  bytes  key.'))
    yield from mongo_setup(ioloop, _app, test, **config.MONGO_DB)
    jinja_config.setup(_app)
    urls.urls(_app)
    # Configure CORS on all routes.
    for route in list(_app.router.routes()):
        cors.add(route)
    _handler = _app.make_handler()
    _srv = yield from ioloop.create_server(_handler, ip, port)
    print("Server started at http://{}:{}".format(ip, port))
    return _srv, _app, _handler

# print('sdfhaskjdfh')


# if '__name__' == '__main__':
loop = asyncio.get_event_loop()
srv, app, handler = loop.run_until_complete(init(loop, ip='0.0.0.0'))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(shutdown(srv, app, handler))
loop.close()
