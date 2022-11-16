class Type:

    def __init__(self, data_type, length=0):
        self.type = data_type,
        self.length = length

    def check(self, data):
        excluded_types = [bool, str, list, dict]
        return isinstance(data, self.type) and \
            len(list(str(data))) <= self.length if self.type not in excluded_types else True
