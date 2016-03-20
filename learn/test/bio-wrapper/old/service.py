__author__ = 'techbk'

import asyncio
from aiohttp import web


@asyncio.coroutine
def init(loop):
    """
    - Khoi tao cac object handler
        + TasksHandler handle cac request listoftasks, runnewtask..
        + ConfigHandler handle cac request xem, settup,... config
        + TaskHandler handle cac request checkresult, checkstatus... cua task co ID = {id}
    - Khoi tao va run service
    """
    tasks = JobsHandler()
    config = ConfigHandler()
    task = TaskHandler()



    app = web.Application(loop = loop)
    app.router.add_route('*', '/tasks/{do_something}', tasks.handle)
    app.router.add_route('*', '/config/{do_something}', config.handle)
    app.router.add_route('*', '/task/{id}/{do_something}', task.handle)

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