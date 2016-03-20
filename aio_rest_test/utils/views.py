from aiohttp import web
import asyncio
import aiohttp_jinja2
from bson import json_util, objectid
from aio_rest_test.utils.coroutine import handle_errors
from aiohttp_session import get_session


class View(web.View):

    @asyncio.coroutine
    def get_user_session(self):
        """
        Before run it, must to wrrap handle request function by @login_required!
        :return: current user or {}
        """
        session = yield from get_session(self.request)
        user = session.get('user', '{}')
        return json_util.loads(user)

    @property
    def coll(self):
        return None

    @property
    def accepts(self):
        return self.request.headers.getall('ACCEPT', [])

    @property
    def json(self):
        return 'application/json' in self.accepts

    def response(self, document):
        if self.json:
            # headers = {'Access-Control-Allow-Origin': '*',
            #            'Access-Control-Request-Method': '*',
            #            'Access-Control-Allow-Headers': '*'
            #            }
            return web.Response(body=json_util.dumps(document, sort_keys=True, indent=4).encode())
        context = {'json': json_util.dumps(document, sort_keys=True, indent=4)}
        return aiohttp_jinja2.render_template('/base/json.html',
                                              self.request,
                                              context)

    @asyncio.coroutine
    def data(self):
        text = yield from self.request.text()
        if text:
            return json_util.loads(text)
        else:
            return {}


class DetailView(View):
    pk = '_id'

    @property
    def get_pk(self):

        if self.pk == '_id':
            _pk = self.request.match_info.get('id')
            _pk = objectid.ObjectId(_pk)
        else:
            _pk = self.request.match_info.get(self.pk)
        return {self.pk: _pk}

    @handle_errors
    @asyncio.coroutine
    def get(self):
        document = yield from self.coll.find_one(self.get_pk)
        return self.response(document)

    # @handle_errors
    @asyncio.coroutine
    def put(self):
        data = yield from self.data()
        data.pop('_id', None)
        # get_pk = self.get_pk
        # note = yield from self.coll.find_one(self.get_pk)
        result = yield from self.coll.update(self.get_pk, {'$set': data})
        document = yield from self.coll.find_one(self.get_pk)
        return self.response(document)


class ListView(View):
    @handle_errors
    @asyncio.coroutine
    def get(self):
        cursor = self.coll.find()
        documents = yield from cursor.to_list(length=20)
        return self.response(documents)