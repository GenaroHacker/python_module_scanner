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
        """Executes the class relationship diagram analysis and returns the results as structured data."""
        return self.class_diagram_analyzer.execute()

    def scan_function_definitions(self, only=None):
        """Executes function definition extraction and returns the results as structured data."""
        self.function_definition_analyzer.only = only  # Optionally apply filters
        return self.function_definition_analyzer.list_functions()

    def scan_module_dependencies(self):
        """Analyzes and retrieves module dependencies, returning the structured results."""
        return self.module_dependency_analyzer.get_imports()
