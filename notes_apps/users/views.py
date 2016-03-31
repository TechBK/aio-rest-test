import asyncio
from aio_framework.utils import views
from aio_framework.utils.coroutine import handle_errors
from .utils import login_required, do_login, do_signin

class UserView(views.View):
    pk = 'login'

    @property
    def coll(self):
        return self.request.app['db'].users

    def get_pk(self):
        _pk = self.request.match_info.get(self.pk)
        return {self.pk: _pk}

    @handle_errors
    @asyncio.coroutine
    def get(self):
        document = yield from self.coll.find_one(self.get_pk())
        return self.response(document)

    @handle_errors
    @login_required
    @asyncio.coroutine
    def put(self):
        """
        Chua co update PassWord
        :return:
        """
        data = yield from self.data()
        data.pop('_id', None)
        data.pop(self.pk, None)
        data.pop('password', None)
        result = yield from self.coll.update(self.get_pk(), {'$set': data})
        document = yield from self.coll.find_one(self.get_pk(), {'_id': 0, 'login': 1})
        return self.response(document)


class UsersView(views.ListView):
    @property
    def coll(self):
        return self.request.app['db'].users

    @handle_errors
    @asyncio.coroutine
    def get(self):
        data = yield from self.data()
        cursor = self.coll.find(data, {'password': 0})
        documents = yield from cursor.to_list(length=20)
        return self.response(documents)

    @handle_errors
    @asyncio.coroutine
    def post(self):
        """
        DO sign in here
        :return:
        """
        data = yield from self.data()
        user = yield from do_signin(self.coll, **data)

        return self.response(user)


class LoginView(views.View):
    @property
    def coll(self):
        return self.request.app['db'].users

    @handle_errors
    @asyncio.coroutine
    def post(self):
        data = yield from self.data()
        data['login'] = data['login'].lower()
        # try:
        user, token = yield from do_login(self.request, self.coll, **data)
        document = {"ok": 1, "user": user, 'token': token}

        return self.response(document)


class LogoutView(views.View):
    # @property
    # def coll(self):
    #     return self.request.app['db'].users

    @handle_errors
    @asyncio.coroutine
    def post(self):
        return self.response({})