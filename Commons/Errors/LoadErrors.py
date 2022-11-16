from Error import Error


class IncorrectJSONLoadException(Error):
    """
    Exception raised when a JSON isn't referred as a string depicting the path to the file (e.g., if it were to be
    given as an IOWrapper
    """

    def __init__(self, value, message="A JSON file must be given in a string, not in any other form or wrapper"):
        self.value = value
        self.message = message
        super().__init__(self.message)