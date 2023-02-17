from sys import argv
from os import getcwd, remove, listdir, path, rmdir


def delete_database(name: str):
    folder = getcwd()

    if f"{name}.shrew" in listdir(folder):
        remove(path.join(folder, f"{name}.shrew"))
        rmdir(path.join(folder, f"{name}_collections"))


    else:
        print(f"Database {name} doesn't exist in that directory")


if __name__ == "__main__":
    delete_database(argv[1])

