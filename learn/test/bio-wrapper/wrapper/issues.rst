======
Issues
======

.. contents::

Before:
======
- Url commit: https://github.com/cloudcomputinghust/bio-wrapper/commit/{commit_id}

Issue 1: cant handle exception
==============================
- Time: 01/1/2016
- Type: code
- File: ./wrapper/handlers.py
- Description: None
- Status: Done
- Traceback:
- Commit have issue: 64190d2bd7ff8916a398909fdd14747a1bde3552
- Commit fix: f19e7a1c1bbf9f8cb3a8d2a9643a7305e18f2106


Issue 2: No module named 'keystoneclient'
=========================================
- Time: 06/1/2016
- Type: env
- File: ./old/test.py
- Fix: sudo pip3 install python-keystoneclient
- Description: None
- Status: Done
- Traceback::

    Traceback (most recent call last):
      File "/usr/local/lib/python3.4/dist-packages/swiftclient/client.py", line 369, in _import_keystone_client
        from keystoneclient.v2_0 import client as ksclient
    ImportError: No module named 'keystoneclient'

- Commit have issue: f19e7a1c1bbf9f8cb3a8d2a9643a7305e18f2106
- Commit fix:


Issue 3: I dont understand thi bug :v
=====================================
- Time: 06/1/2016
- Type: env, config
- File: ./old/test.py
- Fix:
- Description: None
- Status: Done
- Traceback::

    /usr/local/lib/python3.4/dist-packages/keystoneclient/service_catalog.py:198: UserWarning: Providing attr without filter_value to get_urls() is deprecated as of the 1.7.0 release and may be removed in the 2.0.0 release. Either both should be provided or neither should be provided.
    'Providing attr without filter_value to get_urls() is '

- Commit have issue: f19e7a1c1bbf9f8cb3a8d2a9643a7305e18f2106
- Commit fix:



Issue 4: Cant check out statement of swift connect, when create swift mangager
==============================================================================
- Time: 07/1/2016
- Type: code
- File: ./managers.py, method: job.runprocess
- Fix:
- Description: Khi tao job, thong tin swift sai ko bi bao loi.
- Status: Done
- Traceback::

    Traceback (most recent call last):
      File "/usr/local/lib/python3.4/dist-packages/aiohttp/server.py", line 272, in start
        yield from self.handle_request(message, payload)
      File "/usr/local/lib/python3.4/dist-packages/aiohttp/web.py", line 85, in handle_request
        resp = yield from handler(request)
      File "/home/techbk/PycharmProjects/bio-wrapper/wrapper/handlers.py", line 119, in job
        out, error = yield from job.process
      File "/usr/lib/python3.4/asyncio/futures.py", line 388, in __iter__
        return self.result()  # May raise too.
      File "/usr/lib/python3.4/asyncio/futures.py", line 275, in result
        raise self._exception
      File "/usr/lib/python3.4/asyncio/tasks.py", line 236, in _step
        result = coro.send(value)
      File "/home/techbk/PycharmProjects/bio-wrapper/wrapper/managers.py", line 130, in run_process
        raise e
      File "/home/techbk/PycharmProjects/bio-wrapper/wrapper/managers.py", line 126, in run_process
        yield from self.swift.put_data(out)
      File "/usr/lib/python3.4/asyncio/coroutines.py", line 141, in coro
        res = func(*args, **kw)
      File "/home/techbk/PycharmProjects/bio-wrapper/wrapper/managers.py", line 70, in put_data
        content_type='text/plain')
      File "/usr/local/lib/python3.4/dist-packages/swiftclient/client.py", line 1551, in put_object
        response_dict=response_dict)
      File "/usr/local/lib/python3.4/dist-packages/swiftclient/client.py", line 1425, in _retry
        service_token=self.service_token, **kwargs)
      File "/usr/local/lib/python3.4/dist-packages/swiftclient/client.py", line 1141, in put_object
        http_response_content=body)
    swiftclient.exceptions.ClientException: Object PUT failed: http://192.168.145.132:8080/v1/AUTH_3cae5d54604b4473bb1274ec18a1d686/dsafuashfio/1 404 Not Found  [first 60 chars of response] b'<html><h1>Not Found</h1><p>The resource could not be found.<'

- Commit have issue: eed95114e7134da66047e578b88485134790dac4
- Commit fix: