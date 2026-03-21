# Example 8: Inventory and Item Management
# Demonstrates item handling, inventory systems, and equipment management

class InventorySystem:
    def __init__(self):
        self.player_inventories = {}
        self.item_definitions = {
            "rifle": {"type": "weapon", "weight": 4.5, "slots": 2},
            "pistol": {"type": "weapon", "weight": 1.2, "slots": 1},
            "ammo_556": {"type": "magazine", "weight": 0.5, "slots": 1},
            "medkit": {"type": "medical", "weight": 2.0, "slots": 1},
            "backpack": {"type": "container", "weight": 3.0, "slots": 8},
            "helmet": {"type": "headgear", "weight": 1.5, "slots": 1},
            "vest": {"type": "vest", "weight": 2.5, "slots": 1}
        }

    def create_inventory(self, player_id, max_weight=50, max_slots=20):
        """Create inventory for a player"""
        self.player_inventories[player_id] = {
            "items": {},
            "max_weight": max_weight,
            "max_slots": max_slots,
            "current_weight": 0,
            "used_slots": 0
        }

    def add_item(self, player_id, item_id, quantity=1):
        """Add item to player's inventory"""
        if player_id not in self.player_inventories:
            return False

        inventory = self.player_inventories[player_id]
        item_def = self.item_definitions.get(item_id)

        if not item_def:
            return False

        # Check weight and slot limits
        total_weight = item_def["weight"] * quantity
        total_slots = item_def["slots"] * quantity

        if (inventory["current_weight"] + total_weight > inventory["max_weight"] or
            inventory["used_slots"] + total_slots > inventory["max_slots"]):
            return False

        # Add item
        if item_id not in inventory["items"]:
            inventory["items"][item_id] = 0

        inventory["items"][item_id] += quantity
        inventory["current_weight"] += total_weight
        inventory["used_slots"] += total_slots

        return True

    def remove_item(self, player_id, item_id, quantity=1):
        """Remove item from player's inventory"""
        if player_id not in self.player_inventories:
            return False

        inventory = self.player_inventories[player_id]

        if item_id not in inventory["items"] or inventory["items"][item_id] < quantity:
            return False

        item_def = self.item_definitions[item_id]
        weight_removed = item_def["weight"] * quantity
        slots_removed = item_def["slots"] * quantity

        inventory["items"][item_id] -= quantity
        if inventory["items"][item_id] <= 0:
            del inventory["items"][item_id]

        inventory["current_weight"] -= weight_removed
        inventory["used_slots"] -= slots_removed

        return True

    def transfer_item(self, from_player, to_player, item_id, quantity=1):
        """Transfer item between players"""
        if not self.remove_item(from_player, item_id, quantity):
            return False

        if not self.add_item(to_player, item_id, quantity):
            # Failed to add, put back
            self.add_item(from_player, item_id, quantity)
            return False

        return True

    def get_inventory_contents(self, player_id):
        """Get detailed inventory contents"""
        if player_id not in self.player_inventories:
            return None

        inventory = self.player_inventories[player_id]
        contents = []

        for item_id, quantity in inventory["items"].items():
            item_def = self.item_definitions[item_id]
            contents.append({
                "id": item_id,
                "quantity": quantity,
                "type": item_def["type"],
                "weight": item_def["weight"] * quantity,
                "slots": item_def["slots"] * quantity
            })

        return {
            "contents": contents,
            "total_weight": inventory["current_weight"],
            "max_weight": inventory["max_weight"],
            "used_slots": inventory["used_slots"],
            "max_slots": inventory["max_slots"]
        }

    def has_item(self, player_id, item_id, quantity=1):
        """Check if player has specific item and quantity"""
        if player_id not in self.player_inventories:
            return False

        inventory = self.player_inventories[player_id]
        return inventory["items"].get(item_id, 0) >= quantity


# Demo usage
inventory = InventorySystem()

# Create inventories
inventory.create_inventory("player1", max_weight=40, max_slots=15)
inventory.create_inventory("player2", max_weight=50, max_slots=20)

# Add items
inventory.add_item("player1", "rifle", 1)
inventory.add_item("player1", "ammo_556", 5)
inventory.add_item("player1", "medkit", 2)
inventory.add_item("player1", "helmet", 1)

# Check inventory
contents = inventory.get_inventory_contents("player1")
if contents:
    print(f"Player1 inventory: {len(contents['contents'])} items")
    print(f"Weight: {contents['total_weight']}/{contents['max_weight']}")
    print(f"Slots: {contents['used_slots']}/{contents['max_slots']}")

# Transfer items
success = inventory.transfer_item("player1", "player2", "medkit", 1)
print(f"Item transfer successful: {success}")

# Check item availability
has_rifle = inventory.has_item("player1", "rifle")
print(f"Player1 has rifle: {has_rifle}")