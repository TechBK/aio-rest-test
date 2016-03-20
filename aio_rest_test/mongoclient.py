from motor.motor_asyncio import AsyncIOMotorClient


def setup(app):
    # yield from validates.run()
    app['client'] = AsyncIOMotorClient('localhost', 27017)
    app['db'] = app['client'].mydb
