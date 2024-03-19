import json

# 读取JSON数据


# Define the heads, relations, and tails
def read_file():
    json_list = []
    with open("stroke_data.json", "r") as file:
        json_list = json.load(file)
    return json_list


data = read_file()

# 生成OWL格式数据
owl_data = f"""
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
    <owl:Ontology rdf:about="http://example.org/ontology"/>
"""

for item in data:
    owl_data += f"""
    <owl:Class rdf:about="#{item['content']}">
        <rdfs:label>{item['content']}</rdfs:label>
    </owl:Class>
"""

    for child in item["children"]:
        owl_data += f"""
    <owl:Class rdf:about="#{child['content']}">
        <rdfs:label>{child['content']}</rdfs:label>
        <rdfs:subClassOf rdf:resource="#{item['content']}"/>
    </owl:Class>
    """

        for relationship in child.get("relationships", []):
            owl_data += f"""
    <owl:ObjectProperty rdf:about="#{relationship['type']}">
        <rdfs:domain rdf:resource="#{child['content']}"/>
        <rdfs:range rdf:resource="#{relationship['target']}"/>
    </owl:ObjectProperty>
"""

owl_data += "</rdf:RDF>"

# 将OWL数据写入文件
with open("stroke.owl", "w", encoding="utf-8") as file:
    file.write(owl_data)

print("OWL文件已生成：stroke.owl")
