import json
def read_file(path):
    json_list = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            a = {}
            score = line[:2]
            name = line[4:].removeprefix(" ")
            name = name.replace(" \n", "")
            name = name.replace("\n", "")
            a.setdefault("name", name)
            a.setdefault("score", int(score.replace(" ", "")))
            json_list.append(a)
    with open("test.json", "w") as file:
        json.dump(json_list, file)

read_file("./test.txt")
            