import json


class Type:
    def __init__(self, type: None, target: None) -> None:
        self.type = type
        self.target = target


class Tree:
    def __init__(self, content: str) -> None:
        self.children = []
        self.content = content
        self.relationships = []


class TreeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tree):
            return {
                "content": obj.content,
                "children": obj.children,
                "relationships": [
                    {"type": a.type, "target": a.target} for a in obj.relationships
                ],
            }
        return super().default(obj)
