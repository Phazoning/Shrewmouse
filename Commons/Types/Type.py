class Type:

    def __init__(self, data_type):
        self.type = data_type

    def check(self, data):
        return isinstance(data, self.type)

