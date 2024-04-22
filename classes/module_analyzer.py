import ast
import inspect

class ModuleAnalyzer:
    def __init__(self, module):
        self.module = module
        self.ast_tree = ast.parse(inspect.getsource(module))
        self.classes = []
        self.functions = []
        self.dependencies = []
        self.api_surface_area = []
        self.globals = []
        self._parse_classes()
        self._parse_functions()
        self._parse_imports()

    def _parse_classes(self):
        """Private helper method to parse class definitions from the AST."""
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                base_classes = [base.id for base in node.bases if isinstance(base, ast.Name)]
                self.classes.append({'name': node.name, 'bases': base_classes, 'body': node.body})

    def _parse_functions(self):
        """Private helper method to parse function definitions from the AST."""
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                decorators = [decorator.id for decorator in node.decorator_list if isinstance(decorator, ast.Name)]
                self.functions.append({'name': node.name, 'args': args, 'decorators': decorators, 'body': node.body})

    def _parse_imports(self):
        """Private helper method to parse import statements from the AST."""
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.dependencies.append({'module': alias.name, 'alias': alias.asname})
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    self.dependencies.append({
                        'module': f"{node.module if node.module else ''}.{alias.name}",
                        'alias': alias.asname,
                        'level': node.level
                    })




