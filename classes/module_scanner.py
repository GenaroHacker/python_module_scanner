import ast
from python_module_scanner.classes.generate_class_relationships_diagram import GenerateClassRelationshipsDiagram
from python_module_scanner.classes.extract_function_definitions import ExtractFunctionDefinitions
from python_module_scanner.classes.module_dependency_analyzer import ModuleDependencyAnalyzer

class ModuleScanner:
    def __init__(self, module):
        # Initialize instances of the other classes
        self.class_diagram_analyzer = GenerateClassRelationshipsDiagram(module)
        self.function_definition_analyzer = ExtractFunctionDefinitions(module)
        self.module_dependency_analyzer = ModuleDependencyAnalyzer(module)

    def scan_class_relationships(self):
        """Executes the class relationship diagram analysis and returns the results."""
        self.class_diagram_analyzer.execute()  # Execute analysis
        class_diagram = "Class Relationships Diagram:\n"
        for node in self.class_diagram_analyzer.class_nodes.values():
            if not node.bases:  # Only top-level classes are displayed initially
                class_diagram += str(node)
        return class_diagram

    def scan_function_definitions(self, only=None):
        """Executes function definition extraction and prints the results, with optional filtering."""
        # Temporarily set the only filter for this operation
        self.function_definition_analyzer.only = only
        return self.function_definition_analyzer.list_functions()

    def scan_module_dependencies(self):
        """Analyzes and retrieves module dependencies, returning the formatted results."""
        self.module_dependency_analyzer.analyze_imports()
        imports_report = "Module Dependencies:\n"
        imports_report += f"Direct Imports: {self.module_dependency_analyzer.imports['direct']}\n"
        imports_report += f"From Imports: {self.module_dependency_analyzer.imports['from']}"
        return imports_report

