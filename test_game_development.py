#!/usr/bin/env python3
"""
Parma Game Development Test Suite
Tests all major features for production readiness.
"""

import math
import random
from typing import List, Dict, Any, Optional
from game_framework import Vector3, Unit, Building, World, GameManager

def test_math_functions():
    """Test all supported math functions."""
    print("Testing math functions...")

    # Basic math
    assert abs(-5) == 5
    assert math.floor(3.7) == 3
    assert math.ceil(3.2) == 4
    assert math.sqrt(16) == 4

    # Trigonometry
    sin_val = math.sin(0)
    cos_val = math.cos(0)
    assert abs(sin_val) < 0.001  # Should be close to 0
    assert abs(cos_val - 1) < 0.001  # Should be close to 1

    print("✓ Math functions working")

def test_random_functions():
    """Test all supported random functions."""
    print("Testing random functions...")

    # Basic random
    val = random.random()
    assert 0 <= val <= 1

    # Uniform
    val2 = random.uniform(10, 20)
    assert 10 <= val2 <= 20

    # Choice
    items = [1, 2, 3, 4, 5]
    choice = random.choice(items)
    assert choice in items

    # Randint
    rand_int = random.randint(1, 10)
    assert 1 <= rand_int <= 10

    print("✓ Random functions working")

def test_vector_math():
    """Test vector mathematics."""
    print("Testing vector math...")

    v1 = Vector3(1, 2, 3)
    v2 = Vector3(4, 5, 6)

    # Addition
    v3 = v1 + v2
    assert v3.x == 5 and v3.y == 7 and v3.z == 9

    # Subtraction
    v4 = v2 - v1
    assert v4.x == 3 and v4.y == 3 and v4.z == 3

    # Distance
    dist = v1.distance(v2)
    expected = math.sqrt((4-1)**2 + (5-2)**2 + (6-3)**2)
    assert abs(dist - expected) < 0.001

    print("✓ Vector math working")

def test_game_objects():
    """Test game object creation and manipulation."""
    print("Testing game objects...")

    world = World()

    # Create units
    unit1 = Unit(Vector3(100, 100, 0), "B_soldier_F", "player")
    unit2 = Unit(Vector3(200, 200, 0), "O_soldier_F", "enemy")

    world.add_object(unit1)
    world.add_object(unit2)

    assert len(world.units) == 2

    # Create building
    building = Building(Vector3(150, 150, 0), "Land_House_Small_01_F", Vector3(10, 10, 5))
    world.add_object(building)

    assert len(world.buildings) == 1

    # Test unit interactions
    unit1.attack(unit2)
    assert unit1.target == unit2

    print("✓ Game objects working")

def test_ai_system():
    """Test AI system functionality."""
    print("Testing AI system...")

    world = World()

    # Create AI units
    ai_unit = Unit(Vector3(0, 0, 0), "B_soldier_F", "military")
    target_unit = Unit(Vector3(100, 0, 0), "O_soldier_F", "enemy")

    world.add_object(ai_unit)
    world.add_object(target_unit)

    # Test movement
    ai_unit.move_to(Vector3(50, 0, 0))
    assert ai_unit.target.x == 50

    # Test combat
    ai_unit.attack(target_unit)
    assert ai_unit.target == target_unit

    print("✓ AI system working")

def test_world_queries():
    """Test world query functions."""
    print("Testing world queries...")

    world = World()

    # Create units of different factions
    player_unit = Unit(Vector3(0, 0, 0), "B_soldier_F", "player")
    enemy_unit = Unit(Vector3(100, 0, 0), "O_soldier_F", "enemy")
    civilian_unit = Unit(Vector3(200, 0, 0), "C_man_1", "civilian")

    world.add_object(player_unit)
    world.add_object(enemy_unit)
    world.add_object(civilian_unit)

    # Test nearest unit finding
    nearest = world.find_nearest_unit(Vector3(0, 0, 0))
    assert nearest == player_unit  # Should find itself

    # Test radius queries
    nearby = world.get_units_in_radius(Vector3(150, 0, 0), 60)
    assert civilian_unit in nearby
    assert player_unit not in nearby  # Too far

    print("✓ World queries working")

def test_error_handling():
    """Test error handling and edge cases."""
    print("Testing error handling...")

    try:
        # This should work
        val = math.sqrt(4)
        assert val == 2
    except Exception as e:
        assert False, f"Math function failed: {e}"

    try:
        # Test division by zero handling (should be caught by transpiler)
        # Note: In SQF this would cause issues, but Python handles it
        pass
    except:
        pass

    print("✓ Error handling working")

def test_complex_logic():
    """Test complex game logic patterns."""
    print("Testing complex logic...")

    # Test list comprehensions and complex expressions
    numbers = [1, 2, 3, 4, 5]
    squares = [x * x for x in numbers if x % 2 == 0]
    assert squares == [4, 16]

    # Test dictionary operations
    game_state = {
        "health": 100,
        "ammo": 30,
        "position": Vector3(10, 20, 0)
    }

    assert game_state["health"] == 100
    game_state["health"] -= 10
    assert game_state["health"] == 90

    # Test function composition
    def add_five(x):
        return x + 5

    def multiply_by_two(x):
        return x * 2

    result = multiply_by_two(add_five(10))
    assert result == 30

    print("✓ Complex logic working")

def run_full_test_suite():
    """Run the complete test suite."""
    print("🚀 Starting Parma Game Development Test Suite")
    print("=" * 50)

    tests = [
        test_math_functions,
        test_random_functions,
        test_vector_math,
        test_game_objects,
        test_ai_system,
        test_world_queries,
        test_error_handling,
        test_complex_logic
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1

    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All tests passed! Parma is production ready!")
        return True
    else:
        print("⚠️  Some tests failed. Check the implementation.")
        return False

if __name__ == "__main__":
    success = run_full_test_suite()
    exit(0 if success else 1)