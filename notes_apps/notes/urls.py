from .views import *
from aio_framework.utils.urls import URL

urls = [
    # Get and Put note || 1 PUT OK
    URL('GET', '/notes/{id:\w+}/', NoteView, name='note-detail-get'),
    # Get and Put note || 1 PUT OK
    URL('PUT', '/notes/{id:\w+}/', NoteView, name='note-detail-put'),
    # Get notes User.login = login || 1 GET OK
    URL('GET', '/users/{login:\w+}/notes/', NotesOfUser, name='notes_of_user'),
    # Get, Post Note of Current User. || 1 POST OK
    URL('GET', '/notes/', NotesView, name='notes-get'),
    # Get, Post Note of Current User. || 1 POST OK
    URL('POST', '/notes/', NotesView, name='notes-post'),
    # View a User Info, Put new info to update || 2 POST ok
    URL('GET', '/tags/{text:\w+}/', NotesOfTag, name='notes_of_tag-get'),
    # View a User Info, Put new info to update || 2 POST ok
    URL('PUT', '/tags/{text:\w+}/', NotesOfTag, name='notes_of_tag-put')
]


# def urls(app):
#     # Get and Put note || 1 PUT OK
#     app.router.add_route('GET', '/notes/{id:\w+}/', NoteView,
#                          name='note-detail')
#
#     # Get and Put note || 1 PUT OK
#     app.router.add_route('PUT', '/notes/{id:\w+}/', NoteView,
#                          name='note-detail2')
#
#     # Get notes User.login = login || 1 GET OK
#     app.router.add_route('GET', '/users/{login:\w+}/notes/', NotesOfUser,
#                          name='notes_of_user')
#
#
#     # app.router.add_route('*', '/notes/{login:\w+}/{id:\w+}/',
#     # notes.NoteView, name='note-detail')
#
#     # Get, Post Note of Current User. || 1 POST OK
#     app.router.add_route('GET', '/notes/', NotesView,
#                          name='notes')
#
#     # Get, Post Note of Current User. || 1 POST OK
#     app.router.add_route('POST', '/notes/', NotesView,
#                          name='notes1')
#
#
#     # View a User Info, Put new info to update || 2 POST ok
#     app.router.add_route('GET', '/tags/{text:\w+}/', NotesOfTag,
#                          name='notes_of_tag')
#
#     # View a User Info, Put new info to update || 2 POST ok
#     app.router.add_route('PUT', '/tags/{text:\w+}/', NotesOfTag,
#                          name='notes_of_tag2')



