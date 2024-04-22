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

    def __str__(self):
        return self._print_hierarchy()

    def _print_hierarchy(self, level=0):
        ret = "\t" * level + f"{self.name}\n"
        for subclass in self.subclasses:
            ret += subclass._print_hierarchy(level + 1)
        return ret

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
        """
        Generate a diagram showing relationships and hierarchies among classes in the module,
        formatted in a human-readable string using the Composite pattern.
        """
        # Create a readable format of the class relationships.
        print("Class Relationships Diagram:\n\n")
        for node in self.class_nodes.values():
            if not node.bases:  # Print only top-level classes (no bases)
                print(node)


