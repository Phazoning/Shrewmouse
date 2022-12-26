from ..Commons.Types.TypeInstances import references as type_ref
import json
from ..Commons.Operations.OperatorHandler import OperatorHandler as Op
from ..Commons.Errors.DBInputErrors import *
from Aggregator import Aggregator


class Collection:

    def __init__(self, file):
        self.file = file
        self.col = []
        self.prototype = json.load(open(self.file, 'r'))["prototype"]
        self.op = Op()

    def __choose(self, parameters, chk_object):
        hits = [True for e in chk_object.keys if "$" in parameters[e].keys[0] and
                self.op.operate(parameters[e].keys[0], parameters[e].values[0], chk_object[e])
                or chk_object[e] == parameters[e]]
        if len(hits) == len(chk_object.keys):
            return True
        else:
            return False

    def find(self, parameters):

        with json.load(open(self.file, "r"))["data"] as collection_data:
            self.col = [e for e in collection_data if self.__choose(parameters, e) or parameters == {}]

    def insert(self, ins_object):

        if [True for e in ins_object.keys] == [type_ref[self.prototype[e]].check(ins_object[e]) for e in ins_object.keys]:
            with json.load(open(self.file, "r")) as collection_dict:
                collection_dict["data"].append(ins_object)
                json.dump(collection_dict, open(self.file, "w"))
        else:
            raise InvalidObjectParameters

    def delete(self, parameters):

        self.find(parameters)
        with json.load(open(self.file, "r")) as collection_dict:
            collection_dict["data"] = [e for e in collection_dict["data"] if e not in self.col]
            json.dump(collection_dict, open(self.file, "w"))
        self.col = []

    def modify(self, search_parameters, change_parameters):

        self.find(search_parameters)
        with json.load(open(self.file, "r")) as collection_dict:
            for e in collection_dict["data"]:
                if e in self.col:
                    for j in e.keys:
                        e[j] = change_parameters[j]
            json.dump(collection_dict, open(self.file, "w"))
        self.col = []

    def aggregate(self, pipelines):
        if pipelines[0].keys()[0] != "$find":
            self.find({})

        aggregator = Aggregator(self.col)

        aggregator.aggregate(pipelines)
        self.col = aggregator.col

