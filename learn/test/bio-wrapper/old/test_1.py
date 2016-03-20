def handleError(function):
    def handleProblems(self):
        try:
            function(self)
        except Exception as e:
            print(e, "daskjfalsjkf")

    return handleProblems

class A(object):
    @handleError
    def example(self):
        raise KeyError("Boom!")

a = A()
a.example()