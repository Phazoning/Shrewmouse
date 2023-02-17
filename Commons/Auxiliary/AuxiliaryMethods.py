def deep_dict_search(dictionary: dict, field: str) -> object:
    """
    Auxiliary method to delve in a dictionary and find the value of a nested object

    :param dictionary: Dictionary of the object with the all values
    :param field: field we desire to extract. If it's nested, syntax is "field1.field2.field3"
    :return: The desired nested field
    """
    obj = dictionary
    fields = field.split(".") if "." in field else [field]
    while not fields:
        if fields[0] not in [*obj] and isinstance(obj, dict):
            raise KeyError
        elif not isinstance(obj, dict):
            return obj
        elif len(fields) == 1:
            return obj[fields[0]]
        else:
            obj = obj[fields[0]]
            fields.pop()

