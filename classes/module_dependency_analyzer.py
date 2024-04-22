import ast
import inspect
from python_module_scanner.classes.module_analyzer import ModuleAnalyzer

class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.direct_imports = []
        self.from_imports = []

    def visit_Import(self, node):
        for alias in node.names:
            self.direct_imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module if node.module else ''
        for alias in node.names:
            self.from_imports.append(f"{module}.{alias.name}")
        self.generic_visit(node)

class ModuleDependencyAnalyzer(ModuleAnalyzer):
    def __init__(self, module):
        super().__init__(module)
        self.visitor = ImportVisitor()
        self.analyze_imports()

    def analyze_imports(self):
        """Use the ImportVisitor to traverse the AST and gather import statements."""
        self.visitor.visit(self.ast_tree)
        self.imports = {
            'direct': self.visitor.direct_imports,
            'from': self.visitor.from_imports
        }

    def get_imports(self):
        """Returns the categorized imports."""
        return self.imports



