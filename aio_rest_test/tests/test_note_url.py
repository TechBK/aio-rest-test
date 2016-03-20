import asyncio
import unittest
from aio_rest_test.service import init
import socket
import aiohttp
from bson import json_util


class TestNoteUrl(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.user_data = {
            'login': 'quangbinh',
            'password1': 'baogavn',
            'password2': 'baogavn'
        }
        self.login_data = {
            'login': 'quangbinh',
            'password': 'baogavn'
        }
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
    def create_server_and_user_and_login(self, session):
        port = self.find_unused_port()
        self.srv, self.app, self.handler = \
            yield from init(self.loop, port=port, test=True)

        url = "http://127.0.0.1:{}".format(port)

        # POST /users/
        r = yield from session.post(url=url + '/users/',
                                    data=json_util.dumps(self.user_data))
        text = yield from r.text()
        self.assertEqual(200, r.status, text)
        r = yield from r.json(loads=json_util.loads)
        self.assertIn('login', r, text)
        self.assertEqual(r['login'], 'quangbinh')

        # POST /login/
        r = yield from session.post(url=url + '/login/',
                                    data=json_util.dumps(self.login_data))
        text = yield from r.text()
        self.assertEqual(200, r.status, text)
        r = yield from r.json(loads=json_util.loads)
        self.assertIn('ok', r, text)
        self.assertIn('user', r, text)
        self.assertEqual(r['ok'], 1)
        self.assertEqual(r['user']['login'], 'quangbinh')
        self.assertIsNone(r['user'].get('password'))
        return url

    def test_create_new_note_of_user_sucess(self):
        """
        POST /notes/
        :return:
        """

        @asyncio.coroutine
        def go():
            # data = yield from self.create_sample_user(data)
            headers = {'accept': 'application/json'}
            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                url = yield from self.create_server_and_user_and_login(session)

                # POST /notes/
                note_data = {
                    'text': 'note test',
                    'is_public': True,
                    'tags': ['abc', 'abcdf']
                }
                r = yield from session.post(url=url + '/notes/',
                                            data=json_util.dumps(note_data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIsInstance(r, list, text)
                self.assertEqual(len(r), 1, text)
                r = r[0]
                self.assertIn('_id', r, text)
                self.assertIn('users', r, text)
                self.assertIn('tags', r, text)
                self.assertIn('text', r, text)
                self.assertIn('is_public', r, text)
                self.assertEqual(r['text'], note_data['text'], text)
                self.assertEqual(r['is_public'], True, text)
                self.assertEqual(r['users'], ['quangbinh'], text)
                self.assertEqual(r['tags'], note_data['tags'], text)

        self.loop.run_until_complete(go())

    def test_view_note_of_user_sucess(self):
        """
        GET '/users/{login:\w+}/notes/'
        :return:
        """

        @asyncio.coroutine
        def go():
            # data = yield from self.create_sample_user(data)
            headers = {'accept': 'application/json'}
            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                url = yield from self.create_server_and_user_and_login(session)

                # POST /notes/
                note_data = [{
                        'text': 'note test 1',
                        'is_public': True,
                        'tags': ['abc', 'abcdf']
                    },
                    {
                        'text': 'note test 2',
                        'is_public': False,
                        'tags': ['abc', 'abcdfe']
                    }]
                r = yield from session.post(url=url + '/notes/',
                                            data=json_util.dumps(note_data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIsInstance(r, list, text)
                self.assertEqual(len(r), 2, text)
                if r[0]['text'] == 'note test 1':
                    note1, note2 = r
                else:
                    note2, note1 = r
                self.assertIn('_id', note1, text)
                self.assertIn('users', note1, text)
                self.assertIn('tags', note1, text)
                self.assertIn('text', note1, text)
                self.assertIn('is_public', note1, text)
                self.assertEqual(note1['text'], 'note test 1', text)
                self.assertEqual(note1['is_public'], True, text)
                self.assertListEqual(note1['users'], ['quangbinh'], text)
                self.assertListEqual(note1['tags'], ['abc', 'abcdf'], text)

                self.assertIn('_id', note2, text)
                self.assertIn('users', note2, text)
                self.assertIn('tags', note2, text)
                self.assertIn('text', note2, text)
                self.assertIn('is_public', note1, text)
                self.assertEqual(note2['text'], 'note test 2', text)
                self.assertEqual(note2['is_public'], False, text)
                self.assertListEqual(note2['users'], ['quangbinh'], text)
                self.assertListEqual(note2['tags'], ['abc', 'abcdfe'], text)


                # GET '/users/{login:\w+}/notes/'
                r = yield from session.get(url=url + '/users/quangbinh/notes/')
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIsInstance(r, list, text)
                self.assertEqual(len(r), 2, text)
                if r[0]['text'] == 'note test 1':
                    note1, note2 = r
                else:
                    note2, note1 = r
                self.assertIn('_id', note1, text)
                self.assertIn('users', note1, text)
                self.assertIn('tags', note1, text)
                self.assertIn('text', note1, text)
                self.assertIn('is_public', note1, text)
                self.assertEqual(note1['text'], 'note test 1', text)
                self.assertEqual(note1['is_public'], True, text)
                self.assertListEqual(note1['users'], ['quangbinh'], text)
                self.assertListEqual(note1['tags'], ['abc', 'abcdf'], text)

                self.assertIn('_id', note2, text)
                self.assertIn('users', note2, text)
                self.assertIn('tags', note2, text)
                self.assertIn('text', note2, text)
                self.assertIn('is_public', note1, text)
                self.assertEqual(note2['text'], 'note test 2', text)
                self.assertEqual(note2['is_public'], False, text)
                self.assertListEqual(note2['users'], ['quangbinh'], text)
                self.assertListEqual(note2['tags'], ['abc', 'abcdfe'], text)

        self.loop.run_until_complete(go())

    def test_edit_note_of_user_sucess(self):
        """
        # PUT '/notes/{}/'
        :return:
        """

        @asyncio.coroutine
        def go():
            # data = yield from self.create_sample_user(data)
            headers = {'accept': 'application/json'}
            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                url = yield from self.create_server_and_user_and_login(session)

                # POST /notes/
                note_data = {
                    'text': 'note test',
                    'is_public': True,
                    'tags': ['abc', 'abcdf']
                }
                r = yield from session.post(url=url + '/notes/',
                                            data=json_util.dumps(note_data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIsInstance(r, list, text)
                self.assertEqual(len(r), 1, text)
                r = r[0]
                self.assertIn('_id', r, text)
                self.assertIn('users', r, text)
                self.assertIn('tags', r, text)
                self.assertIn('text', r, text)
                self.assertIn('is_public', r, text)
                self.assertEqual(r['text'], note_data['text'], text)
                self.assertEqual(r['is_public'], True, text)
                self.assertEqual(r['users'], ['quangbinh'], text)
                self.assertEqual(r['tags'], note_data['tags'], text)

                # PUT '/notes/{}/'
                _id = str(r['_id'])
                edit_note = {
                    'text': 'note test 1',
                    'is_public': False,
                    'tags': ['abc', 'abcdf', 'klm']
                }
                # assert 0, r
                r = yield from session.put(url=url + '/notes/{}/'.format(_id),
                                           data=json_util.dumps(edit_note))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                # self.assertIsInstance(r, list, text)
                # self.assertEqual(len(r), 1, text)
                # r = r[0]
                self.assertIn('_id', r, text)
                self.assertIn('users', r, text)
                self.assertIn('tags', r, text)
                self.assertIn('text', r, text)
                self.assertIn('is_public', r, text)
                self.assertEqual(r['text'], 'note test 1', text)
                self.assertEqual(r['is_public'], False, text)
                self.assertEqual(r['users'], ['quangbinh'], text)
                self.assertEqual(r['tags'], edit_note['tags'], text)

        self.loop.run_until_complete(go())


    def test_view_note_of_tag_sucess(self):
        """
        GET '/tags/{text:\w+}/'
        :return:
        """

        @asyncio.coroutine
        def go():
            # data = yield from self.create_sample_user(data)
            headers = {'accept': 'application/json'}
            with aiohttp.ClientSession(loop=self.loop,
                                       headers=headers) as session:
                url = yield from self.create_server_and_user_and_login(session)

                # POST /notes/
                note_data = [{
                        'text': 'note test 1',
                        'is_public': True,
                        'tags': ['abc', 'abcdf']
                    },
                    {
                        'text': 'note test 2',
                        'is_public': False,
                        'tags': ['abc', 'abcdfe']
                    }]
                r = yield from session.post(url=url + '/notes/',
                                            data=json_util.dumps(note_data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIsInstance(r, list, text)
                self.assertEqual(len(r), 2, text)
                if r[0]['text'] == 'note test 1':
                    note1, note2 = r
                else:
                    note2, note1 = r
                self.assertIn('_id', note1, text)
                self.assertIn('users', note1, text)
                self.assertIn('tags', note1, text)
                self.assertIn('text', note1, text)
                self.assertIn('is_public', note1, text)
                self.assertEqual(note1['text'], 'note test 1', text)
                self.assertEqual(note1['is_public'], True, text)
                self.assertListEqual(note1['users'], ['quangbinh'], text)
                self.assertListEqual(note1['tags'], ['abc', 'abcdf'], text)

                self.assertIn('_id', note2, text)
                self.assertIn('users', note2, text)
                self.assertIn('tags', note2, text)
                self.assertIn('text', note2, text)
                self.assertIn('is_public', note1, text)
                self.assertEqual(note2['text'], 'note test 2', text)
                self.assertEqual(note2['is_public'], False, text)
                self.assertListEqual(note2['users'], ['quangbinh'], text)
                self.assertListEqual(note2['tags'], ['abc', 'abcdfe'], text)


                # GET /tags/{}/

                tags_data = 'abc'
                r = yield from session.get(url=url + '/tags/{}/'.format(tags_data))
                text = yield from r.text()
                self.assertEqual(200, r.status, text)
                r = yield from r.json(loads=json_util.loads)
                self.assertIsInstance(r, list, text)
                self.assertEqual(len(r), 2, text)
                if r[0]['text'] == 'note test 1':
                    note1, note2 = r
                else:
                    note2, note1 = r
                self.assertIn('_id', note1, text)
                self.assertIn('users', note1, text)
                self.assertIn('tags', note1, text)
                self.assertIn('text', note1, text)
                self.assertIn('is_public', note1, text)
                self.assertEqual(note1['text'], 'note test 1', text)
                self.assertEqual(note1['is_public'], True, text)
                self.assertListEqual(note1['users'], ['quangbinh'], text)
                self.assertListEqual(note1['tags'], ['abc', 'abcdf'], text)

                self.assertIn('_id', note2, text)
                self.assertIn('users', note2, text)
                self.assertIn('tags', note2, text)
                self.assertIn('text', note2, text)
                self.assertIn('is_public', note1, text)
                self.assertEqual(note2['text'], 'note test 2', text)
                self.assertEqual(note2['is_public'], False, text)
                self.assertListEqual(note2['users'], ['quangbinh'], text)
                self.assertListEqual(note2['tags'], ['abc', 'abcdfe'], text)


        self.loop.run_until_complete(go())
