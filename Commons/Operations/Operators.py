from Operation import Operation as Op

greater_than = lambda val:  Op("$gt", lambda x: x > val)
greater_or_equal_than = lambda val: Op("$gte", lambda x: x >= val)
less_than = lambda val: Op("$lt", lambda x: x < val)
less_or_equal_than = lambda val: Op("$lte", lambda x: x <= val)
equal = lambda val: Op("$eq", lambda x: x == val)
not_equal = lambda val: Op("$neq", lambda x: x != val)
not_null = Op("$NaN", lambda x: x is not None)
is_null = Op("$isN", lambda x: x is None)
includes = lambda val: Op("$in", lambda x: x in val)
not_includes = lambda val: Op("$nin", lambda x: x not in val)