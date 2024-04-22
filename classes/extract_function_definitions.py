import ast
from python_module_scanner.classes.module_analyzer import ModuleAnalyzer

class FunctionIterator:
    """Iterator for accessing and traversing elements."""
    def __init__(self, data):
        self.data = data
        self.index = 0

    def has_next(self):
        """Check if there are more elements."""
        return self.index < len(self.data)

    def next(self):
        """Return the next element."""
        if not self.has_next():
            raise StopIteration("No more elements")
        result = self.data[self.index]
        self.index += 1
        return result

class ExtractFunctionDefinitions(ModuleAnalyzer):
    def __init__(self, module, only=None):
        super().__init__(module)
        self.only = only or {}
        self.functions = self._parse_functions()
        self.iterator = FunctionIterator(self.filtered_functions())

    def filtered_functions(self):
        """Apply filters based on the 'only' options provided."""
        filtered = self.functions
        if 'docstring' in self.only:
            filtered = [f for f in filtered if (f['docstring'] is not None) == self.only['docstring']]
        if 'decorators' in self.only:
            filtered = [f for f in filtered if (f['decorators'] is not None) == self.only['decorators']]
        if 'args' in self.only:
            filtered = [f for f in filtered if (f['args'] is not None) == self.only['args']]
        if 'returns' in self.only:
            filtered = [f for f in filtered if (f['returns'] is not None) == self.only['returns']]
        if 'class' in self.only:
            filtered = [f for f in filtered if f['class'] in self.only['class'] if self.only['class'] is not None]
        
        return filtered

    def _parse_functions(self):
        """Private helper method to parse function definitions and retrieve detailed info, including class membership."""
        function_list = []
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                parent_class = [c.name for c in ast.walk(self.ast_tree) if isinstance(c, ast.ClassDef) and node in c.body]
                func_info = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args] if node.args.args else None,
                    'returns': ast.unparse(node.returns) if node.returns else None,
                    'docstring': ast.get_docstring(node),
                    'decorators': [ast.unparse(decorator) for decorator in node.decorator_list] if node.decorator_list else None,
                    'class': parent_class[0] if parent_class else None
                }
                function_list.append(func_info)
        return function_list

    def list_functions(self):
        """Return a list of functions as dictionaries."""
        functions_list = []
        while self.iterator.has_next():
            func = self.iterator.next()
            function_detail = {
                'name': func['name'],
                'class': func.get('class'),
                'details': {k: v for k, v in func.items() if k not in ['name', 'class'] and v is not None}
            }
            functions_list.append(function_detail)
        return functions_list
