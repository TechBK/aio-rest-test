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
import jinja_config
from mongoclient import db
from bson import json_util
import aiohttp_jinja2
import views




__author__ = 'techbk'

@asyncio.coroutine
def shutdown(server, app, handler):
    sock = server.sockets[0]
    app.loop.remove_reader(sock.fileno())
    sock.close()

    yield from handler.finish_connections(1.0)
    server.close()
    yield from server.wait_closed()
    yield from app.finish()

@asyncio.coroutine
def test(request):
    document = yield from db['restaurants'].find_one()
    # assert 0, document
    # return web.Response(body=json.dumps(document).encode())
    context = {'json': json_util.dumps(document, sort_keys=True, indent=4)}
    # context = {'json': pprint.pformat(document)}
    response = aiohttp_jinja2.render_template('base.html',
                                              request,
                                              context)
    # assert 0

    return response

@asyncio.coroutine
def init(loop):
    """
    - Khoi tao handler
    - Tao handler va run service
    """

    app = web.Application(loop=loop)

    jinja_config.setup(app)

    app.router.add_route('GET', '/test/', test, name='test')
    app.router.add_route('*', '/notes/{id}/', views.NoteView, name='note-detail')

    app.router.add_route('*', '/notes/', views.NotesView, name='notes')
    # app.router.add_route('*', )

    handler = app.make_handler()
    srv = yield from loop.create_server(handler, '0.0.0.0', 8080)
    print("Server started at http://0.0.0.0:8080")
    return srv, app, handler


loop = asyncio.get_event_loop()
srv, app, handler = loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(shutdown(srv, app, handler))
loop.close()