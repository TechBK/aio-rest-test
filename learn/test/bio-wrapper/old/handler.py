__author__ = 'techbk'


class Handler(object):
    _command = {}

    def handle(self, request):
        """get command from request, goi command"""

        do_something = request.match_info.get('do_something')
        return self._command.get(do_something, self._error)(request)

    def _error(self, request):
        """return thong bao loi"""
        pass


class TasksHandler(Handler):
    def __init__(self):
        """
        Dinh nghia cac function
        """
        self._command = {
            "list": self._list,
            "run": self._run
        }

    def _list(self, request):
        """
        return list of task + status cua task
        """
        pass

    def _run(self, request):
        """
        run a task + add task into Tasks
        """
        pass

class ConfigHandler(Handler):
    def __init__(self):
        self._command = {
            "settup": self._settup,
            "show": self._show
        }

    def _settup(self, request):
        """
        update config
        """
        pass

    def _show(self, request):
        """
        show config
        """
        pass


class TaskHandler(Handler):
    def __init__(self):
        self._command = {
            'status': self._status,
            'output': self._output
        }

    def _status(self, request):
        """
        return status
        """
        pass

    def _output(self, request):
        """
        return ket qua cua task
        """
        pass
