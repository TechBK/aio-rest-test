import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('localhost', 27017)

# db = client['test']
db = client.mydb
