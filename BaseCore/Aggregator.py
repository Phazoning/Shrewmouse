from BaseCore.Collection import Collection as Col
from ..Commons.Operations.OperatorHandler import OperatorHandler as Op
from ..Commons.Auxiliary.AuxiliaryMethods import deep_dict_search as dds
from BaseFile import BaseFile


class Aggregator:

    # Constructor method
    def __init__(self, collection: list[dict], db_file: str) -> None:
        """
        !!!Constructor method

        :param collection: dictionary with the registries from the collection
        :param db_file: String with the database data. Needed for the lookup
        """
        self.col = collection
        self.db = db_file

    # General pipeline methods

    def __find(self, parameters: dict) -> None:
        """

        :param parameters: Dictionary detailing the sought parameters.
        Accepts operations (e.g. element in a list with operator "$in")

        :return: None, alters "__col" class parameter
        """

        def is_found(chk_object: dict) -> bool:
            """
            This method iterates over the parameter keys and checks if every key in an object checks all the conditions

            :param chk_object: Object to be checked
            :return: Boolean if the desired value/s have been found or not
            """
            operator = Op()
            ret = False
            for e in [*parameters]:
                ret = True if "$" in [*parameters[e]][0] \
                              and operator.operate([*parameters[e]][0], [*parameters[e].values()][0],
                                                   dds(chk_object, e)) \
                              or dds(chk_object, e) == parameters[e] else False
            return ret

        self.col = [e for e in self.col if is_found(e)]

    def __lookup(self, local_field: str, foreign_collection: str, foreign_field: str, name: str) -> None:
        """
        Method equivalent to SQL JOIN, for all registries in "__col" seeks in a second Collection
        all registries where the field "foreign_field" equals the registry's "local_field"

        :param local_field: Field we are using as a reference for each registry on the collection
        :param foreign_collection: Second collection where want to seek all the equaling registries from
        :param foreign_field: Reference field we are using to check equality
        :param name: name we want to give the new field in the registry
        :return: None, alters "__col" class parameter
        """
        for_col = Col([e for e in BaseFile(self.db).collections if e["name"] == foreign_collection][0], self.db)
        for_col.find({})
        for e in self.col:
            e[name] = [j for j in for_col.data_fetch() if for_col.data_fetch()[foreign_field] == e[local_field]]

    def __unwind(self, field: str) -> None:
        """
        For every element in "__col" gets an array and populates different registries for each value in the array
        assigned to the same field as the original array

        :param field: String with the field we are to unwrap
        :return: None, alters "__col" class parameter
        """
        results = []

        for e in self.col:
            if isinstance(e[field], list):
                for j in e[field]:
                    newobj = e
                    newobj[field] = j
                    results.append(newobj)
            else:
                results.append(e)

        self.col = results

    def __sort(self, field: str, order: int = 1) -> None:
        """
        Sorts "__col" using a field as a reference

        :param field: String with the name of the array we are to order "__col" with
        :param order: Integer denoting if we want normal or inverse order. 1 for normal, -1 for inverse, defaults to 1
        :return: None, alters "__col" class parameter
        """

        # Asserting if the "order" parameter follows an expected value
        if order != 1 and order != -1:
            print(f"Not able to order with value {order}, skipping pipeline")
            return None

        else:
            data = []
            is_reversed = order == -1
            ordered_field = [e[field] for e in self.col]
            ordered_field.sort(reverse=is_reversed)

            with [] as fields:
                for e in ordered_field:
                    if fields.count(e) == 0:
                        fields.append(e)
                ordered_field = fields

            if isinstance(self.col[0][field], str) or isinstance(self.col[0][field], int) or \
                    isinstance(self.col[0][field], float):

                while len(data) < len(self.col):
                    objs = [e for e in self.col if e[field] == ordered_field[0]]
                    if len(objs) > 1:
                        data.extend(objs)
                    else:
                        data.append(objs[0])

                    [self.col.pop(self.col.index(e)) for e in objs]
                    [ordered_field.pop(0) for e in range(len(objs))]

                self.col = data

            else:
                print("Not able to order such a field, skipping pipeline")
                return None

    def __summa(self, key: str) -> int or float:
        """
        Sums all records in a single field

        :param key: String with the field of reference on what to sum
        :return: Number with the total result, float will be returned if any float number involved, else int
        """
        if not (isinstance(self.col[0][key], int) or isinstance(self.col[0][key], float)):
            print(f"Field {key} is not summable, skipping pipeline")
            return None

        return sum([j[key] for j in self.col])

    # Auxiliary methods

    def __count(self, value_list: list) -> int:
        """
        Counts all instances of a single registry

        :param value_list: List with all the values given for a certain field in all registries
        :return:
        """
        return len(value_list)

    def __total(self, value_list: list) -> int or float:
        """
        Returns the sum of all values in an array

        :param value_list: List with all values to sum
        :return: Number with the total result, float will be returned if any float number involved, else int
        """
        if [j for j in value_list if (isinstance(j, int) or isinstance(j, float))] == value_list:
            return sum(value_list)
        else:
            print("Non-numeric field, aborting")

    def __single_values(self, value_list: list) -> list:
        """
        Gets a list with all the different values in an array

        :param value_list: List we'll use to get all the different values from
        :return: List with all the different values
        """
        ret = []

        for e in value_list:
            ret.append(e) if e not in ret else None

        return ret

    # Result pipeline methods

    def __group(self, key: str, fields: dict = {}) -> None:
        """
        Groups all values around a single key while performing operations.
        It's a result pipeline method, so the result will replace "__col"

        :param key: key we'll use to group all values
        :param fields: fields we will use to perform operations while grouping.
        If empty (default) just groups all values in an array
        :return: None, alters "__col" class parameter
        """

        result = []
        singles = []

        with [] as single_records:
            for e in [j[key] for j in self.col]:
                if e not in single_records:
                    single_records.append(e)
            singles = single_records

        for e in singles:
            ret_object = {"_id": e}
            for j in [*fields]:
                field_value = None

                if "$" in j.keys()[0]:
                    with fields[j].keys[0] as operation:
                        if operation == "$sum":
                            field_value = self.__total([i[[*fields[j].values][0]] for i in self.col])
                        elif operation == "$single":
                            field_value = self.__single_values([i[[*fields[j].values[0]]] for i in self.col])
                        elif operation == "$count":
                            field_value = self.__count([i[*[fields[j].values][0]] for i in self.col])
                        else:
                            print("Operator not found, skipping operation")
                else:
                    try:
                        field_value = [i[j.keys()[0]] for i in self.col]
                    except KeyError:
                        if "$" in fields[j].values[0]:
                            try:
                                field_value = [i[fields[j].values[0][1:]] for i in self.col]
                            except KeyError:
                                print(f"Field {fields[j].values[0][1:]} not found")
                        else:
                            print(f"Field {j.keys()[0]} not found")
                ret_object[j] = field_value
            result.append(ret_object)

        self.col = result

    def __project(self, parameters: dict) -> None:
        """
        Alters the form "__col" takes while performing operations.
        It's a result pipeline method, so the result will replace "__col"

        :param parameters: Dictionary which will draw the new form "__col" will take
        :return: None, alters "__col" class parameter
        """
        ret = []
        id_number = None if "_id" not in parameters and parameters["_id"] != -1 else parameters["_id"]

        for e in self.col:
            obj = {}
            if id_number:
                obj["_id"] = id_number
                id_number += 1

            for j in parameters:

                if j.values()[0] in e.keys():
                    obj[j] = e[j.values()[0]]

                elif [*[*j.values()][0].values()][0] in [*e]:
                    operation, value = [*[*j.values()][0]][0], [[*j.values()][0].values()][0]
                    if operation == "$count":
                        obj[j] = self.__count(value)
                    elif operation == "$single":
                        obj[j] = self.__single_values(value)
                    elif operation == "$sum":
                        obj[j] = self.__total(value)
                    else:
                        print(f"Unable to do operation {operation}, skipping")

                else:
                    print(f"Field {list(j.values())[0]} not found in element, skipping")

            ret.append(obj)

        self.col = ret

    # Class utility method

    def aggregate(self, pipelines: list[dict]) -> list[dict]:
        """
        This method exists to actually perform the aggregation operation.
        As such, it'll iterate over a series of pipelines procedurally while altering the original "__col" class parameter
        in accordance with the requested parameters for those pipelines

        :param pipelines: List of dictionaries detailing which operations to perform over "__col" and which parameters
        to use in those operations
        :return: the resulting "__col" parameter in order to be able ot be used externally
        """

        for pipeline in pipelines:
            pipeline_keys = [*pipeline][0]
            pipeline_values = [*pipeline.values()][0]
            operation = pipeline_keys[0]

            if operation == "$find":
                try:
                    assert (isinstance(pipeline_values, dict))
                    self.__find(pipeline_values)
                except AssertionError:
                    print("Parameters must be a dictionary for $find, skipping")

            elif operation == "$lookup":
                self.__lookup(pipeline_values["local_field"], pipeline_values["foreign_collection"],
                              pipeline_values["foreign_field"], pipeline_values["as"])

            elif operation == "$unwind":
                try:
                    assert (pipeline_values in [*self.col[0]] and isinstance(pipeline_values, list or tuple))
                    self.__unwind(pipeline_values)
                except AssertionError:
                    if pipeline_values not in [*self.col[0]]:
                        print(f"Field {pipeline_values} isn't present in the collection,skipping")
                    else:
                        print(f"Field {pipeline_values} isn't a tuple or array, thus it isn't unwindable, skipping")

            elif operation == "$sort":
                try:
                    assert (pipeline_values in [*self.col[0]])
                except AssertionError:
                    print(f"Field {pipeline_values} not found, skipping pipeline")

            elif operation == "$sum":
                self.__summa(pipeline_values)

            elif operation == "$group":
                try:
                    with pipeline_values["_id"] as id_field:
                        pipeline_values.pop("_id")
                        self.__group(id_field, pipeline_values) if pipeline_values else self.__group(id_field)
                except KeyError:
                    print("No _id field found, skipping pipeline")

            elif operation == "$project":
                with pipeline_values[0] as parameters:
                    self.__project(parameters)

            else:
                print(f"Pipeline {operation} not recognized, skipping")

        return self.col
