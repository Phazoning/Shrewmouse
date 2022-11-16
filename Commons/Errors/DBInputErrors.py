from Error import Error


class InvalidObjectParameters(Error):

    def __init__(self, msg="Object doesn't match with collection prototype"):
        self.msg = msg
        super.__init__(self.msg)

