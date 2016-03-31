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
from notes_apps.notes_app import app, mongo_setup


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

loop = asyncio.get_event_loop()
loop.run_until_complete(mongo_setup(loop, app, test=False))
handler = app.make_handler()
srv = loop.create_server(handler, '0.0.0.0', 8080)
print("Server started at http://{}:{}".format('0.0.0.0', 8080))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(shutdown(srv, app, handler))
loop.close()
