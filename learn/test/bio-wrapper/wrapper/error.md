Error handling request
Traceback (most recent call last):
  File "/usr/local/lib/python3.4/dist-packages/aiohttp/server.py", line 272, in start
    yield from self.handle_request(message, payload)
  File "/usr/local/lib/python3.4/dist-packages/aiohttp/web.py", line 85, in handle_request
    resp = yield from handler(request)
  File "/usr/lib/python3.4/asyncio/coroutines.py", line 143, in coro
    res = yield from res
  File "/home/techbk/PycharmProjects/bio-wrapper/wrapper/handlers.py", line 118, in job
    raise KeyError("sdjkfas")
KeyError: 'sdjkfas'
I have same problem.
example code:
```python
def handle_errors(func):
    def wrapped(request):
        data = {}
        try:
            data = func(request)
        except Exception as e:
            print('Pha 1: %s', e)
            data = {
                'status': False,
                'error_message': str(e)
            }
            data = web.Response(body=json.dumps(data).encode('utf-8'))
        finally:
            return data
    return wrapped

@handle_errors
def index(request):
    raise ExceptionError('error')
```

my server dont return data = { 'status': False,'error_message': str(e)}.
it response 500 Internal Server Error with Traceback:

```
Error handling request
Traceback (most recent call last):
  File "/usr/local/lib/python3.4/dist-packages/aiohttp/server.py", line 272, in start
    yield from self.handle_request(message, payload)
  File "/usr/local/lib/python3.4/dist-packages/aiohttp/web.py", line 85, in handle_request
    resp = yield from handler(request)
  File "/usr/lib/python3.4/asyncio/coroutines.py", line 143, in coro
    res = yield from res
  File "...................................................../handlers.py", line 118, in job
    raise ExceptionError('error')
ExceptionError: 'error'
```