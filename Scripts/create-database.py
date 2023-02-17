from sys import argv
from os import getcwd, mkdir, path, listdir
import json


def create_database(name: str):
    folder = getcwd()

    if f"{name}.shrew" not in listdir(folder):
        with open(path.join(folder, f"{name}.shrew"), "w+") as file:
            item = {
                "name": name,
                "collections": []
            }
        json.dump(item, file)
        mkdir(path.join(folder, f"{name}_collections"))
    else:
        print(f"Database {name} already exists in that directory")


if __name__ == "__main__":
    create_database(argv[1])

