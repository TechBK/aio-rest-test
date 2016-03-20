import asyncio
import unittest
from aio_rest_test.service import init
import socket
import aiohttp
from bson import json_util


class TestUserUrl(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.srv.close()
        self.loop.stop()
        self.loop.run_forever()
        self.loop.close()

    def find_unused_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    @asyncio.coroutine
    def create_server(self):
        port = self.find_unused_port()
        self.srv, self.app, self.handler = \
            yield from init(self.loop, port=port, test=True)

        url = "http://127.0.0.1:{}".format(port)
        return url

    def test_create_new_user_sucess(self):
        """
        POST /users/
        :return:
        """

        @asyncio.coroutine
        def go():
            data = {
                'login': 'quangbinh',
                'password1': 'baogavn',
                'password2': 'baogavn'
            }

            # data = yield from self.create_sample_user(data)
            url = yield from self.create_server()

            headers = {'accept': 'application/json'}
            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                r = yield from session.post(url=url + '/users/',
                                            data=json_util.dumps(data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('login', r, text)
                self.assertEqual(r['login'], 'quangbinh')

        self.loop.run_until_complete(go())


    def test_create_new_user_unsucess(self):
        """
        POST /users/
        :return:
        """

        @asyncio.coroutine
        def go():
            data = {
                'login': 'quangbinh',
                'password1': 'baogavn',
                'password2': ''
            }

            # data = yield from self.create_sample_user(data)
            url = yield from self.create_server()

            headers = {'accept': 'application/json'}
            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                r = yield from session.post(url=url + '/users/',
                                            data=json_util.dumps(data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('error', r, text)

        self.loop.run_until_complete(go())

    def test_login_sucess(self):
        """
        POST /login/
        :return:
        """

        @asyncio.coroutine
        def go():
            data = {
                'login': 'quangbinh',
                'password1': 'baogavn',
                'password2': 'baogavn'
            }

            # data = yield from self.create_sample_user(data)
            url = yield from self.create_server()
            headers = {'accept': 'application/json'}
            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                # Create new user
                r = yield from session.post(url=url + '/users/',
                                            data=json_util.dumps(data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('login', r, text)
                self.assertEqual(r['login'], 'quangbinh')

                data1 = {
                    'login': 'quangbinh',
                    'password': 'baogavn'
                }
                # LogIn
                r = yield from session.post(url=url + '/login/',
                                            data=json_util.dumps(data1))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('ok', r, text)
                self.assertIn('user', r, text)
                self.assertEqual(r['ok'], 1)
                self.assertEqual(r['user']['login'], 'quangbinh')
                self.assertIsNone(r['user'].get('password'))

        self.loop.run_until_complete(go())

    def test_login_unsucess(self):
        """
        POST /login/
        :return:
        """
        @asyncio.coroutine
        def go():
            data = {
                'login': 'quangbinh',
                'password1': 'baogavn',
                'password2': 'baogavn'
            }

            # data = yield from self.create_sample_user(data)
            url = yield from self.create_server()
            headers = {'accept': 'application/json'}
            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                # Create new user
                r = yield from session.post(url=url + '/users/',
                                            data=json_util.dumps(data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('login', r, text)
                self.assertEqual(r['login'], 'quangbinh', text)

                data1 = {
                    'login': 'quangbinh',
                    'password': '   '
                }

                # LogIn with error
                r = yield from session.post(url=url + '/login/',
                                            data=json_util.dumps(data1))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('error', r, text)

        self.loop.run_until_complete(go())

    def test_logout_sucess(self):
        """
        POST /logout/
        :return:
        """

        @asyncio.coroutine
        def go():
            data = {
                'login': 'quangbinh',
                'password1': 'baogavn',
                'password2': 'baogavn'
            }

            # data = yield from self.create_sample_user(data)
            url = yield from self.create_server()
            headers = {'accept': 'application/json'}
            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                # Create new user
                r = yield from session.post(url=url + '/users/',
                                            data=json_util.dumps(data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('login', r, text)
                self.assertEqual(r['login'], 'quangbinh')

                data1 = {
                    'login': 'quangbinh',
                    'password': 'baogavn'
                }

                # LogIn
                r = yield from session.post(url=url + '/login/',
                                            data=json_util.dumps(data1))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('ok', r, text)
                self.assertIn('user', r, text)
                self.assertEqual(r['ok'], 1, text)
                self.assertEqual(r['user']['login'], 'quangbinh', text)
                self.assertNotIn('password', r['user'], text)

                # LogOut
                r = yield from session.post(url=url + '/logout/')
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('ok', r, text)
                # self.assertIn('user', r, text)
                self.assertEqual(r['ok'], 1, text)
                # self.assertEqual(r['user']['login'], 'quangbinh')
                # self.assertIsNone(r['user'].get('password'))

        self.loop.run_until_complete(go())

    def test_logout_unsucess(self):
        """
        POST /logout/
        :return:
        """

        @asyncio.coroutine
        def go():
            data = {
                'login': 'quangbinh',
                'password1': 'baogavn',
                'password2': 'baogavn'
            }

            # data = yield from self.create_sample_user(data)
            url = yield from self.create_server()
            headers = {'accept': 'application/json'}
            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                # Create new user
                r = yield from session.post(url=url + '/users/',
                                            data=json_util.dumps(data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('login', r, text)
                self.assertEqual(r['login'], 'quangbinh')

                # data1 = {
                #     'login': 'quangbinh',
                #     'password': 'baogavn'
                # }

                # # LogIn
                # r = yield from session.post(url=url + '/login/',
                #                             data=json_util.dumps(data1))
                # text = yield from r.text()
                # self.assertEqual(200, r.status, text)
                # r = yield from r.json(loads=json_util.loads)
                # self.assertIn('ok', r, text)
                # self.assertIn('user', r, text)
                # self.assertEqual(r['ok'], 1, text)
                # self.assertEqual(r['user']['login'], 'quangbinh', text)
                # self.assertNotIn('password', r['user'], text)

                # LogOut
                r = yield from session.post(url=url + '/logout/')
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('error', r, text)
                self.assertIn("Login Requirement!!!", r['error'], text)

        self.loop.run_until_complete(go())

    def test_get_a_user(self):
        """
        GET `/users/{login}/`
        :return:
        """
        @asyncio.coroutine
        def go():
            data = {
                'login': 'quangbinh',
                'password1': 'baogavn',
                'password2': 'baogavn'
            }

            # data = yield from self.create_sample_user(data)
            url = yield from self.create_server()
            headers = {'accept': 'application/json'}

            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                r = yield from session.post(url=url + '/users/',
                                            data=json_util.dumps(data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('login', r, text)
                self.assertEqual(r['login'], 'quangbinh', text)

                data1 = {
                    'login': 'quangbinh',
                    'password': 'baogavn'
                }
                # ## LogIn GET `/login/`
                # r = yield from session.post(url=url+'/login/',
                #                             data=json_util.dumps(data1))
                # text = yield from r.text()
                # self.assertEqual(200, r.status, text)
                # r = yield from r.json(loads=json_util.loads)
                # self.assertIn('ok', r, text)
                # self.assertIn('user', r, text)
                # self.assertEqual(r['ok'], 1)
                # self.assertEqual(r['user']['login'], 'quangbinh')
                # self.assertIsNone(r['user'].get('password'))

                # GET `/users/{login}/`
                r = yield from session.get(url=url + '/users/quangbinh/',
                                           data=json_util.dumps(data1))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIn('login', r, text)
                self.assertEqual(r['login'], 'quangbinh', text)

        self.loop.run_until_complete(go())
