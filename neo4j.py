import json
from py2neo import Graph, Node, Relationship


nodes = {}
relationships = []


# Define the heads, relations, and tails
def read_file():
    json_list = []
    with open("stroke_data.json", "r") as file:
        json_list = json.load(file)
    return json_list


def create_node(json_list):
    for term in json_list:
        parent = term.get("content")
        parent_node = parse_rel(term)
        parse_children(parent_node, parent, term.get("children"))


def parse_children(parent_node, parent, children):
    for term in children:
        child = term.get("content")
        child_node = parse_rel(term)
        a = Relationship(parent_node, "contains", child_node)
        relationships.append(a)
        parse_children(child_node, child, term.get("children"))


def parse_rel(term):
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


def create_graph():
    # 连接neo4j数据库，输入地址、用户名、密码
    graph = Graph("http://localhost:7474", password="Welcome123")

    graph.delete_all()

    for i in range(len(head)):
        node = Node()
    # 创建结点
    node1 = Node("person", name="chenjianbo")  # 该结点语义类型是person  结点名字是chenjianbo  也是它的属性
    node2 = Node("major", name="software")  # 该结点语义类型是major  结点名字是software  也是它的属性
    node3 = Node("person", name="bobo")  # 该结点语义类型是person  结点名字是bobo   也是它的属性

    # 给结点node1 添加一个属性 age
    node1["age"] = 18
    # 给结点node2 添加一个属性 college
    node2["college"] = "software college"
    # 给结点node3 添加一个属性 sex
    node3["sex"] = "男"

    # 把结点实例化 在Neo4j中显示出来
    graph.create(node1)
    graph.create(node2)
    graph.create(node3)
    # 创建关系
    maojor = Relationship(node1, "专业", node2)
    friends = Relationship(node1, "朋友", node3)
    maojor1 = Relationship(node3, "专业", node2)
    # 把关系实例化 在Neo4j中显示出来
    graph.create(maojor)
    graph.create(maojor1)
    graph.create(friends)


if __name__ == "__main__":
    json_list = read_file()
    create_node(json_list)
    # 连接neo4j数据库，输入地址、用户名、密码
    graph = Graph("http://localhost:7474", password="Welcome123")

    graph.delete_all()
    for node in nodes.values():
        graph.create(node)
    for relationship in relationships:
        graph.create(relationship)
