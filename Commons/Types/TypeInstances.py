from Type import Type


references = {
    "Int32": Type(int, 32),
    "Int64": Type(int, 64),
    "Float32": Type(float, 32),
    "Float64": Type(float, 64),
    "String": Type(str),
    "Boolean": Type(bool),
    "List": Type(list),
    "Object": Type(dict)
}


