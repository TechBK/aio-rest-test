import asyncio
from aio_framework.utils import views
from aio_framework.utils.coroutine import handle_errors
from notes_apps.users.utils import login_required


class NoteView(views.DetailView):
    @property
    def coll(self):
        return self.request.app['db'].notes


class NotesView(views.ListView):
    @property
    def coll(self):
        return self.request.app['db'].notes

    @handle_errors
    @login_required
    @asyncio.coroutine
    def get(self):
        """
        Khi nguoi dung da dang nhap, muon xem note cua ban than
        :return:
        """
        current_user = self.user
        cursor = self.coll.find({'users': {'$all': current_user['login']}})
        documents = yield from cursor.to_list(length=20)
        return self.response(documents)

    @handle_errors
    @login_required
    @asyncio.coroutine
    def post(self):
        current_user = self.user
        data = yield from self.data()
        if not isinstance(data, list):
            data = [data]
        for note in data:
            if 'users' not in note:
                note['users'] = [current_user['login']]
            elif current_user['login'] not in note.get('user'):
                note['users'].append(current_user['login'])

        ids = yield from self.coll.insert(data)
        if not isinstance(ids, list):
            ids = [ids]
        _len = len(ids)

        cursor = self.coll.find({'_id': {'$in': ids}})
        documents = yield from cursor.to_list(length=_len)

        return self.response(documents)


class NotesOfUser(views.ListView):
    @property
    def coll(self):
        return self.request.app['db'].notes

    # # @asyncio.coroutine
    # def get_pk(self):
    #     query = self.request.match_info.get('login')
    #     return {''}

    @handle_errors
    @asyncio.coroutine
    def get(self):
        data = yield from self.data()
        login = self.request.match_info.get('login')
        # user = yield from self.request.app['db'].users.find_one({'login': login}, {'login': 1})
        # user = yield from self.get_user_session()
        cursor = self.coll.find({'users': {'$all': login}}.update(data))
        documents = yield from cursor.to_list(length=20)
        return self.response(documents)

    @handle_errors
    @login_required
    @asyncio.coroutine
    def post(self):
        login = self.request.match_info.get('login')
        user = yield from self.request.app['db'].users.find_one({'login': login}, {'login': 1})
        data = yield from self.data()
        assert data, 'Post Note'
        if not isinstance(data, list):
            data = [data]
        for note in data:
            if 'users' not in note:
                note['users'] = [user['login']]
            elif user['login'] not in note.get('user'):
                note['users'].append(user['login'])

        ids = yield from self.coll.insert(data)
        if not isinstance(ids, list):
            ids = [ids]
        _len = len(ids)

        cursor = self.coll.find({'_id': {'$in': ids}})
        documents = yield from cursor.to_list(length=_len)

        return self.response(documents)


class NotesOfTag(views.ListView):
    @property
    def coll(self):
        return self.request.app['db'].notes

    @handle_errors
    @asyncio.coroutine
    def get(self):
        data = yield from self.data()
        tag = self.request.match_info.get('text')
        # user = yield from self.request.app['db'].users.find_one({'login': login}, {'login': 1})
        # user = yield from self.get_user_session()
        cursor = self.coll.find({'users': {'$all': tag}}.update(data))
        documents = yield from cursor.to_list(length=20)
        return self.response(documents)
