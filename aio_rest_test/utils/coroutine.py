import asyncio

DEBUG = False


def handle_errors(func):
    @asyncio.coroutine
    def wrapped(s):
        try:
            r = yield from func(s)
            return r
        except Exception as e:
            if DEBUG:
                raise e

            message = "%s: %s" % (type(e).__name__, e)
            return s.response({'error': message})

    return wrapped
