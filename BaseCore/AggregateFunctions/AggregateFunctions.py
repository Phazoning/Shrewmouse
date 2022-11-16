from ..Collection import Collection as Col


def lookup(name, reference_field, target_collection, target_field, records):
    looked_records = []
    for e in records:
        target = Col(target_collection)
        target.find({target_field: e[reference_field]})
        e[name] = target.col
        if e[name]:
            looked_records.append(e)
    return looked_records


def unwind(field, records):
    unwinded = []
    for e in records:
        field_records = e[field]
        e.pop(field)
        for i in field_records:
            record = e
            record[field] = i
            unwinded.append(e)
    return unwinded

