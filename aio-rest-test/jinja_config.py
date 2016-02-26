# from jinja2 import Environment
import aiohttp_jinja2
import jinja2
# env = Environment(**options)
# env.globals.update({
#     'static': staticfiles_storage.url,
#     'url': reverse,
#     'get_messages': messages.get_messages,
# })




def setup(app):
    env = aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('templates'))
    # env.globals.update({
    #     ''
    # })
    return env