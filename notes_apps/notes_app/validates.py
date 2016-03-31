from motor.motor_asyncio import AsyncIOMotorClient
import asyncio


class ValidateSetup(object):
    def __init__(self, collection=None, validator=None):
        # self.client =
        if collection:
            self.collection = collection
        assert self.collection and isinstance(self.collection, str), \
            '`collection` must to be string.'
        if validator:
            self.validator = validator
        assert self.validator and isinstance(self.validator, list), \
            '`validator` parameter is required!'
        # self.collection = collection
        self.db = AsyncIOMotorClient('localhost', 27017).mydb
        self.coll = self.db[self.collection]

    @asyncio.coroutine
    def run(self):
        count = yield from self.coll.count()
        if count:
            yield from self.db.command(
                {
                    'collMod': self.collection,
                    'validator': {'$or': self.validator}
                }
            )
        else:
            yield from self.db.createCollection(
                self.collection,
                {
                    'validator': {'$or': self.validator}
                })


class Users(ValidateSetup):
    collection = 'users'
    validator = [
        {
            '_id':
                {
                    '$exists': True,
                    '$type': 'objectId'
                }
        },
        {
            'login':
                {
                    '$exists': True,
                    '$type': 'string'

                }
        },
        {
            'password':
                {
                    '$exists': True,
                    '$type': 'string'
                }
        },
        {
            'last_login':
                {

                }
        }
    ]


class Notes(ValidateSetup):
    collection = 'notes'
    validator = [
        {
            '_id':
            {
                '$exists': True,
                '$type': 'objectId'
            }
        },
        {
            "is_public":
            {
                '$exists': True,
                '$type': 'bool'
            }

        },
        {
            'text':
            {
                '$exists': True,
                '$type': 'array'
            }
        },
        {
            'users':
            {
                '$exists': True,
                '$type': 'array',
                'elemMatch': 'string'
            }
        },
        {
            'tags':
            {
                '$exists': True,
                '$type': 'array',
                'elemMatch': 'string'
            }
        }
    ]


# class Tags(ValidateSetup):
#     validator = [
#         {'_id':
#             {
#                 '$exits': True,
#                 '$type': 'objectId'
#             }
#         },
#         {'slug':
#             {
#                 '$exits': True,
#                 '$type': 'string'
#             }
#         }
#     ]

@asyncio.coroutine
def run():
    models = [Users(), Notes()]
    for m in models:
        yield from m.run()
