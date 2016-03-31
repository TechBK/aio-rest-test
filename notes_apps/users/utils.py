import asyncio
import datetime
import jwt
from bson import json_util
import hashlib
from aiohttp_session import get_session

SECRET = 'techbk_pro'

def jwt_encode(user):
    """

    :param user: UserObject
    :return:
    """
    return jwt.encode(
        {
            'user': user,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        },
        SECRET,
        algorithm='HS256',
        json_encoder=json_util.dumps
    )


def jwt_decode(jwt_payload):
    """

    :param jwt_payload:
    :return: User Object
    """
    return jwt.decode(jwt_payload, SECRET)['user']



def login_required(func = None):
    """
    Coroutine to check login requirement!!! and set s.user = user
    :param func:
    :param s: View Class
    :return:
    """
    @asyncio.coroutine
    def wrapped(s):
        # session = yield from get_session(s.request)
        # user = session.get('user', None)
        token = s.request.headers.get('Authorization')
        assert token, 'Login Requirement!!!'
        user = jwt_decode(token)
        assert user, 'Login Requirement!!!'
        s.user = user
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
    # session = yield from get_session(request)
    # assert (session.get('user') is None), Exception('Need Logout before!')
    assert login, ValueError('None is allowed as login value')
    assert password, ValueError('None is not allowed as password value')
    user = yield from coll.find_one({'login': login})
    assert user, ValueError('%s is not exist' % login)
    hash_password = yield from hash_pass(password)
    if user['password'] != hash_password:
        raise Exception('Password is incorrect!')

    # session['user'] = json_util.dumps(user)
    user.pop('password', None)
    token = jwt_encode(user)

    # user.pop('_id', None)
    return user, token


# @asyncio.coroutine
# def do_logout(session, coll):
#     user = session.pop('user', None)
#     if user:
#         user = json_util.loads(user)
#         r = yield from coll.update({'_id': user['_id']},
#                                    {'last_login': datetime.datetime.utcnow()})
#         return True
#     else:
#         return False

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