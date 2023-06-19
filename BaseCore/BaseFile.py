import json
from Collection import Collection
from Commons.Types.TypeInstances import references as type_ref
import Commons.Errors.FormatErrors as FErrors
import Commons.Errors.LoadErrors as LErrors


class BaseFile:

    def __init__(self, file: str):
        try:
            assert(str(file) == file)
            self.file = file
        except AssertionError:
            raise LErrors.IncorrectJSONLoadException

        if json.load(open(file))["collections"]:
            self.collections = [*json.load(open(file))["collections"].values()]
        else:
            raise FErrors.NoCollectionsError

    def get_collection(self, name: str) -> Collection or None:
        try:
            return Collection([e for e in self.collections if e["name"] == name][0], self.file)
        except KeyError:
            print(f"Collection {name} not found")

    def create_collection(self, name: str, prototype: dict = {}) -> None:
        if not name:
            print("A collection name is needed")
        elif name in [e["name"] for e in self.collections]:
            print(f"Collection {name} already exists, please choose another one")
        else:
            col = {"name": name}
            if prototype and [True for e in [*prototype]] == [e in [*type_ref] for e in [*prototype.values()]]:
                col["prototype"] = prototype
            else:
                print(f"Types for fields {[e for e in [*prototype.values()] if e not in [*type_ref]]}, "
                      f"unable to create prototype")

            self.collections.append(col)
            with open(self.file, "rw") as jsonfile:
                json_data = json.load(jsonfile)
                json_data["collections"] = self.collections
                json.dump(json_data, jsonfile)

    def delete_collection(self, name: str):
        if name in [e["name"] for e in self.collections]:
            self.collections.pop(self.collections.index(name))
            with open(self.file, "rw") as jsonfile:
                json_data = json.load(jsonfile)
                json_data["collections"] = self.collections
                json.dump(json_data, jsonfile)
        else:
            print(f"Error, there is no collection with name {name}")

