# from aio_rest_test import notes, users


def urls(app):
    # || 2 POST ok |
    app.router.add_route('POST', '/authenticate/', users.LoginView, name='login')

    # || 2 POST ok |
    # app.router.add_route('POST', '/logout/', users.LogoutView, name='logout')

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

