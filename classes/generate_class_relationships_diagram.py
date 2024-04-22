import ast
from python_module_scanner.classes.module_analyzer import ModuleAnalyzer

class ClassNode:
    def __init__(self, name):
        self.name = name
        self.bases = []
        self.subclasses = []

    def add_base(self, base):
        self.bases.append(base)

    def add_subclass(self, subclass):
        self.subclasses.append(subclass)

    def to_dict(self):
        # Convert the class node and its hierarchy to a dictionary
        return {
            'name': self.name,
            'bases': [base.name for base in self.bases],
            'subclasses': [subclass.to_dict() for subclass in self.subclasses]
        }


class GenerateClassRelationshipsDiagram(ModuleAnalyzer):
    def __init__(self, module):
        super().__init__(module)
        self.class_nodes = {cls['name']: ClassNode(cls['name']) for cls in self.classes}
        for cls in self.classes:
            node = self.class_nodes[cls['name']]
            for base in cls['bases']:
                if base in self.class_nodes:
                    node.add_base(self.class_nodes[base])
                    self.class_nodes[base].add_subclass(node)

    def execute(self):
        # Instead of printing, structure the data into a nested dictionary
        output = {}
        for node in self.class_nodes.values():
            if not node.bases:  # Only top-level classes included initially
                output[node.name] = node.to_dict()
        return output


