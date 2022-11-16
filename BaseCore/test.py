def myfunc():
    file = "aaaa.txt"
    copy_file = "aaaa_copy.txt"

    #Part 1
    open(copy_file, "w+").writelines([open(file, "r").readline(e) for e in range(len(open(file, "r").readlines()), 0)])

    #Part 2
    open(copy_file, "a").write("Alonso Morenas Diaz")

    #Part 3
    [print(e) for e in open(copy_file, "r").readlines()]
