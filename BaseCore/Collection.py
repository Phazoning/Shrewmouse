import json
from ..Commons.Types.TypeInstances import references as type_ref
from ..Commons.Operations.OperatorHandler import OperatorHandler as Op
from ..Commons.Errors.DBInputErrors import *
from ..Commons.Auxiliary.AuxiliaryMethods import deep_dict_search as dds
from Aggregator import Aggregator
from pprint import pprint


class Collection:

    def __init__(self, collection_file: str, db_file: str) -> None:
        """
        !!!Constructor method

        :param collection_file: String with the path to the file with the actual data of the object
        :param db_file: String with the database data. Needed for the aggregator
        """
        self.file: str = collection_file
        self.db: str = db_file
        self.__col: list[dict] = []
        self.prototype: dict = json.load(open(self.file, 'r'))["prototype"] \
            if json.load(open(self.file, 'r'))["prototype"] else {}
        self.op: Op = Op()

    def __choose(self, parameters: dict, chk_object: dict) -> bool:
        """
        Given a set of parameters, checks if the corresponding on a dictionary fulfills the conditions

        :param parameters: Dictionary with the set of parameters
        :param chk_object: Object to be checked
        :return: Boolean if the desired value/s have been found or not
        """
        ret = False
        for e in [*parameters]:
            ret = True if "$" in [*parameters[e]][0] \
                and self.op.operate([*parameters[e]][0], [*parameters[e].values()][0], dds(chk_object, e)) \
                or dds(chk_object, e) == parameters[e] else False

        return ret

    def find(self, parameters: dict) -> None:
        """
        Given a dictionary with parameters turns the inner property with the data into the requested items

        :param parameters: Dictionary with the parameters to search the collection
        :return: None, changes applied to inner property
        """
        try:
            with json.load(open(self.file, "r"))["data"] as collection_data:
                self.__col = [e for e in collection_data if self.__choose(parameters, e) or parameters == {}]
        except KeyError:
            print("One or more keys weren't found within parameters, please check them and try again")

    def insert(self, ins_object: dict) -> None:
        """
        Method to insert a new object in the collection. For coherency reasons it has its own checks against a prototype
        that says how the datatypes and fields in a collection work. If the collection were to be empty, it creates
        the prototype using the registry to be inserted

        :param ins_object: The object to be inserted
        :return: None, result stored in the json
        """
        with json.load(open(self.file, "rw+")) as collection_file:
            if not self.prototype:
                proto = {}
                data_comp = {int: "Int", float: "Float", "String": str, "List": list, "Boolean": bool, "Object": dict}
                for e in [*ins_object]:
                    with ins_object[e] as data:
                        proto[e] = [j for j in [*data_comp.values()] if isinstance(data, j)][0]

                collection_file["prototype"] = proto
                self.prototype = proto

            if [True for e in [*ins_object]
                    if type_ref[collection_file["prototype"][e]](ins_object[e])] == [True for e in [*ins_object]]:

                collection_file["data"].append(ins_object)
            json.dump(self.file, collection_file)

    def delete(self, parameters: dict) -> None:
        """
        This method deletes from the data in a collection all registries that meet a certain criteria

        :param parameters: The criteria the objects to be deleted meet
        :return: None, the resulting data is written into the collection file
        """

        self.find(parameters)
        with json.load(open(self.file, "r")) as collection_dict:
            collection_dict["data"] = [e for e in collection_dict["data"] if e not in self.__col]
            json.dump(collection_dict, open(self.file, "w"))
        self.__col = []

    def modify(self, search_parameters: dict, change_parameters: dict) -> None:
        """
        This method seeks all registries that meet a few criteria and changes the parameters on them as requested

        :param search_parameters: Criteria to seek the registries to be changed
        :param change_parameters: The new data those registries will have
        :return: None, all operations are performed into the collection file
        """

        self.find(search_parameters)
        with json.load(open(self.file, "r")) as collection_dict:
            for e in collection_dict["data"]:
                if e in self.__col:
                    for j in [*e]:
                        e[j] = change_parameters[j]
            json.dump(collection_dict, open(self.file, "w"))
        self.__col = []

    def aggregate(self, pipelines: list[dict]) -> None:
        """
        Method to perform the procedural data extraction and processing

        :param pipelines: list with the series of pipelines with the processes to do
        :return: None, changes applied on __col field
        """
        if [*pipelines[0]][0] != "$find":
            self.find({})

        aggregator = Aggregator(self.__col, self.db)

        aggregator.aggregate(pipelines)
        self.__col = aggregator.col

    def data_fetch(self, data_format: str = "raw", file: str = "") -> object:
        """
        Method to be able to retrieve the data after a search or aggregate in several forms

        :param data_format: Format the data output is wanted. Defaults to "raw"
        :param file: Name (and lo cation) of the file to store the data if it is to be stored
        :return: Several outputs depending on the parameters
        """
        error_msg = f"Format {data_format} not recognized, aborting"

        if data_format == "raw":
            return self.__col
        elif "csv" in data_format:
            columns = [";".join([*self.__col[0]])]
            columns.extend([";".join([*self.__col[e].values()]) for e in range(len(self.__col))])
            if data_format == "csv_to_file":
                with open(file, "w+") as file_obj:
                    file_obj.writelines(columns)
                    file_obj.close()
            elif data_format == "csv_print":
                [print(e) for e in columns]
            elif data_format == "csv_return":
                return columns
            else:
                print(error_msg)
        elif data_format == "pretty_print":
            pprint(self.__col)
        elif data_format == "print":
            print(self.__col)
        elif data_format == "json_file":
            with open(file, "w+") as file_obj:
                json.dump(self.__col, file_obj)
                file_obj.close()
        else:
            print(error_msg)

    def __str__(self):
        print(f"File: {self.file}")

