from aiohttp import web
import asyncio
import aiohttp_jinja2
from bson import json_util, objectid
from mongoclient import db
# from motor.motor_asyncio import
# from pymongo

class View(web.View):
    # coll = None

    @property
    def accepts(self):
        return self.request.headers.getall('ACCEPT', [])

    @property
    def json(self):
        return 'application/json' in self.accepts

    def response(self, document):
        if self.json:
            return web.Response(body=json_util.dumps(document, sort_keys=True, indent=4).encode())
        context = {'json': json_util.dumps(document, sort_keys=True, indent=4)}
        return aiohttp_jinja2.render_template('base.html',
                                              self.request,
                                              context)


class DetailView(View):
    # coll = None
    @asyncio.coroutine
    def get(self):
        _id = self.request.match_info.get('id', None)
        _id = objectid.ObjectId(_id)
        document = yield from self.coll.find_one({'_id':_id})
        return self.response(document)


    @asyncio.coroutine
    def put(self):
        _id = self.request.match_info.get('id', None)
        _id = objectid.ObjectId(_id)
        text = yield from self.request.text()

        note = json_util.loads(text)
        note.pop('_id', None)
        result = yield from self.coll.update({'_id': _id}, {'$set':note})
        note = yield from self.coll.find_one({'_id': _id})
        return self.response(note)

class ListView(View):
    @asyncio.coroutine
    def get(self):
        cursor = self.coll.find()
        notes = yield from cursor.to_list(length=20)
        return self.response(notes)

    @asyncio.coroutine
    def post(self):
        text = yield from self.request.text()
        notes = json_util.loads(text)
        # return notes
        ids = yield from self.coll.insert(notes)
        if ids is not list:
            _len = 1
            ids = [ids]
        else:
            _len = len(ids)
        cursor = self.coll.find({'_id': {'$in': ids} })
        notes = yield from cursor.to_list(length=_len)

        return self.response(notes)


class NoteView(DetailView):
    coll = db.notes

    # @asyncio.coroutine
    # def get(self):
    #     _id = self.request.match_info.get('id', None)
    #     _id = objectid.ObjectId(_id)
    #     document = yield from db.notes.find_one({'_id':_id})
    #     return self.response(document)
    #
    #
    # @asyncio.coroutine
    # def put(self):
    #     _id = self.request.match_info.get('id', None)
    #     _id = objectid.ObjectId(_id)
    #     text = yield from self.request.text()
    #
    #     note = json_util.loads(text)
    #     note.pop('_id', None)
    #     result = yield from db.notes.update({'_id': _id}, {'$set':note})
    #     note = yield from db.notes.find_one({'_id': _id})
    #     return self.response(note)
    #     # except KeyError:
    #     #     self.response({'errors': '`_id` KeyError'})


class NotesView(ListView):
    coll = db.notes
    # @asyncio.coroutine
    # def get(self):
    #     cursor = db.notes.find()
    #     notes = yield from cursor.to_list(length=20)
    #     return self.response(notes)
    #
    # @asyncio.coroutine
    # def post(self):
    #     text = yield from self.request.text()
    #     notes = json_util.loads(text)
    #     # return notes
    #     ids = yield from db.notes.insert(notes)
    #     if ids is not list:
    #         _len = 1
    #         ids = [ids]
    #     else:
    #         _len = len(ids)
    #     cursor = db.notes.find({'_id': {'$in': ids} })
    #     notes = yield from cursor.to_list(length=_len)
    #
    #     return self.response(notes)


