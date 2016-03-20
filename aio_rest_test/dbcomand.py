# from aio_rest_test.mongoclient import setup
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


def command():
    db = AsyncIOMotorClient('localhost', 27017).mydb
    # db = yield from DB()
    r = yield from db.users.remove({})
    r = yield from db.notes.remove({})

    print(r)


loop = asyncio.get_event_loop()
loop.run_until_complete(command())
# command()
