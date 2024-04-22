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
        """List all functions using the iterator pattern, returning results as a string."""
        result = "Function Definitions:\n"
        while self.iterator.has_next():
            func = self.iterator.next()
            result += f"Function Name: {func['name']}\n"
            if func['class']:
                result += f"  Class: {func['class']}\n"
            for key, value in func.items():
                if key not in ['name', 'class'] and value is not None:
                    result += f"  {key.capitalize()}: {value}\n"
            result += "\n"  # Blank line for separation
        return result



