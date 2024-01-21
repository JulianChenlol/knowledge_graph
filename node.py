import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import json

head = []
relation = []
tail = []


# Define the heads, relations, and tails
def read_file():
    json_list = []
    with open("stroke_data.json", "r") as file:
        json_list = json.load(file)
        for term in json_list:
            parent = term.get("content")
            parse_rel(term)
            parse_children(parent, term.get("children"))


def parse_children(parent, children):
    for child in children:
        parse_rel(child)
        head.append(parent)
        relation.append("contains")
        tail.append(child.get("content"))
        # print(head[-1], relation[-1], tail[-1])
        parse_children(child.get("content"), child.get("children"))


def parse_rel(term):
    rels = term.get("relationships")
    for rel in rels:
        head.append(term.get("content"))
        relation.append(rel.get("type"))
        tail.append(rel.get("target"))
        # print(head[-1], relation[-1], tail[-1])


def total(G):
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")
    print(f"Ratio edges to nodes: {round(num_edges / num_nodes, 2)}")


def visual(G):
    pos = nx.spring_layout(G, seed=42, k=0.9)
    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)

    # Visualize centrality measures
    plt.figure(figsize=(15, 10))

    # Degree centrality
    plt.subplot(131)
    nx.draw(
        G,
        pos,
        with_labels=True,
        font_size=10,
        node_size=[v * 3000 for v in degree_centrality.values()],
        node_color=list(degree_centrality.values()),
        cmap=plt.cm.Blues,
        edge_color="gray",
        alpha=0.6,
    )
    plt.title("Degree Centrality")

    # Betweenness centrality
    plt.subplot(132)
    nx.draw(
        G,
        pos,
        with_labels=True,
        font_size=10,
        node_size=[v * 3000 for v in betweenness_centrality.values()],
        node_color=list(betweenness_centrality.values()),
        cmap=plt.cm.Oranges,
        edge_color="gray",
        alpha=0.6,
    )
    plt.title("Betweenness Centrality")

    # Closeness centrality
    plt.subplot(133)
    nx.draw(
        G,
        pos,
        with_labels=True,
        font_size=10,
        node_size=[v * 3000 for v in closeness_centrality.values()],
        node_color=list(closeness_centrality.values()),
        cmap=plt.cm.Greens,
        edge_color="gray",
        alpha=0.6,
    )
    plt.title("Closeness Centrality")

    plt.tight_layout()
    plt.show()


def draw():
    # Create a dataframe
    df = pd.DataFrame({"head": head, "relation": relation, "tail": tail})
    # # Create a knowledge graph
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(row["head"], row["tail"], label=row["relation"])

    total(G)
    # visual(G)

    # Visualize the knowledge graph
    pos = nx.spring_layout(G, seed=42, k=0.9)
    labels = nx.get_edge_attributes(G, "label")
    plt.figure(figsize=(12, 10))
    nx.draw(
        G,
        pos,
        with_labels=True,
        font_size=10,
        node_size=700,
        node_color="lightblue",
        edge_color="gray",
        alpha=0.6,
    )
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=labels,
        font_size=8,
        label_pos=0.3,
        verticalalignment="baseline",
    )
    plt.title("Knowledge Graph")
    plt.savefig("knowledge_graph.png")
    plt.show()


if __name__ == "__main__":
    read_file()
    draw()
