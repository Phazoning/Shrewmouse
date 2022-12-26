from BaseCore.Collection import Collection as Col
from ..Commons.Operations.OperatorHandler import OperatorHandler as Op


class Aggregator:

    def __init__(self, collection):
        self.col = collection

    def __find(self, parameters):
        def is_found(chk_object):
            operator = Op()
            return [True for e in chk_object.keys if "$" in parameters[e].keys[0]
                    and operator.operate(parameters[e].keys[0], parameters[e].values[0], chk_object[e])
                    or chk_object[e] == parameters[e]] == [True for e in chk_object.keys]

        return [e for e in self.col if is_found(e)]

    def __lookup(self, local_field, foreign_collection, foreign_field, name):

        for_col = Col(foreign_collection)
        for_col.find({})
        for e in self.col:
            e[name] = [j for j in for_col.col if for_col.col[foreign_field] == e[local_field]]

    def __unwind(self, field):
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

    def __sort(self, field, order):

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

    def __summa(self, key):
        if not (isinstance(self.col[0][key], int) or isinstance(self.col[0][key], float)):
            print(f"Field {key} is not summable, skipping pipeline")
            return None

        return sum([j[key] for j in self.col])

    def __count(self, value_list):
        return len(value_list)

    def __total(self, value_list):
        if [j for j in value_list if (isinstance(j, int) or isinstance(j, float))] == value_list:
            return sum(value_list)
        else:
            print("Non-numeric field, aborting")

    def __single_values(self, value_list):
        ret = []

        for e in value_list:
            ret.append(e) if e not in ret else None

        return ret

    def __group(self, key, fields={}):

        result = []
        singles = []

        with [] as single_records:
            for e in [j[key] for j in self.col]:
                if e not in single_records:
                    single_records.append(e)
            singles = single_records

        for e in singles:
            ret_object = {"_id": e}
            for j in fields.keys():
                field_value = None

                if "$" in j.keys()[0]:
                    with fields[j].keys[0] as operation:
                        if operation == "$sum":
                            field_value = self.__total([i[fields[j].values[0]] for i in self.col])
                        elif operation == "$single":
                            field_value = self.__single_values([i[fields[j].values[0]] for i in self.col])
                        elif operation == "$count":
                            field_value = self.__count([i[fields[j].values[0]] for i in self.col])
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

        return result

    def __project(self, parameters):
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

                elif j.values()[0].values()[0] in e.keys():
                    operation, value = j.values()[0].keys()[0], j.values()[0].values()[0]
                    if operation == "$count":
                        obj[j] = self.__count(value)
                    elif operation == "$single":
                        obj[j] = self.__single_values(value)
                    elif operation == "$sum":
                        obj[j] = self.__total(value)
                    else:
                        print(f"Unable to do operation {operation}, skipping")

                else:
                    print(f"Field {j.values()[0]} not found in element, skipping")

            ret.append(obj)

            return ret

    def aggregate(self, pipelines):

        for pipeline in pipelines:

            operation = pipeline.keys()[0]

            if operation == "$find":
                self.__find(self.__find(pipeline.values()[0]))

            elif operation == "$lookup":
                with pipeline.values()[0] as parameters:
                    self.__lookup(parameters["local_field"], parameters["foreign_collection"],
                                  parameters["foreign_field"], parameters["as"])

            elif operation == "$unwind":
                self.__unwind(pipeline.values()[0])

            elif operation == "$sort":
                with pipeline.values()[0] as parameters:
                    self.__sort(parameters.keys()[0], parameters.values()[0])

            elif operation == "$sum":
                self.__summa(pipeline.values()[0])

            elif operation == "$group":
                with pipeline.values()[0] as parameters:
                    self.__group(parameters["key"], parameters["values"]) if parameters["values"] \
                        else self.__group(parameters["key"])

            elif operation == "$project":
                with pipeline.values()[0] as parameters:
                    self.__project(parameters)

            else:
                print(f"Pipeline {operation} not recognized, skipping")

