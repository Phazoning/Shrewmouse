from Error import Error


class NoCollectionsError(Error):

    def __init__(self,  message="Database holds no collections, aborted"):
        self.message = message
        super().__init__(self.message)