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
from handlers import JobsHandler
from aiohttp import web


__author__ = 'techbk'


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    # app.router.add_route('POST', '/runtask/', jobs.runtask, name='runtask')
    # app.router.add_route('GET', '/listjobs/', jobs.listjobs, name='listjobs')
    # app.router.add_route('GET', '/job/', jobs.job, name='job')
    # app.router.add_route('POST', '/canceljob/', jobs.canceljob, name='canceljob')

    handler = app.make_handler()
    srv = yield from loop.create_server(handler, '0.0.0.0', 8080)
    print("Server started at http://0.0.0.0:8080")
    return srv, handler


loop = asyncio.get_event_loop()
srv, handler = loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
