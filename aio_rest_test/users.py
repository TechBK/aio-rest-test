import asyncio
from bson import json_util
import hashlib
from aiohttp_session import get_session
from aio_rest_test.utils import views
from aio_rest_test.utils.coroutine import handle_errors
import time


def login_required(func = None):
    """
    Coroutine to check login requirement!!!
    :param func:
    :return:
    """

    @asyncio.coroutine
    def wrapped(s):
        session = yield from get_session(s.request)
        user = session.get('user', None)
        assert user, 'Login Requirement!!!'
        r = yield from func(s)
        return r

    return wrapped


@asyncio.coroutine
def hash_pass(password):
    # used to hash the password similar to how MySQL hashes passwords with the password() function.
    hash_password = hashlib.sha1(password.encode('utf-8')).digest()
    hash_password = hashlib.sha1(hash_password).hexdigest()
    hash_password = '*' + hash_password.upper()
    return hash_password


@asyncio.coroutine
def do_login(request, coll, login=None, password=None):
    session = yield from get_session(request)
    assert (session.get('user') is None), Exception('Need Logout before!')
    assert login, ValueError('None is allowed as login value')
    assert password, ValueError('None is not allowed as password value')
    user = yield from coll.find_one({'login': login})
    assert user, ValueError('%s is not exist' % login)
    hash_password = yield from hash_pass(password)
    if user['password'] != hash_password:
        raise Exception('Password is incorrect!')
    session['user'] = json_util.dumps(user)
    user.pop('password', None)
    user.pop('_id', None)
    return user

@asyncio.coroutine
def do_logout(session, coll):
    user = session.pop('user', None)
    # assert 0, user
    # assert user is not None, Exception('User have not been login!')
    if user:
        user = json_util.loads(user)
        r = yield from coll.update({'_id': str(user['_id'])},
                                   {'last_login': time.time()})
        return True
    else:
        return False


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



@asyncio.coroutine
def do_signin(coll, login = None, password1 = None, password2 = None):
    """
    do sign in.
    :param coll:
    :param login:
    :param password1:
    :param password2:
    :return:
    """
    assert login, 'Require Username'
    assert password1, 'Require Password'
    assert password2, 'Require Confirm Password'
    assert password1 == password2, 'Require Password'
    data = {}
    data['login'] = login.lower()
    data['password'] = yield from hash_pass(password1)
    # return notes
    _id = yield from coll.insert(data)

    document = yield from coll.find_one({'_id': _id}, {'_id': 0, 'login': 1})
    return document

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
        # assert 0, self.request
        # session = yield from get_session(self.request)
        data = yield from self.data()
        data['login'] = data['login'].lower()
        # try:
        user = yield from do_login(self.request, self.coll, **data)
        document = {"ok": 1, "user": user}

        return self.response(document)


class LogoutView(views.View):
    @property
    def coll(self):
        return self.request.app['db'].users

    @handle_errors
    @login_required
    @asyncio.coroutine
    def post(self):
        session = yield from get_session(self.request)
        result = yield from do_logout(session, self.coll)
        # assert result, "User have't been login!" || Vi da co login_required
        return self.response({'ok': 1})