# Example 4: Dialogue and Conversation System
# Demonstrates NPC dialogue trees and conversation management

class DialogueSystem:
    def __init__(self):
        self.npcs = {}
        self.conversations = {}
        self.active_conversations = {}

    def add_npc(self, npc_id, name, dialogues=None):
        """Add an NPC with dialogue options"""
        self.npcs[npc_id] = {
            "name": name,
            "dialogues": dialogues or [],
            "current_dialogue": None
        }

    def add_dialogue(self, dialogue_id, npc_id, text, responses=None):
        """Add a dialogue entry for an NPC"""
        dialogue = {
            "id": dialogue_id,
            "npc_id": npc_id,
            "text": text,
            "responses": responses or []
        }

        if npc_id not in self.conversations:
            self.conversations[npc_id] = []
        self.conversations[npc_id].append(dialogue)

        # Add to NPC's dialogues
        if npc_id in self.npcs:
            self.npcs[npc_id]["dialogues"].append(dialogue_id)

    def add_response(self, dialogue_id, response_text, next_dialogue=None, action=None):
        """Add a response option to a dialogue"""
        for npc_conversations in self.conversations.values():
            for dialogue in npc_conversations:
                if dialogue["id"] == dialogue_id:
                    response = {
                        "text": response_text,
                        "next_dialogue": next_dialogue,
                        "action": action
                    }
                    dialogue["responses"].append(response)
                    break

    def start_conversation(self, player_id, npc_id):
        """Start a conversation between player and NPC"""
        if npc_id not in self.npcs or not self.conversations.get(npc_id):
            return None

        conversation = {
            "player_id": player_id,
            "npc_id": npc_id,
            "current_dialogue": self.conversations[npc_id][0]["id"],
            "history": []
        }

        self.active_conversations[player_id] = conversation
        return self.get_current_dialogue(player_id)

    def respond_to_dialogue(self, player_id, response_index):
        """Player responds to current dialogue"""
        if player_id not in self.active_conversations:
            return None

        conversation = self.active_conversations[player_id]
        current_dialogue = self._get_dialogue_by_id(conversation["npc_id"], conversation["current_dialogue"])

        if not current_dialogue or response_index >= len(current_dialogue["responses"]):
            return None

        response = current_dialogue["responses"][response_index]

        # Record in history
        conversation["history"].append({
            "dialogue": current_dialogue["text"],
            "response": response["text"]
        })

        # Execute action if any
        if response["action"]:
            self._execute_action(response["action"])

        # Move to next dialogue
        if response["next_dialogue"]:
            conversation["current_dialogue"] = response["next_dialogue"]
            return self.get_current_dialogue(player_id)
        else:
            # End conversation
            del self.active_conversations[player_id]
            return {"type": "end", "message": "Conversation ended"}

    def get_current_dialogue(self, player_id):
        """Get current dialogue for player"""
        if player_id not in self.active_conversations:
            return None

        conversation = self.active_conversations[player_id]
        dialogue = self._get_dialogue_by_id(conversation["npc_id"], conversation["current_dialogue"])

        if not dialogue:
            return None

        return {
            "type": "dialogue",
            "npc_name": self.npcs[conversation["npc_id"]]["name"],
            "text": dialogue["text"],
            "responses": [r["text"] for r in dialogue["responses"]]
        }

    def _get_dialogue_by_id(self, npc_id, dialogue_id):
        """Get dialogue by ID"""
        if npc_id not in self.conversations:
            return None

        for dialogue in self.conversations[npc_id]:
            if dialogue["id"] == dialogue_id:
                return dialogue
        return None

    def _execute_action(self, action):
        """Execute a dialogue action"""
        # This would trigger game events
        print(f"Executing action: {action}")


# Demo usage
dialogue_system = DialogueSystem()

# Add NPC
dialogue_system.add_npc("merchant", "Village Merchant")

# Add dialogues
dialogue_system.add_dialogue("greeting", "merchant", "Welcome to our village! How can I help you?")
dialogue_system.add_dialogue("shop", "merchant", "What would you like to buy?")
dialogue_system.add_dialogue("goodbye", "merchant", "Safe travels!")

# Add responses
dialogue_system.add_response("greeting", "I'd like to buy something", "shop")
dialogue_system.add_response("greeting", "Just browsing", "goodbye")
dialogue_system.add_response("shop", "Show me weapons", None, "open_weapon_shop")
dialogue_system.add_response("shop", "Never mind", "greeting")

# Start conversation
dialogue = dialogue_system.start_conversation("player1", "merchant")
if dialogue:
    print(f"{dialogue['npc_name']}: {dialogue['text']}")
    for i, response in enumerate(dialogue['responses']):
        print(f"{i+1}. {response}")
else:
    print("Failed to start conversation")

# Player chooses response 1
result = dialogue_system.respond_to_dialogue("player1", 0)
if result and isinstance(result, dict) and result.get("type") == "dialogue":
    print(f"{result['npc_name']}: {result['text']}")