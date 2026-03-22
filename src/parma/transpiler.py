"""Core SQF transpiler for Python AST."""
import ast
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class SQFTranspiler(ast.NodeVisitor):
    """Transpiles Python AST to SQF code."""

    def __init__(self):
        self.output: List[str] = []
        self.indent_level = 0
        self.variables: Dict[str, str] = {}
        self.classes: Dict[str, Dict] = {}
        self.current_class: Optional[str] = None
        self.scopes: List[Dict[str, str]] = []  # Stack of variable scopes
        self.function_params: Dict[str, List[str]] = {}  # Function parameter names
        self.imports: Dict[str, str] = {}  # Maps alias to module name
        self.imported_functions: Dict[str, str] = {}  # Maps imported function names to SQF equivalents
        self.current_function: Optional[str] = None  # Current function being processed
        self.source_lines: List[str] = []  # Source code lines for error reporting
        self.errors: List[str] = []  # Collection of errors found during transpilation
        # Performance optimizations
        self._expr_cache: Dict[str, str] = {}  # Cache for expression results
        self._var_cache: Dict[str, str] = {}  # Cache for variable resolutions

    def _add_error(self, message: str, node: Optional[ast.AST] = None):
        """Add an error with line number context."""
        if node and hasattr(node, 'lineno') and node.lineno:
            line_num = node.lineno
            if 0 < line_num <= len(self.source_lines):
                line_content = self.source_lines[line_num - 1].strip()
                error_msg = f"Line {line_num}: {message}\n    {line_content}"
            else:
                error_msg = f"Line {line_num}: {message}"
        else:
            error_msg = message
        self.errors.append(error_msg)

    def get_errors(self) -> List[str]:
        """Get all errors found during transpilation."""
        return self.errors.copy()

    def _push_scope(self):
        """Push a new variable scope"""
        self.scopes.append({})

    def _pop_scope(self):
        """Pop the current variable scope"""
        if self.scopes:
            self.scopes.pop()

    def _add_variable(self, name: str, sqf_name: Optional[str] = None):
        """Add a variable to the current scope"""
        if not self.scopes:
            self._push_scope()
        if sqf_name is None:
            sqf_name = name
        self.scopes[-1][name] = sqf_name

    def _resolve_variable(self, name: str) -> str:
        """Resolve a variable name to its SQF equivalent"""
        # Check cache first
        if name in self._var_cache:
            return self._var_cache[name]

        result = self._resolve_variable_uncached(name)

        # Cache the result (but not for dynamic variables)
        if result == name and name not in ['True', 'False', 'None']:
            # Don't cache unresolved variables that might be defined later
            pass
        else:
            self._var_cache[name] = result

        return result

    def _resolve_variable_uncached(self, name: str) -> str:
        """Internal variable resolution without caching"""
        # Check if it's a built-in name that should be preserved
        if name in ['True', 'False', 'None', 'self']:
            return name

        # Check if it's a function parameter in current function
        if self.current_function and name in self.function_params.get(self.current_function, []):
            return name  # Parameters are passed as-is

        # Check all scopes from innermost to outermost
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]

        # Check global variables
        if name in self.variables:
            return self.variables[name]

        # Check if it's an imported module/function
        if name in self.imports:
            return name  # Import aliases should be preserved

        # If not found, it might be:
        # 1. A variable defined later (forward reference)
        # 2. A built-in function we're calling
        # 3. A parameter that will be passed in
        # For now, return as-is and let SQF handle it
        logger.debug(f"Unresolved variable: {name} (may be forward reference, built-in, or parameter)")
        return name

    def transpile(self, source_code: str) -> str:
        """Transpile Python AST to SQF."""
        try:
            tree = ast.parse(source_code, mode='exec')
            self.source_lines = source_code.splitlines()
            self.visit(tree)
            return self._format_output()
        except SyntaxError as e:
            line_info = f" at line {e.lineno}: {self.source_lines[e.lineno-1].strip()}" if e.lineno else ""
            raise ValueError(f"Invalid Python syntax{line_info}: {e}")

    def _format_output(self) -> str:
        """Format the generated SQF code with optimized string building."""
        # Pre-allocate list with header
        lines = [
            "/*",
            " * Generated by Parma - Python to SQF Transpiler",
            " */",
            '#include "macros/oop.h"',
            ""
        ]

        # Extend with output lines for efficiency
        lines.extend(self.output)

        # Clean up consecutive empty lines in one pass
        cleaned_lines = []
        prev_empty = False

        for line in lines:
            stripped = line.strip()
            is_empty = len(stripped) == 0
            if not (is_empty and prev_empty):  # Avoid consecutive empty lines
                cleaned_lines.append(line.rstrip())  # Remove trailing whitespace
            prev_empty = is_empty

        # Use join for efficient final string creation
        return '\n'.join(cleaned_lines)

    def _indent(self) -> str:
        """Get current indentation."""
        return "    " * self.indent_level

    def _add_line(self, line: str):
        """Add a line to output with proper indentation."""
        self.output.append(f"{self._indent()}{line}")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Handle class definitions using OOP macros."""
        class_name = node.name

        # Use CLASS macro instead of raw class syntax
        if node.bases:
            # Handle inheritance
            base_name = node.bases[0].id if isinstance(node.bases[0], ast.Name) else "unknown"
            self._add_line(f'CLASS_EXTENDS("{class_name}","{base_name}")')
        else:
            self._add_line(f'CLASS("{class_name}")')

        # Store class info
        self.classes[class_name] = {
            'methods': {},
            'bases': [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases],
            'instance_vars': set()
        }

        # Process class body
        self.current_class = class_name
        for item in node.body:
            self.visit(item)
        self.current_class = None

        self._add_line("ENDCLASS;")
        self._add_line("")

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Handle function definitions using OOP macros."""
        func_name = node.name
        args = [arg.arg for arg in node.args.args]

        # Track function parameters
        self.function_params[func_name] = args
        self.current_function = func_name

        # Push function scope and add parameters
        self._push_scope()
        for arg in args:
            self._add_variable(arg)  # Parameters are available in function scope

        # Special handling for __init__
        if func_name == "__init__":
            func_name = "constructor"
            # Assume public for now
            self._add_line(f'PUBLIC FUNCTION("array","{func_name}") {{')
        else:
            # Assume public for now - could be enhanced to detect private methods
            return_type = "any"  # Could be enhanced to infer types
            self._add_line(f'PUBLIC FUNCTION("{return_type}","{func_name}") {{')

        self.indent_level += 1

        # Process function body
        for stmt in node.body:
            self.visit(stmt)

        self.indent_level -= 1
        self._add_line("};")
        self._add_line("")

        # Pop function scope
        self._pop_scope()
        self.current_function = None

    def visit_Return(self, node: ast.Return) -> None:
        """Handle return statements."""
        if node.value:
            value = self._visit_expr(node.value)
            self._add_line(f"{value}")
        else:
            self._add_line("nil")

    def visit_Import(self, node: ast.Import) -> None:
        """Handle import statements."""
        # For now, we'll ignore most imports as they don't translate directly to SQF
        # But we can add special handling for specific modules if needed
        for alias in node.names:
            module_name = alias.name
            as_name = alias.asname or module_name

            # Track imports for method resolution
            self.imports[as_name] = module_name

            # Handle specific modules that might be useful
            if module_name in ["math", "random"]:
                # These are handled by built-in SQF functions or can be ignored
                # Add a comment for clarity
                self._add_line(f"// Imported {module_name} as {as_name}")
            else:
                # For unknown modules, add a warning comment
                self._add_line(f"// Warning: Import of '{module_name}' not supported in SQF")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Handle from ... import statements."""
        module_name = node.module or ""

        for alias in node.names:
            name = alias.name
            as_name = alias.asname or name

            # Handle specific imports that can be mapped to SQF
            if module_name == "math":
                if name in ["sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "atan2", "pi", "e", "floor", "ceil", "abs", "pow", "log", "exp"]:
                    self._add_line(f"// Imported math.{name} as {as_name}")
                else:
                    self._add_line(f"// Warning: math.{name} not supported in SQF")
            elif module_name == "random":
                if name in ["uniform", "choice", "randint", "random", "seed", "shuffle", "sample"]:
                    self._add_line(f"// Imported random.{name} as {as_name}")
                else:
                    self._add_line(f"// Warning: random.{name} not supported in SQF")
            elif module_name == "json":
                if name in ["loads", "dumps"]:
                    self._add_line(f"// Imported json.{name} as {as_name}")
                else:
                    self._add_line(f"// Warning: json.{name} not supported in SQF")
            elif module_name == "datetime":
                if name in ["datetime", "date", "time", "timedelta"]:
                    self._add_line(f"// Imported datetime.{name} as {as_name}")
                else:
                    self._add_line(f"// Warning: datetime.{name} not supported in SQF")
            elif module_name == "collections":
                if name in ["defaultdict", "Counter", "deque"]:
                    self._add_line(f"// Imported collections.{name} as {as_name}")
                else:
                    self._add_line(f"// Warning: collections.{name} not supported in SQF")
            elif module_name == "json":
                if name in ["loads", "dumps"]:
                    self._add_line(f"// Imported json.{name} as {as_name}")
                else:
                    self._add_line(f"// Warning: json.{name} not supported in SQF")
            elif module_name == "typing":
                # Type hints are ignored in SQF
                self._add_line(f"// Imported typing.{name} as {as_name} (type hints ignored)")
            else:
                self._add_line(f"// Warning: Import from '{module_name}' not supported in SQF")

    def visit_Expr(self, node: ast.Expr) -> None:
        """Handle expression statements."""
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value)
            self._add_line(";")
        else:
            self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Handle function calls."""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id

            # Handle built-in functions
            if func_name == "print":
                self._handle_print(node)
            elif func_name == "len":
                self._handle_len(node)
            elif func_name == "range":
                self._handle_range(node)
            elif func_name == "random":
                self._handle_random(node)
            elif func_name == "enumerate":
                self._handle_enumerate(node)
            elif func_name == "zip":
                self._handle_zip(node)
            elif func_name == "reversed":
                self._handle_reversed(node)
            elif func_name == "isinstance":
                self._handle_isinstance(node)
            elif func_name == "str":
                self._handle_str(node)
            elif func_name == "int":
                self._handle_int(node)
            elif func_name == "float":
                self._handle_float(node)
            elif func_name == "sum":
                self._handle_sum(node)
            elif func_name == "max":
                self._handle_max_min(node, "max")
            elif func_name == "min":
                self._handle_max_min(node, "min")
            elif func_name == "all":
                self._handle_all(node)
            elif func_name == "any":
                self._handle_any(node)
            elif func_name == "abs":
                self._handle_abs(node)
            elif func_name == "round":
                self._handle_round(node)
            elif func_name == "bool":
                self._handle_bool(node)
            # Handle math functions
            elif func_name == "sqrt":
                self._handle_math_sqrt(node)
            elif func_name == "sin":
                self._handle_math_sin(node)
            elif func_name == "cos":
                self._handle_math_cos(node)
            elif func_name == "tan":
                self._handle_math_tan(node)
            elif func_name == "asin":
                self._handle_math_asin(node)
            elif func_name == "acos":
                self._handle_math_acos(node)
            elif func_name == "atan":
                self._handle_math_atan(node)
            elif func_name == "atan2":
                self._handle_math_atan2(node)
            elif func_name == "floor":
                self._handle_math_floor(node)
            elif func_name == "ceil":
                self._handle_math_ceil(node)
            elif func_name == "pow":
                self._handle_math_pow(node)
            elif func_name == "log":
                self._handle_math_log(node)
            elif func_name == "exp":
                self._handle_math_exp(node)
            # Handle more random functions
            elif func_name == "random":
                self._handle_random_random(node)
            elif func_name == "randint":
                self._handle_random_randint(node)
            elif func_name == "seed":
                self._handle_random_seed(node)
            elif func_name == "shuffle":
                self._handle_random_shuffle(node)
            elif func_name == "sample":
                self._handle_random_sample(node)
            # Handle JSON functions
            elif func_name == "loads":
                self._handle_json_loads(node)
            elif func_name == "dumps":
                self._handle_json_dumps(node)
            # Handle random functions
            elif func_name == "uniform":
                self._handle_random_uniform(node)
            elif func_name == "choice":
                self._handle_random_choice(node)
            elif func_name in self.classes:
                # Class instantiation
                args = []
                for arg in node.args:
                    if isinstance(arg, ast.Str):
                        args.append(f'"{arg.s}"')
                    elif isinstance(arg, ast.Num):
                        args.append(str(arg.n))
                    elif isinstance(arg, ast.Constant):
                        if isinstance(arg.value, str):
                            args.append(f'"{arg.value}"')
                        else:
                            args.append(str(arg.value))
                    elif isinstance(arg, ast.Name):
                        args.append(arg.id)
                    else:
                        args.append(self._visit_expr(arg))

                if args:
                    args_str = ", " + ", ".join(args)
                else:
                    args_str = ""
                self.output.append(f'["new"{args_str}] call {func_name}')
            else:
                # Regular function call
                args = []
                for arg in node.args:
                    if isinstance(arg, ast.Str):
                        args.append(f'"{arg.s}"')
                    elif isinstance(arg, ast.Num):
                        args.append(str(arg.n))
                    elif isinstance(arg, ast.Constant):
                        if isinstance(arg.value, str):
                            args.append(f'"{arg.value}"')
                        else:
                            args.append(str(arg.value))
                    elif isinstance(arg, ast.Name):
                        args.append(arg.id)
                    else:
                        args.append(self._visit_expr(arg))

                args_str = ", ".join(args)
                self.output.append(f"{func_name}({args_str})")
        elif isinstance(node.func, ast.Attribute):
            # Method call like obj.method() or obj.attr.method()
            method = node.func.attr
            obj_name = "unknown"  # Default

            # Get the object being called on
            if isinstance(node.func.value, ast.Name):
                obj_name = node.func.value.id
                if obj_name == "self":
                    obj = "this"
                else:
                    obj = obj_name
            elif isinstance(node.func.value, ast.Attribute):
                # Handle self.attribute.method() or obj.attribute.method()
                inner_obj = node.func.value.value.id if isinstance(node.func.value.value, ast.Name) else "unknown"
                if inner_obj == "self":
                    obj = f"this.{node.func.value.attr}"
                else:
                    obj = f"{inner_obj}.{node.func.value.attr}"
            else:
                obj = "unknown"

            # Handle specific methods
            obj_module = self.imports.get(obj_name, obj_name)
            if method == "uniform" and obj_module == "random":
                self._handle_random_uniform(node)
            elif method == "choice" and obj_module == "random":
                self._handle_random_choice(node)
            elif method == "randint" and obj_module == "random":
                self._handle_random_randint(node)
            elif method == "random" and obj_module == "random":
                self._handle_random_random(node)
            elif method == "seed" and obj_module == "random":
                self._handle_random_seed(node)
            elif method == "shuffle" and obj_module == "random":
                self._handle_random_shuffle(node)
            elif method == "sample" and obj_module == "random":
                self._handle_random_sample(node)
            # JSON functions
            elif method == "loads" and obj_module == "json":
                self._handle_json_loads(node)
            elif method == "dumps" and obj_module == "json":
                self._handle_json_dumps(node)
            # Math functions
            elif method in ["sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "floor", "ceil", "log", "exp"] and obj_module == "math":
                handler_name = f"_handle_math_{method}"
                if hasattr(self, handler_name):
                    getattr(self, handler_name)(node)
            elif method == "atan2" and obj_module == "math":
                self._handle_math_atan2(node)
            elif method == "pow" and obj_module == "math":
                self._handle_math_pow(node)
            elif method == "append":
                # List append
                args = []
                for arg in node.args:
                    if isinstance(arg, ast.Str):
                        args.append(f'"{arg.s}"')
                    elif isinstance(arg, ast.Num):
                        args.append(str(arg.n))
                    elif isinstance(arg, ast.Constant):
                        if isinstance(arg.value, str):
                            args.append(f'"{arg.value}"')
                        else:
                            args.append(str(arg.value))
                    else:
                        args.append(self._visit_expr(arg))
                args_str = ", ".join(args)
                self.output.append(f"{obj} pushBack {args_str};")
            elif method == "clear":
                if obj == "this.created_units":
                    self.output.append('MEMBER("created_units",[])')
                else:
                    self.output.append(f"{obj} = []")
            else:
                # Generic method call using MEMBER macro
                args = []
                for arg in node.args:
                    if isinstance(arg, ast.Str):
                        args.append(f'"{arg.s}"')
                    elif isinstance(arg, ast.Num):
                        args.append(str(arg.n))
                    elif isinstance(arg, ast.Constant):
                        if isinstance(arg.value, str):
                            args.append(f'"{arg.value}"')
                        else:
                            args.append(str(arg.value))
                    elif isinstance(arg, ast.Name):
                        args.append(arg.id)
                    else:
                        args.append("arg")  # Placeholder

                if args:
                    args_str = ", ".join(args)
                    self.output.append(f'MEMBER("{method}",[{args_str}])')
                else:
                    self.output.append(f'MEMBER("{method}",nil)')

    def _handle_print(self, node: ast.Call) -> None:
        """Handle print() calls - convert to diag_log with proper SQF syntax."""
        if node.args:
            arg = node.args[0]
            if isinstance(arg, ast.Str):
                # Simple string
                self.output.append(f'diag_log "{arg.s}";')
            elif isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                # Constant string (Python 3.8+)
                self.output.append(f'diag_log "{arg.value}";')
            elif isinstance(arg, ast.BinOp) and self._is_string_concatenation(arg):
                # String concatenation - convert to format[]
                parts = self._extract_string_parts(arg)
                if len(parts) == 2:
                    format_str = f'format["%1%2", {parts[0]}, {parts[1]}]'
                    self.output.append(f'diag_log {format_str};')
                else:
                    # Fallback for complex concatenation
                    formatted = self._visit_expr(arg)
                    self.output.append(f'diag_log {formatted};')
            elif isinstance(arg, ast.Name):
                # Variable
                self.output.append(f'diag_log {arg.id};')
            else:
                expr = self._visit_expr(arg)
                self.output.append(f'diag_log {expr};')

    def _is_string_concatenation(self, node: ast.BinOp) -> bool:
        """Check if a binary operation is string concatenation."""
        if isinstance(node.op, ast.Add):
            # Check if both sides are strings or string operations
            left_is_str = isinstance(node.left, ast.Str) or (
                isinstance(node.left, ast.BinOp) and self._is_string_concatenation(node.left)
            )
            right_is_str = isinstance(node.right, ast.Str) or (
                isinstance(node.right, ast.BinOp) and self._is_string_concatenation(node.right)
            )
            return left_is_str and right_is_str
        return False

    def _extract_string_parts(self, node: ast.BinOp) -> list:
        """Extract parts from string concatenation."""
        parts = []
        if isinstance(node.left, ast.Str):
            parts.append(f'"{node.left.s}"')
        elif isinstance(node.left, ast.BinOp):
            parts.extend(self._extract_string_parts(node.left))
        else:
            parts.append(self._visit_expr(node.left))

        if isinstance(node.right, ast.Str):
            parts.append(f'"{node.right.s}"')
        elif isinstance(node.right, ast.BinOp):
            parts.extend(self._extract_string_parts(node.right))
        else:
            parts.append(self._visit_expr(node.right))

        return parts

    def _handle_len(self, node: ast.Call) -> None:
        """Handle len() calls - convert to count with proper SQF syntax."""
        if node.args:
            arg = node.args[0]
            expr = self._visit_expr(arg)
            self.output.append(f"(count {expr})")

    def _handle_range(self, node: ast.Call) -> None:
        """Handle range() calls - convert to SQF for loop."""
        if node.args:
            arg = node.args[0]
            if isinstance(arg, ast.Num):
                # For now, just output the range call - needs loop context
                end_val = int(arg.n) - 1
                self.output.append(f"0 to {end_val}")
            elif isinstance(arg, ast.Constant):
                try:
                    end_val = int(arg.value) - 1
                    self.output.append(f"0 to {end_val}")
                except (ValueError, TypeError):
                    expr = self._visit_expr(arg)
                    self.output.append(f"0 to ({expr} - 1)")
            elif isinstance(arg, ast.Name):
                self.output.append(f"0 to ({arg.id} - 1)")
            else:
                expr = self._visit_expr(arg)
                self.output.append(f"0 to ({expr} - 1)")

    def _handle_enumerate(self, node: ast.Call) -> None:
        """Handle enumerate() function - convert to SQF index-based iteration."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # In SQF, we can create index-value pairs
            # For now, return the original array (enumerate behavior is handled in for loops)
            self.output.append(arg)
        else:
            self.output.append("[]")

    def _handle_zip(self, node: ast.Call) -> None:
        """Handle zip() function - combine multiple arrays."""
        if node.args:
            # Convert arguments to expressions
            args_expr = [self._visit_expr(arg) for arg in node.args]
            args_str = ", ".join(args_expr)
            # In SQF, we don't have a direct zip equivalent, but we can simulate it
            # For now, just return the first array (this is a simplification)
            self.output.append(f"({args_expr[0]}) // zip({args_str}) - simplified")
        else:
            self.output.append("[]")

    def _handle_reversed(self, node: ast.Call) -> None:
        """Handle reversed() function - reverse array order."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # SQF has reverse command
            self.output.append(f"reverse {arg}")
        else:
            self.output.append("reverse []")

    def _handle_isinstance(self, node: ast.Call) -> None:
        """Handle isinstance() function - type checking."""
        if len(node.args) >= 2:
            obj_expr = self._visit_expr(node.args[0])
            type_arg = node.args[1]

            if isinstance(type_arg, ast.Name):
                type_name = type_arg.id
                # Basic type checking - this is simplified
                if type_name in ['int', 'float', 'str', 'list', 'dict']:
                    self.output.append(f"(typeName {obj_expr} == {type_name})")
                else:
                    self.output.append(f"(typeName {obj_expr} == {type_name}) // isinstance check")
            else:
                type_expr = self._visit_expr(type_arg)
                self.output.append(f"(typeName {obj_expr} == {type_expr}) // isinstance check")
        else:
            self.output.append("false // isinstance needs 2 arguments")

    def _handle_str(self, node: ast.Call) -> None:
        """Handle str() function - convert to string."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            self.output.append(f"str {arg}")
        else:
            self.output.append('""')

    def _handle_int(self, node: ast.Call) -> None:
        """Handle int() function - convert to integer."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # SQF parseNumber can convert strings to numbers
            self.output.append(f"(parseNumber {arg})")
        else:
            self.output.append("0")

    def _handle_float(self, node: ast.Call) -> None:
        """Handle float() function - convert to float."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # SQF parseNumber can convert strings to numbers
            self.output.append(f"(parseNumber {arg})")
        else:
            self.output.append("0.0")

    def _handle_sum(self, node: ast.Call) -> None:
        """Handle sum() function - sum all elements in array."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # Use SQF's select and apply to sum elements
            self.output.append(f"({arg} call BIS_fnc_arraySum)")
        else:
            self.output.append("0")

    def _handle_max_min(self, node: ast.Call, func_type: str) -> None:
        """Handle max() and min() functions."""
        if node.args:
            if len(node.args) == 1:
                # Single array argument
                arg = self._visit_expr(node.args[0])
                if func_type == "max":
                    self.output.append(f"({arg} call BIS_fnc_arrayMax)")
                else:
                    self.output.append(f"({arg} call BIS_fnc_arrayMin)")
            else:
                # Multiple arguments - find max/min of them
                args_expr = [self._visit_expr(arg) for arg in node.args]
                args_str = ", ".join(args_expr)
                if func_type == "max":
                    self.output.append(f"([ {args_str} ] call BIS_fnc_arrayMax)")
                else:
                    self.output.append(f"([ {args_str} ] call BIS_fnc_arrayMin)")
        else:
            self.output.append("0")

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> str:
        """Handle generator expressions - convert to lazy evaluation."""
        # Generator expressions are similar to list comprehensions but lazy
        # For SQF, we'll treat them similarly to list comprehensions
        if len(node.generators) == 1:
            generator = node.generators[0]
            iter_expr = self._visit_expr(generator.iter)

            # Handle the comprehension element
            elt_expr = self._visit_expr(node.elt)

            # Handle conditions (if clauses)
            conditions = []
            for cond in generator.ifs:
                cond_expr = self._visit_expr(cond)
                conditions.append(cond_expr)

            if conditions:
                # With conditions: select + apply
                condition_str = " && ".join(f"({_cond})" for _cond in conditions)
                return f"({iter_expr} select {{{condition_str}}} apply {{{elt_expr}}})"
            else:
                # Simple comprehension: just apply
                return f"({iter_expr} apply {{{elt_expr}}})"
        else:
            # Multiple generators not supported yet
            return f"[{self._visit_expr(node.elt)}] // Complex generator not fully supported"

    def visit_Set(self, node: ast.Set) -> str:
        """Handle set creation - convert to SQF array (sets not native in SQF)."""
        elements = []
        for elt in node.elts:
            if isinstance(elt, ast.Str):
                elements.append(f'"{elt.s}"')
            elif isinstance(elt, ast.Num):
                elements.append(str(elt.n))
            elif isinstance(elt, ast.Constant):
                if isinstance(elt.value, str):
                    elements.append(f'"{elt.value}"')
                else:
                    elements.append(str(elt.value))
            else:
                elements.append(self._visit_expr(elt))

        # SQF doesn't have native sets, so we return an array
        # Could potentially add deduplication logic
        return f"[{', '.join(elements)}] // Set converted to array"

    def visit_SetComp(self, node: ast.SetComp) -> str:
        """Handle set comprehensions."""
        # Similar to list comprehensions but for sets
        # SQF doesn't have sets, so treat as array comprehension
        if len(node.generators) == 1:
            generator = node.generators[0]
            iter_expr = self._visit_expr(generator.iter)
            elt_expr = self._visit_expr(node.elt)

            conditions = []
            for cond in generator.ifs:
                cond_expr = self._visit_expr(cond)
                conditions.append(cond_expr)

            if conditions:
                condition_str = " && ".join(f"({_cond})" for _cond in conditions)
                return f"({iter_expr} select {{{condition_str}}} apply {{{elt_expr}}}) // Set comprehension"
            else:
                return f"({iter_expr} apply {{{elt_expr}}}) // Set comprehension"
        else:
            return f"[{self._visit_expr(node.elt)}] // Complex set comprehension not supported"

    def _handle_all(self, node: ast.Call) -> None:
        """Handle all() function - check if all elements are truthy."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # In SQF, we can use a combination of select and count
            self.output.append(f"(({arg} select {{!_x}}) isEqualTo [])")
        else:
            self.output.append("true")

    def _handle_any(self, node: ast.Call) -> None:
        """Handle any() function - check if any element is truthy."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # Check if there's at least one truthy element
            self.output.append(f"(count ({arg} select {{_x}}) > 0)")
        else:
            self.output.append("false")

    def _handle_abs(self, node: ast.Call) -> None:
        """Handle abs() function - absolute value."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            self.output.append(f"(abs {arg})")
        else:
            self.output.append("0")

    def _handle_round(self, node: ast.Call) -> None:
        """Handle round() function - round to nearest integer."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            if len(node.args) >= 2:
                # Round to specified decimal places (simplified)
                ndigits = self._visit_expr(node.args[1])
                self.output.append(f"(round ({arg} * (10 ^ {ndigits})) / (10 ^ {ndigits}))")
            else:
                # Round to nearest integer
                self.output.append(f"(round {arg})")
        else:
            self.output.append("0")

    def _handle_bool(self, node: ast.Call) -> None:
        """Handle bool() function - convert to boolean."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # In SQF, most values are truthy, but we can check for specific falsy values
            self.output.append(f"({arg} isNotEqualTo false && {{!isNil '{arg}'}})")
        else:
            self.output.append("false")

    def _handle_random(self, node: ast.Call) -> None:
        """Handle random module calls."""
        # This would be handled by attribute calls, but placeholder
        self.output.append("random")

    def _handle_random_uniform(self, node: ast.Call) -> None:
        """Handle random.uniform() - convert to SQF random."""
        if node.args and len(node.args) >= 2:
            min_val = self._visit_expr(node.args[0])
            max_val = self._visit_expr(node.args[1])
            self.output.append(f"{min_val} + (random ({max_val} - {min_val}))")

    def _handle_random_choice(self, node: ast.Call) -> None:
        """Handle random.choice() - convert to SQF select."""
        if node.args:
            arg = node.args[0]
            arg_str = self._visit_expr(arg)
            self.output.append(f"{arg_str} select (floor random count {arg_str})")

    def _handle_math_sqrt(self, node: ast.Call) -> None:
        """Handle math.sqrt() - convert to SQF sqrt."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            self.output.append(f"sqrt {arg}")

    def _handle_math_sin(self, node: ast.Call) -> None:
        """Handle math.sin() - convert to SQF sin (but SQF sin expects degrees)."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # SQF sin expects degrees, Python sin expects radians
            # Convert radians to degrees: arg * 180 / PI
            self.output.append(f"sin ({arg} * 180 / 3.14159265359)")

    def _handle_math_cos(self, node: ast.Call) -> None:
        """Handle math.cos() - convert to SQF cos."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # Convert radians to degrees
            self.output.append(f"cos ({arg} * 180 / 3.14159265359)")

    def _handle_math_tan(self, node: ast.Call) -> None:
        """Handle math.tan() - convert to SQF tan."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            # Convert radians to degrees
            self.output.append(f"tan ({arg} * 180 / 3.14159265359)")

    def _handle_math_asin(self, node: ast.Call) -> None:
        """Handle math.asin() - convert to SQF asin."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            self.output.append(f"asin {arg}")

    def _handle_math_acos(self, node: ast.Call) -> None:
        """Handle math.acos() - convert to SQF acos."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            self.output.append(f"acos {arg}")

    def _handle_math_atan(self, node: ast.Call) -> None:
        """Handle math.atan() - convert to SQF atan."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            self.output.append(f"atan {arg}")

    def _handle_math_atan2(self, node: ast.Call) -> None:
        """Handle math.atan2() - convert to SQF atan2."""
        if len(node.args) >= 2:
            y = self._visit_expr(node.args[0])
            x = self._visit_expr(node.args[1])
            self.output.append(f"atan2 ({y}, {x})")

    def _handle_math_floor(self, node: ast.Call) -> None:
        """Handle math.floor() - convert to SQF floor."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            self.output.append(f"floor {arg}")

    def _handle_math_ceil(self, node: ast.Call) -> None:
        """Handle math.ceil() - convert to SQF ceil."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            self.output.append(f"ceil {arg}")

    def _handle_math_pow(self, node: ast.Call) -> None:
        """Handle math.pow() - convert to SQF ^ operator."""
        if len(node.args) >= 2:
            base = self._visit_expr(node.args[0])
            exp = self._visit_expr(node.args[1])
            self.output.append(f"({base} ^ {exp})")

    def _handle_math_log(self, node: ast.Call) -> None:
        """Handle math.log() - convert to SQF ln."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            self.output.append(f"ln {arg}")

    def _handle_math_exp(self, node: ast.Call) -> None:
        """Handle math.exp() - convert to SQF exp."""
        if node.args:
            arg = self._visit_expr(node.args[0])
            self.output.append(f"exp {arg}")

    def _handle_random_random(self, node: ast.Call) -> None:
        """Handle random.random() - convert to SQF random."""
        self.output.append("random 1")

    def _handle_random_randint(self, node: ast.Call) -> None:
        """Handle random.randint() - convert to SQF floor random."""
        if len(node.args) >= 2:
            min_val = self._visit_expr(node.args[0])
            max_val = self._visit_expr(node.args[1])
            self.output.append(f"({min_val} + floor random ({max_val} - {min_val} + 1))")

    def _handle_random_seed(self, node: ast.Call) -> None:
        """Handle random.seed() - not directly supported in SQF."""
        self._add_line("// Warning: random.seed() not supported in SQF")

    def _handle_random_shuffle(self, node: ast.Call) -> None:
        """Handle random.shuffle() - not directly supported in SQF."""
        self._add_line("// Warning: random.shuffle() not supported in SQF")

    def _handle_random_sample(self, node: ast.Call) -> None:
        """Handle random.sample() - not directly supported in SQF."""
        self._add_line("// Warning: random.sample() not supported in SQF")

    def _handle_json_loads(self, node: ast.Call) -> None:
        """Handle json.loads() - convert to SQF parseSimpleArray or similar."""
        if node.args:
            json_str = self._visit_expr(node.args[0])
            # In SQF, we can use parseSimpleArray for basic JSON-like structures
            self.output.append(f"parseSimpleArray {json_str}")
        else:
            self.output.append("parseSimpleArray")

    def _handle_json_dumps(self, node: ast.Call) -> None:
        """Handle json.dumps() - convert to SQF str representation."""
        if node.args:
            data = self._visit_expr(node.args[0])
            # SQF has str command for basic string conversion
            self.output.append(f"str {data}")
        else:
            self.output.append("str nil")

    def visit_Assign(self, node: ast.Assign) -> None:
        """Handle variable assignments."""
        if len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                var_name = target.id
                value = self._visit_expr(node.value)
                if value:  # Only assign if we have a value
                    self._add_variable(var_name)  # Track the variable
                    self._add_line(f"{var_name} = {value};")
                else:
                    self._add_variable(var_name)
                    self._add_line(f"{var_name} = unknown;")
            elif isinstance(target, ast.Attribute):
                # Handle self.attribute = value using MEMBER macro
                obj_name = target.value.id if isinstance(target.value, ast.Name) else "unknown"
                if obj_name == "self" and self.current_class:
                    attr = target.attr
                    value = self._visit_expr(node.value)
                    if value:
                        self._add_line(f'MEMBER("{attr}",{value});')
                    else:
                        self._add_line(f'MEMBER("{attr}",unknown);')
                    # Track instance variable
                    self.classes[self.current_class]['instance_vars'].add(attr)

    def visit_List(self, node: ast.List) -> str:
        """Handle list creation and return SQF array syntax."""
        elements = []
        for elt in node.elts:
            if isinstance(elt, ast.Str):
                elements.append(f'"{elt.s}"')
            elif isinstance(elt, ast.Num):
                elements.append(str(elt.n))
            elif isinstance(elt, ast.Constant):
                if isinstance(elt.value, str):
                    elements.append(f'"{elt.value}"')
                else:
                    elements.append(str(elt.value))
            else:
                elements.append(self._visit_expr(elt))

        return f"[{', '.join(elements)}]"

    def visit_ListComp(self, node: ast.ListComp) -> str:
        """Handle list comprehensions by converting to SQF array operations."""
        # List comprehensions are complex in SQF
        # We'll convert them to a combination of select/filter operations

        # For now, implement a basic version
        # [x*2 for x in items if x > 0] becomes something like:
        # items select {_x > 0} apply {_x * 2}

        if len(node.generators) == 1:
            generator = node.generators[0]
            iter_expr = self._visit_expr(generator.iter)

            # Handle the comprehension element
            elt_expr = self._visit_expr(node.elt)

            # Handle conditions (if clauses)
            conditions = []
            for cond in generator.ifs:
                cond_expr = self._visit_expr(cond)
                conditions.append(cond_expr)

            if conditions:
                # With conditions: select + apply
                condition_str = " && ".join(f"({_cond})" for _cond in conditions)
                return f"({iter_expr} select {{{condition_str}}} apply {{{elt_expr}}})"
            else:
                # Simple comprehension: just apply
                return f"({iter_expr} apply {{{elt_expr}}})"
        else:
            # Multiple generators not supported yet
            return f"[{self._visit_expr(node.elt)}] // Complex comprehension not fully supported"

    def visit_Dict(self, node: ast.Dict) -> str:
        """Handle dictionary literals - convert to SQF arrays of pairs."""
        if not node.keys:
            return "[]"

        pairs = []
        for key, value in zip(node.keys, node.values):
            if key is None:
                continue  # Skip ** unpacking for now

            if isinstance(key, ast.Str):
                key_str = f'"{key.s}"'
            elif isinstance(key, ast.Num):
                key_str = str(key.n)
            else:
                key_str = self._visit_expr(key)

            value_str = self._visit_expr(value)
            pairs.append(f"[{key_str}, {value_str}]")

        return f"[{', '.join(pairs)}]"

    def visit_If(self, node: ast.If) -> None:
        """Handle if statements."""
        # Convert condition
        condition = self._visit_expr(node.test)

        self._add_line(f"if ({condition}) then {{")
        self.indent_level += 1

        for stmt in node.body:
            self.visit(stmt)

        self.indent_level -= 1
        if node.orelse:
            self._add_line("} else {")
            self.indent_level += 1

            for stmt in node.orelse:
                self.visit(stmt)

            self.indent_level -= 1
        self._add_line("};")

    def visit_For(self, node: ast.For) -> None:
        """Handle for loops."""
        loop_var = "_i"  # Default loop variable

        # Add loop variable to scope
        if isinstance(node.target, ast.Name):
            loop_var = node.target.id
            self._add_variable(loop_var, f"_{loop_var}")  # Use underscore prefix for SQF

        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":
            # Handle for i in range(n)
            range_call = node.iter
            if range_call.args:
                range_arg = self._visit_expr(range_call.args[0])
                loop_var_sqf = self._resolve_variable(loop_var)
                self._add_line(f"for \"{loop_var_sqf}\" from 0 to ({range_arg} - 1) do {{")
                self.indent_level += 1

                for stmt in node.body:
                    self.visit(stmt)

                self.indent_level -= 1
                self._add_line("};")
        else:
            # Generic for loop - convert to forEach
            iter_expr = self._visit_expr(node.iter)
            self._add_line("{ // for loop")
            self.indent_level += 1

            for stmt in node.body:
                self.visit(stmt)

            self.indent_level -= 1
            self._add_line(f"}} forEach {iter_expr};")

    def visit_Try(self, node: ast.Try) -> None:
        """Handle try/except blocks using SQF error handling patterns."""
        # In SQF, we'll use a variable to track if an "exception" occurred
        exception_var = f"_exception_{id(node)}"
        self._add_variable(exception_var, exception_var)
        self._add_line(f"{exception_var} = nil; // Exception tracking")

        self._add_line("// Try block")
        self._push_scope()

        # Handle the try body with exception simulation
        for stmt in node.body:
            # Wrap each statement in error checking
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                # For function calls, we can check return values
                func_name = "unknown"
                if isinstance(stmt.value.func, ast.Name):
                    func_name = stmt.value.func.id

                # Special handling for known error-prone functions
                if func_name in ["int", "float", "len"]:
                    self._add_line(f"// Safe call to {func_name}")
                    self.visit_Expr(stmt)
                else:
                    self.visit_Expr(stmt)
            else:
                self.visit(stmt)

        self._pop_scope()

        # Handle except handlers
        for i, handler in enumerate(node.handlers):
            exception_type = "any"
            if handler.type and isinstance(handler.type, ast.Name):
                exception_type = handler.type.id

            # Check if we have an exception (simulated)
            self._add_line(f"// Except block for {exception_type}")
            self._add_line(f"if (!isNil \"{exception_var}\") then {{")

            self.indent_level += 1

            if handler.name:
                # Exception variable
                exc_var = handler.name
                self._add_variable(exc_var, exc_var)
                self._add_line(f"{exc_var} = {exception_var};")

            # Handle the except body
            self._push_scope()
            for stmt in handler.body:
                self.visit(stmt)
            self._pop_scope()

            # Clear the exception
            self._add_line(f"{exception_var} = nil;")

            self.indent_level -= 1
            self._add_line("};")

        # Handle finally block
        if node.finalbody:
            self._add_line("// Finally block")
            for stmt in node.finalbody:
                self.visit(stmt)

    def visit_With(self, node: ast.With) -> None:
        """Handle with statements (context managers)."""
        # With statements are tricky in SQF since it doesn't have context managers
        # We'll implement them as try/finally blocks

        self._add_line("// With statement (context manager)")
        self._push_scope()

        # Handle the context managers
        for item in node.items:
            if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                # Variable assignment from context manager
                var_name = item.optional_vars.id
                self._add_variable(var_name, var_name)
                context_expr = self._visit_expr(item.context_expr)
                self._add_line(f"{var_name} = {context_expr}; // Context manager")
            else:
                # Context manager without variable
                context_expr = self._visit_expr(item.context_expr)
                self._add_line(f"// Context manager: {context_expr}")

        # Handle the body
        for stmt in node.body:
            self.visit(stmt)

        self._pop_scope()
        self._add_line("// End with statement")

    def visit_Lambda(self, node: ast.Lambda) -> str:
        """Handle lambda expressions by converting to SQF functions."""
        # Lambda functions become inline SQF functions
        # Get parameter names
        params = []
        if node.args.args:
            for arg in node.args.args:
                params.append(arg.arg)

        param_str = ", ".join(params) if params else ""

        # Create a function body from the lambda expression
        # Lambdas in SQF are typically handled as inline code
        lambda_id = f"_lambda_{id(node)}"

        # For now, we'll create a simple inline function
        # More complex lambdas would need proper function definition
        body_expr = self._visit_expr(node.body)

        if len(params) == 1:
            # Single parameter lambda: lambda x: x*2
            return f"{{{params[0]} {{ {body_expr} }} }}"
        else:
            # Multi-parameter lambda
            return f"{{{param_str} {{ {body_expr} }} }}"

    def visit_Break(self, node: ast.Break) -> None:
        """Handle break statements in loops."""
        self._add_line("// Break statement - not directly supported in SQF")
        self._add_line("// Consider restructuring the loop logic")

    def visit_Continue(self, node: ast.Continue) -> None:
        """Handle continue statements in loops."""
        self._add_line("// Continue statement - not directly supported in SQF")
        self._add_line("// Consider restructuring the loop logic")

    def visit_Assert(self, node: ast.Assert) -> None:
        """Handle assert statements - convert to SQF assertions."""
        test_expr = self._visit_expr(node.test)

        if node.msg:
            msg_expr = self._visit_expr(node.msg)
            self._add_line(f"assert({test_expr}); // {msg_expr}")
        else:
            self._add_line(f"assert({test_expr});")

    def visit_Raise(self, node: ast.Raise) -> None:
        """Handle raise statements - convert to SQF error handling."""
        if node.exc:
            exc_msg = self._visit_expr(node.exc)
            # Set exception variable and log
            self._add_line(f'diag_log format ["Exception: %1", {exc_msg}];')
            # In SQF context, we might set a global error flag
            self._add_line(f'missionNamespace setVariable ["_last_error", {exc_msg}];')
        else:
            self._add_line('diag_log "Exception re-raised";')

    def visit_Subscript(self, node: ast.Subscript) -> str:
        """Handle subscript access like dict[key] or list[index] with proper SQF syntax."""
        value = self._visit_expr(node.value)
        if isinstance(node.slice, ast.Index):
            # list[index] or dict[key] - use select command
            index_expr = getattr(node.slice, 'value', None)
            if index_expr:
                index = self._visit_expr(index_expr)
                return f"({value} select {index})"
        elif isinstance(node.slice, ast.Constant):
            # Handle dict['key'] style access
            if isinstance(node.slice.value, str):
                key = node.slice.value
                # For our data structures, we need to handle dictionary access
                # In SQF, we can use the get command for associative arrays
                return f"({value} get '{key}')"
        return f"({value} select 0)"  # Default fallback with proper parentheses

    def _visit_expr(self, node: ast.AST) -> str:
        """Visit an expression and return its string representation."""
        if isinstance(node, ast.Compare):
            left = self._visit_expr(node.left)
            op = self._cmp_op_to_sqf(node.ops[0])
            right = self._visit_expr(node.comparators[0])
            return f"{left} {op} {right}"
        elif isinstance(node, ast.Name):
            return self._resolve_variable(node.id)
        elif isinstance(node, ast.Num):
            return str(node.n)
        elif isinstance(node, ast.Str):
            return f'"{node.s}"'
        elif isinstance(node, ast.Constant):
            # Handle Python 3.8+ ast.Constant (preferred over deprecated ast.Str/ast.Num)
            if isinstance(node.value, str):
                return f'"{node.value}"'
            else:
                return str(node.value)
        elif isinstance(node, ast.JoinedStr):
            # Handle f-strings and other joined strings
            parts = []
            for value in node.values:
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    parts.append(f'"{value.value}"')
                elif isinstance(value, ast.FormattedValue):
                    # F-string interpolation
                    expr = self._visit_expr(value.value)
                    parts.append(f'str({expr})')
                else:
                    parts.append(self._visit_expr(value))
            return " + ".join(parts)
            # Handle Python 3.8+ ast.Constant
            if isinstance(node.value, str):
                return f'"{node.value}"'
            else:
                return str(node.value)
        elif isinstance(node, ast.Attribute):
            obj_name = node.value.id if isinstance(node.value, ast.Name) else "unknown"
            if obj_name == "self" and self.current_class:
                # Use MEMBER macro for reading self attributes
                return f'MEMBER("{node.attr}",nil)'
            else:
                # For non-self attributes, use direct access
                if obj_name == "self":
                    obj = "this"
                else:
                    obj = obj_name
                return f"{obj}.{node.attr}"
        elif isinstance(node, ast.List):
            return self.visit_List(node)
        elif isinstance(node, ast.ListComp):
            return self.visit_ListComp(node)
        elif isinstance(node, ast.GeneratorExp):
            return self.visit_GeneratorExp(node)
        elif isinstance(node, ast.Set):
            return self.visit_Set(node)
        elif isinstance(node, ast.SetComp):
            return self.visit_SetComp(node)
        elif isinstance(node, ast.Dict):
            return self.visit_Dict(node)
        elif isinstance(node, ast.Lambda):
            return self.visit_Lambda(node)
        elif isinstance(node, ast.Call):
            # Handle function calls in expressions
            original_output = self.output
            self.output = []
            self.visit_Call(node)
            result = "".join(self.output).strip()
            self.output = original_output
            return result
        elif isinstance(node, ast.BinOp):
            left = self._visit_expr(node.left)
            op = self._bin_op_to_sqf(node.op)
            right = self._visit_expr(node.right)
            return f"({left} {op} {right})"
        else:
            return "unknown"

    def _bin_op_to_sqf(self, op: ast.operator) -> str:
        """Convert Python binary operators to SQF."""
        if isinstance(op, ast.Add):
            return "+"
        elif isinstance(op, ast.Sub):
            return "-"
        elif isinstance(op, ast.Mult):
            return "*"
        elif isinstance(op, ast.Div):
            return "/"
        elif isinstance(op, ast.Mod):
            return "%"
        else:
            return "+"  # Default

    def _cmp_op_to_sqf(self, op: ast.cmpop) -> str:
        """Convert Python comparison operators to SQF."""
        if isinstance(op, ast.Gt):
            return ">"
        elif isinstance(op, ast.Lt):
            return "<"
        elif isinstance(op, ast.GtE):
            return ">="
        elif isinstance(op, ast.LtE):
            return "<="
        elif isinstance(op, ast.Eq):
            return "=="
        elif isinstance(op, ast.NotEq):
            return "!="
        else:
            return "=="  # Default


def transpile_python_to_sqf(source_code: str) -> str:
    """Main entry point for transpiling Python to SQF."""
    transpiler = SQFTranspiler()
    return transpiler.transpile(source_code)