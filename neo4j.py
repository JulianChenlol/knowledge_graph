import json
from py2neo import Graph, Node, Relationship
import os


# Define the heads, relations, and tails
def read_file(path):
    json_list = []
    with open(path, "r", encoding="utf-8") as file:
        json_list = json.load(file)
    return json_list


def create_node(folder, file, nodes, relationships, root_node, json_list):
    try:
        for term in json_list:
            parent_node = parse_rel(nodes, relationships, term)
            parse_children(nodes, relationships, parent_node, term.get("children"))
            parse_root(root_node, parent_node)
        parse_grade(folder, file, root_node)
    except Exception as r:
        print('未知错误 %s' %(r))
        print("root_node", root_node)

def parse_root(root_node, parent_node):
    a = Relationship(parent_node, "Belong to", root_node)
    relationships.append(a)

def parse_grade(folder, file, parent_node):
    path = "./score/" + folder + "/" + file
    grades = read_file(path)
    for grade in grades:
        node = Node("Grade", name=grade.get("name"), score=grade.get("score"))
        nodes.setdefault(parent_node, node)
        a = Relationship(node, "Score", parent_node)
        relationships.append(a)



def parse_children(nodes, relationships, parent_node, children):
    try:
        for term in children:
            child_node = parse_rel(nodes, relationships, term)
            a = Relationship(child_node, "Belong to", parent_node)
            relationships.append(a)
            parse_children(nodes, relationships, child_node, term.get("children"))
    except Exception as r:
        print('未知错误 %s' %(r))
        print("parent_node", parent_node)
        print("child_node", child_node)



def parse_rel(nodes, relationships, term):
    node = None
    rels = term.get("relationships")
    for rel in rels:
        if rel.get("type") == "Is a":
            node = Node(rel.get("target"), name=term.get("content"))
            nodes.setdefault(term.get("content"), node)
        else:
            # node[rel.get("type")] = rel.get("target")
            node1 = nodes.get(term.get("content"))
            relation = rel.get("type")
            node2 = nodes.setdefault(
                rel.get("target"), Node(rel.get("target"), name=rel.get("target"))
            )
            a = Relationship(node1, relation, node2)
            relationships.append(a)
    return node


if __name__ == "__main__":
    # 连接neo4j数据库，输入地址、用户名、密码
    graph = Graph("http://localhost:7474", password="Welcome123", name="stroke")
    graph.delete_all()
    path = "./data/"
    folders = os.listdir(path)
    for folder in folders:
        files = os.listdir(path + folder)
        root_node = Node("Scale", name=folder)
        graph.create(root_node)
        for file in files:
            nodes = {}
            relationships = []
            json_list = read_file(path + folder + "/" + file)
            file_node = Node("Scale Item", name=file.replace('.json',''))
            a = Relationship(file_node, "Belong to", root_node)
            relationships.append(a)
            print(file)
            create_node(folder, file, nodes, relationships, file_node, json_list)
            for node in nodes.values():
                graph.create(node)
            for relationship in relationships:
                graph.create(relationship)
            print("file", file)
            
