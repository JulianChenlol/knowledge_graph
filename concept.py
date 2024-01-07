from owlready2 import *
import requests
import json
from typing import List


class Type():
    def __init__(self, type: None, target: None) -> None:
        self.type = type
        self.target = target


class Tree():
    def __init__(self, content: str) -> None:
        self.children = []
        self.content = content
        self.relationships = []


class TreeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tree):
            return {"content": obj.content, "children": obj.children, "relationships": [{"type": a.type, "target": a.target} for a in obj.relationships]}
        return super().default(obj)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}


def build():
    input_file = './Terminology/sct2_sRefset_OWLExpressionFull_US1000124_20230901.txt'  # 输入文件路径
    output_file = './output.txt'  # 输出文件路径

    with open(input_file, 'r') as file:
        with open(output_file, 'w') as output:
            for line in file:
                if '230690007' in line:
                    output.write(line)


def express():

    url = "https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN/2024-01-01/descriptions"
    params = {
        'limit': 100,
        'term': 'stroke',
        'active': True,
        'conceptActive': True,
        'lang': 'english',
        'groupByConcept': True
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        content = json.loads(response.text)
        id = content.get("items")[0].get("concept").get("id")
        url = "https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN/2024-01-01/concepts/{}/children?form=inferred".format(
            "230690007")
        params = {
            'form': 'inferred'
        }
        response = requests.get(url, params=params, headers=headers)
        result = Tree(None)
        getChildren(id, result)
        return result


def getChildren(id, tree):
    url = "https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN/2024-01-01/concepts/{}/children".format(
        id)
    params = {
        'form': 'inferred'
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        content = json.loads(response.text)
        if content:
            for c in content:
                a = Tree(c.get("pt").get("term"))
                tree.children.append(a)
                getPro(id, a)
                getChildren(c.get("id"), a)
                print(a.children)


def getPro(id, tree):
    url = "https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN/2024-01-01/concepts/{}".format(
        id)
    params = {
        'descendantCountForm': 'inferred'
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        content = json.loads(response.text)
        if content:
            for a in content.get("classAxioms"):
                for re in a.get("relationships"):
                    tree.relationships.append(Type(re.get("type").get("pt").get("term"), re.get("target").get("pt").get("term")))


if __name__ == '__main__':
    result = express()
    json_str = json.dumps(result, cls=TreeEncoder)
    json_object = json.loads(json_str)
    with open("data3.json", "w") as file:
        json.dump(json_object, file)
