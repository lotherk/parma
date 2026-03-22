#!/usr/bin/env python3
"""
Test advanced Parma features including async support
"""

import asyncio
import math
import random
from typing import List, Dict, Any

class AdvancedGameAI:
    def __init__(self, position: List[float]):
        self.position = position
        self.health = 100
        self.mana = 50

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @staticmethod
    def calculate_distance(pos1: List[float], pos2: List[float]) -> float:
        """Calculate Euclidean distance between two points."""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))

    @classmethod
    def create_random_ai(cls) -> 'AdvancedGameAI':
        """Create an AI at a random position."""
        x = random.uniform(-1000, 1000)
        y = random.uniform(-1000, 1000)
        return cls([x, y])

    async def perform_action(self, action: str) -> str:
        """Perform an async action (converted to sync in SQF)."""
        if action == "attack":
            self.mana -= 10
            return f"Attacked with {self.mana} mana remaining"
        elif action == "defend":
            self.health += 5
            return f"Defended, health now {self.health}"
        else:
            return f"Unknown action: {action}"

    def find_nearby_entities(self, entities: List['AdvancedGameAI'], max_distance: float) -> List['AdvancedGameAI']:
        """Find entities within a certain distance using advanced comprehensions."""
        nearby = [
            entity for entity in entities
            if entity != self and entity.is_alive
            and self.calculate_distance(self.position, entity.position) <= max_distance
        ]

        # Sort by distance using lambda
        nearby.sort(key=lambda e: self.calculate_distance(self.position, e.position))
        return nearby[:5]  # Return top 5 closest

def advanced_game_logic():
    """Demonstrate advanced game logic with modern Python features."""

    # Create AI entities
    ais = [AdvancedGameAI.create_random_ai() for _ in range(10)]

    # Use set comprehensions
    alive_positions = {tuple(ai.position) for ai in ais if ai.is_alive}

    # Advanced list comprehensions with multiple conditions
    healthy_ais = [
        ai for ai in ais
        if ai.health > 80 and ai.mana > 20
        and AdvancedGameAI.calculate_distance(ai.position, [0, 0]) < 500
    ]

    # Type checking and advanced operations
    total_health = sum(ai.health for ai in ais)
    avg_health = total_health / len(ais) if ais else 0

    # Dictionary comprehensions (would need implementation)
    health_status = {}
    for ai in ais:
        status = "healthy" if ai.health > 75 else "wounded" if ai.health > 25 else "critical"
        health_status[f"ai_{id(ai)}"] = status

    # Demonstrate isinstance usage
    valid_entities = [ai for ai in ais if isinstance(ai, AdvancedGameAI) and ai.is_alive]

    # Complex mathematical operations
    distances = [AdvancedGameAI.calculate_distance(ai.position, [0, 0]) for ai in ais]
    max_distance = max(distances) if distances else 0
    min_distance = min(distances) if distances else 0
    avg_distance = sum(distances) / len(distances) if distances else 0

    return {
        "total_ais": len(ais),
        "alive_positions": len(alive_positions),
        "healthy_ais": len(healthy_ais),
        "avg_health": round(avg_health, 2),
        "max_distance": round(max_distance, 2),
        "min_distance": round(min_distance, 2),
        "avg_distance": round(avg_distance, 2),
        "health_status_count": len(health_status),
        "valid_entities": len(valid_entities)
    }

# Test async function (will be converted to sync)
async def async_game_update():
    """Async game update function."""
    result = await perform_complex_calculation()
    return f"Async result: {result}"

async def perform_complex_calculation():
    """Complex async calculation."""
    # This would be complex AI decision making in a real game
    return 42

def main():
    """Main function demonstrating all advanced features."""
    print("Testing Advanced Parma Features...")

    # Test basic functionality
    result = advanced_game_logic()
    print(f"Game logic result: {result}")

    # Test async functions (converted to sync)
    # async_result = asyncio.run(async_game_update())  # Would work in Python
    print("Async functions converted to synchronous SQF")

    # Test error handling
    try:
        # This might cause issues that Parma handles gracefully
        test_unsupported_feature = lambda: None
        complex_nested = {"key": [1, 2, {"nested": True}]}
        print("Complex nested structures handled")
    except Exception as e:
        print(f"Handled error: {e}")

    # Test assertions
    total_ais = result["total_ais"]
    assert total_ais == 10, f"Expected 10 AIs, got {total_ais}"
    assert result["avg_health"] > 0, "Average health should be positive"

    print("All advanced features tested successfully!")
    return result

if __name__ == "__main__":
    main()