import asyncio
from bson import json_util
import hashlib
from aiohttp_session import get_session
from notes_apps.utils import views
from notes_apps.utils.coroutine import handle_errors


def login_required(func = None):

    @asyncio.coroutine
    def wrapped(s):
        session = yield from get_session(s.request)
        if not session.get('user'):
            # return s.response({'error':'Login Requirement'})
            raise Exception('Login Requirent')
        r = yield from func(s)
        return r

    return wrapped


class NoteView(views.DetailView):
    @property
    def coll(self):
        return self.db().notes


class NotesView(views.ListView):
    @property
    def coll(self):
        return self.db().notes



class UserView(views.DetailView):
    pk = 'login'

    @property
    def coll(self):
        return self.db().users

    def get_pk(self):
        _pk = self.request.match_info.get(self.pk)
        return {self.pk: _pk}

    @handle_errors
    @asyncio.coroutine
    def get(self):
        document = yield from self.coll.find_one(self.get_pk())
        return self.response(document)

    @handle_errors
    @asyncio.coroutine
    def put(self):
        text = yield from self.request.text()
        document = json_util.loads(text)
        document.pop('_id', None)
        document.pop(self.pk, None)
        result = yield from self.coll.update(self.get_pk(), {'$set': document})
        document = yield from self.coll.find_one(self.get_pk(), {'_id': 0, 'login': 1})
        return self.response(document)


class UsersView(views.ListView):
    @property
    def coll(self):
        return self.db().users

    @handle_errors
    @asyncio.coroutine
    def post(self):
        text = yield from self.request.text()
        data = json_util.loads(text)
        data['login'] = data['login'].lower()
        data['password'] = yield from hash_pass(data['password'])
        # return notes
        _id = yield from self.coll.insert(data)

        document = yield from self.coll.find_one({'_id': _id}, {'_id': 0, 'login': 1})
        # documents = yield from cursor.to_list(length=_len)

        return self.response(document)


@asyncio.coroutine
def hash_pass(password):
    # used to hash the password similar to how MySQL hashes passwords with the password() function.
    hash_password = hashlib.sha1(password.encode('utf-8')).digest()
    hash_password = hashlib.sha1(hash_password).hexdigest()
    hash_password = '*' + hash_password.upper()
    return hash_password


@asyncio.coroutine
def get_user_session(session):
    user = session['user']
    return json_util.loads(user)


@asyncio.coroutine
def do_login(session, coll, login=None, password=None):
    # assert 0, session.get('user')
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
def do_logout(session):
    user = session.pop('user', None)
    # assert 0, user
    # assert user is not None, Exception('User have not been login!')
    if user:
        return True
    else:
        return False


class LoginView(views.View):
    @property
    def coll(self):
        return self.db().users

    @handle_errors
    @asyncio.coroutine
    def post(self):
        session = yield from get_session(self.request)
        text = yield from self.request.text()
        data = json_util.loads(text)
        data['login'] = data['login'].lower()
        try:
            user = yield from do_login(session, self.coll, **data)
            r = {"ok": 1, "user": user}
        except Exception as e:
            # raise e
            r = {'error': str(e)}
        # document = yield from self.coll.find_one()

        return self.response(r)


class LogoutView(views.View):
    @property
    def coll(self):
        return self.db().users

    @handle_errors
    @login_required
    @asyncio.coroutine
    def post(self):
        session = yield from get_session(self.request)
        result = yield from do_logout(session)
        if not result:
            return self.response({'error': 'User have not been login!'})
        return self.response({'ok': 1})