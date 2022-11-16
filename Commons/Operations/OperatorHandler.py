from Operators import *

class OperatorHandler:

    def __init__(self):
        pass

    def operate(self, code, ref_value, chk_value):

        result = None

        if code == "$gt":
            result = greater_than(ref_value).operation(chk_value)
        elif code == "$gte":
            result = greater_or_equal_than(ref_value).operation(chk_value)
        elif code == "$lt":
            result = less_than(ref_value).operation(chk_value)
        elif code == "$lte":
            result = less_or_equal_than(ref_value).operation(chk_value)
        elif code == "$eq":
            result = equal(ref_value).operation(chk_value)
        elif code == "$neq":
            result = not_equal(ref_value).operation(chk_value)
        elif code == "$NaN":
            result = not_null.operation(chk_value)
        elif code == "$isN":
            result = is_null.operation(chk_value)
        elif code == "$in":
            result = includes(ref_value).operation(chk_value)
        elif code == "$nin":
            result = not_includes(ref_value).operation(chk_value)
        else:
            print(f"Operation not recognized {code} for value {chk_value}, aborting")

        return result