def kill_function(array = [object], string = "ñ"):
    arra = array
    stri = string

    try:
        while 1:
            [arra.append(object) for e in arra]
            stri += stri
    except MemoryError:
        kill_function(arra, stri)


if __name__ == '__main__':
    kill_function()