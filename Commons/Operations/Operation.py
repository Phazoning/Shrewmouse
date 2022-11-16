class Operation:

    def __init__(self, name, operator_function):
        self.name = name
        self.func = operator_function

    def operation(self, *args):
        return self.func(*args)
