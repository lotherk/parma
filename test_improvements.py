#!/usr/bin/env python3
"""
Test the improved Parma transpiler with new features
"""

import json
from typing import List

def test_try_except():
    """Test try/except blocks"""
    try:
        result = 10 / 2
        return result
    except ZeroDivisionError as e:
        return "error"
    except Exception as e:
        return "unknown error"
    finally:
        print("cleanup")

def test_lambda():
    """Test lambda functions"""
    square = lambda x: x * x
    numbers = [1, 2, 3, 4, 5]
    squares = list(map(square, numbers))
    return squares

def test_list_comprehension():
    """Test list comprehensions"""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    evens = [x for x in numbers if x % 2 == 0]
    doubled = [x * 2 for x in evens]
    return doubled

def test_with_statement():
    """Test with statement (context manager)"""
    # In a real scenario, this might be file handling
    # For demo, we'll simulate it
    with "some_context" as ctx:
        result = f"processing {ctx}"
        return result

def test_json_operations():
    """Test JSON operations"""
    data = {"name": "test", "value": 42, "items": [1, 2, 3]}

    # Serialize
    json_str = json.dumps(data)

    # Deserialize (would fail in SQF, but shows the pattern)
    try:
        parsed = json.loads(json_str)
        return parsed
    except:
        return {"error": "json parsing not available in SQF"}

def test_break_continue():
    """Test break and continue statements"""
    result = []
    for i in range(10):
        if i == 3:
            continue  # Skip 3
        if i == 7:
            break     # Stop at 7
        result.append(i)
    return result

def main():
    """Main test function"""
    print("Testing improved Parma features...")

    # These will be transpiled to show the new capabilities
    try_result = test_try_except()
    lambda_result = test_lambda()
    comp_result = test_list_comprehension()
    with_result = test_with_statement()
    json_result = test_json_operations()
    loop_result = test_break_continue()

    return {
        "try_except": try_result,
        "lambda": lambda_result,
        "comprehension": comp_result,
        "with_statement": with_result,
        "json": json_result,
        "loops": loop_result
    }

if __name__ == "__main__":
    results = main()
    print("Test results:", results)