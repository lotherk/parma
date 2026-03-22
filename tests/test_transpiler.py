"""Unit tests for Parma transpiler."""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from parma.transpiler import transpile_python_to_sqf


class TestTranspiler:
    """Test the core transpilation functionality."""

    def test_basic_function(self):
        """Test basic function transpilation."""
        python_code = """
def hello():
    print("Hello World")
"""
        sqf_code = transpile_python_to_sqf(python_code)

        assert "PUBLIC FUNCTION" in sqf_code
        assert "hello" in sqf_code
        assert "diag_log" in sqf_code

    def test_math_operations(self):
        """Test mathematical operations."""
        python_code = """
def calculate(x, y):
    result = x + y * 2
    return result
"""
        sqf_code = transpile_python_to_sqf(python_code)

        assert "+" in sqf_code
        assert "*" in sqf_code
        assert "PUBLIC FUNCTION" in sqf_code

    def test_random_functions(self):
        """Test random function support."""
        python_code = """
import random

def roll_dice():
    return random.randint(1, 6)
"""
        sqf_code = transpile_python_to_sqf(python_code)

        assert "floor random" in sqf_code or "random" in sqf_code

    def test_math_functions(self):
        """Test math function support."""
        python_code = """
import math

def calculate_distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx*dx + dy*dy)
"""
        sqf_code = transpile_python_to_sqf(python_code)

        assert "sqrt" in sqf_code
        assert "(dx * dx) + (dy * dy)" in sqf_code

    def test_control_flow(self):
        """Test control flow structures."""
        python_code = """
def check_condition(x):
    if x > 10:
        return "big"
    elif x > 5:
        return "medium"
    else:
        return "small"
"""
        sqf_code = transpile_python_to_sqf(python_code)

        assert "if" in sqf_code
        assert "then" in sqf_code
        assert "else" in sqf_code

    def test_loops(self):
        """Test loop structures."""
        python_code = """
def sum_range(n):
    total = 0
    for i in range(n):
        total = total + i
    return total
"""
        sqf_code = transpile_python_to_sqf(python_code)

        assert "for" in sqf_code
        assert "from 0 to" in sqf_code

    def test_string_operations(self):
        """Test string operations."""
        python_code = """
def format_message(name, score):
    message = "Player " + name + " scored " + str(score) + " points"
    return message
"""
        sqf_code = transpile_python_to_sqf(python_code)

        assert "+" in sqf_code
        assert "str " in sqf_code

    def test_list_operations(self):
        """Test list operations."""
        python_code = """
def process_list(items):
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result
"""
        sqf_code = transpile_python_to_sqf(python_code)

        assert "pushBack" in sqf_code or "append" in sqf_code
        assert "forEach" in sqf_code

    def test_class_basic(self):
        """Test basic class transpilation."""
        python_code = """
class SimpleObject:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value
"""
        sqf_code = transpile_python_to_sqf(python_code)

        assert "class" in sqf_code or "SimpleObject" in sqf_code

    def test_game_framework_import(self):
        """Test that game framework can be imported and used."""
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))
            from game_framework import Vector3, Unit, Building, World, GameManager
            # Test basic functionality
            v = Vector3(1, 2, 3)
            assert v.x == 1
            assert v.y == 2
            assert v.z == 3
        except ImportError:
            pytest.skip("Game framework not available")

    def test_advanced_features(self):
        """Test newly added advanced Python features."""
        python_code = """
import math
import random

def advanced_function():
    # Test new built-ins
    numbers = [1, 2, 3, 4, 5]
    total = sum(numbers)
    maximum = max(numbers)
    minimum = min(numbers)
    absolute = abs(-42)
    rounded = round(3.14159)

    # Test type checking
    is_str = isinstance("hello", str)
    is_int = isinstance(42, int)

    # Test all/any
    all_true = all([True, True, True])
    any_true = any([False, True, False])

    # Test reversed
    rev_list = list(reversed(numbers))

    # Test set
    my_set = {1, 2, 3, 2}  # Duplicates should be removed

    # Test lambda
    square = lambda x: x * x
    result = square(5)

    # Test f-string
    message = f"Result: {result}"

    # Test assert
    assert result == 25

    return {
        "total": total,
        "max": maximum,
        "min": minimum,
        "abs": absolute,
        "round": rounded,
        "is_str": is_str,
        "is_int": is_int,
        "all_true": all_true,
        "any_true": any_true,
        "reversed": rev_list,
        "set": my_set,
        "message": message
    }
"""

        sqf_code = transpile_python_to_sqf(python_code)

        # Check that advanced features are present in generated code
        assert "BIS_fnc_arraySum" in sqf_code  # sum function
        assert "BIS_fnc_arrayMax" in sqf_code  # max function
        assert "BIS_fnc_arrayMin" in sqf_code  # min function
        assert "(abs " in sqf_code            # abs function
        assert "round " in sqf_code           # round function
        assert "typeName" in sqf_code         # isinstance
        assert "select {!_x}" in sqf_code   # all function
        assert "select {_x}" in sqf_code    # any function
        assert "reverse " in sqf_code         # reversed function
        assert "{x { (x * x) } }" in sqf_code  # lambda function
        assert "+" in sqf_code                # string concatenation (f-strings)
        assert "assert(" in sqf_code          # assert statement


class TestCLI:
    """Test CLI functionality."""

    def test_cli_import(self):
        """Test that CLI can be imported."""
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
            from parma.cli import main
            assert callable(main)
        except ImportError:
            pytest.fail("CLI module could not be imported")


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_transpilation_pipeline(self):
        """Test complete transpilation of a complex script."""
        python_code = """
import math
import random

def complex_function():
    # Math operations
    angle_rad = math.atan2(10, 5)
    distance = math.sqrt(100 + 25)

    # Random operations
    roll = random.randint(1, 20)
    chance = random.random()

    # Control flow
    if roll > 10:
        result = "success"
    else:
        result = "failure"

    return result

def main():
    result = complex_function()
    print("Result: " + result)
    return result

if __name__ == "__main__":
    main()
"""

        sqf_code = transpile_python_to_sqf(python_code)

        # Check that all expected elements are present
        assert "sqrt" in sqf_code
        assert "atan2" in sqf_code
        assert "floor random" in sqf_code or "random" in sqf_code
        assert "if" in sqf_code
        assert "diag_log" in sqf_code
        assert "PUBLIC FUNCTION" in sqf_code

        # Check that the code is not empty and has reasonable length
        assert len(sqf_code) > 100