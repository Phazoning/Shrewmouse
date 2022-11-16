import json
import Commons.Errors.FormatErrors as FErrors
import Commons.Errors.LoadErrors as LErrors


class BaseFile:

    def __init__(self, file):
        try:
            assert(str(file) == file)
            self.file = json.load(open(file, 'rw'))
        except AssertionError:
            raise LErrors.IncorrectJSONLoadException

        if self.file["collections"]:
            self.collections = self.file["collections"].keys()
        else:
            raise FErrors.NoCollectionsError

        if self.file["users"]:
            self.users = self.file["users"]
        else:
            print("No users detected, no requirements applied on accessing db")
            self.users = False

