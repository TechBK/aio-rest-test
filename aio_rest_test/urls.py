from aio_rest_test import notes, users


def urls(app):
    # || 2 POST ok |
    app.router.add_route('POST', '/login/', users.LoginView, name='login')

    # || 2 POST ok |
    app.router.add_route('POST', '/logout/', users.LogoutView, name='logout')

    # Post New User! Get Users Info || Sigin Here || 2 POST ok
    app.router.add_route('POST', '/users/', users.UsersView, name='users')

    # Post New User! Get Users Info || Sigin Here || 2 POST ok
    app.router.add_route('GET', '/users/', users.UsersView, name='users2')

    # View a User Info, Put new info to update || 2 POST ok
    app.router.add_route('PUT', '/users/{login:\w+}/', users.UserView,
                         name='user-detail')
    # View a User Info, Put new info to update || 2 POST ok
    app.router.add_route('GET', '/users/{login:\w+}/', users.UserView,
                         name='user-detail2')

    # Get and Put note || 1 PUT OK
    app.router.add_route('GET', '/notes/{id:\w+}/', notes.NoteView,
                         name='note-detail')

    # Get and Put note || 1 PUT OK
    app.router.add_route('PUT', '/notes/{id:\w+}/', notes.NoteView,
                         name='note-detail2')

    # Get notes User.login = login || 1 GET OK
    app.router.add_route('GET', '/users/{login:\w+}/notes/', notes.NotesOfUser,
                         name='notes_of_user')


    # app.router.add_route('*', '/notes/{login:\w+}/{id:\w+}/',
    # notes.NoteView, name='note-detail')

    # Get, Post Note of Current User. || 1 POST OK
    app.router.add_route('GET', '/notes/', notes.NotesView,
                         name='notes')

    # Get, Post Note of Current User. || 1 POST OK
    app.router.add_route('POST', '/notes/', notes.NotesView,
                         name='notes1')


    # View a User Info, Put new info to update || 2 POST ok
    app.router.add_route('GET', '/tags/{text:\w+}/', notes.NotesOfTag,
                         name='notes_of_tag')

    # View a User Info, Put new info to update || 2 POST ok
    app.router.add_route('PUT', '/tags/{text:\w+}/', notes.NotesOfTag,
                         name='notes_of_tag2')