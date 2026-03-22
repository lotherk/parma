#!/usr/bin/env python3
"""
SQF Command Database for Parma Validation
Extracted from SQF-VBS3 repository (https://github.com/zahngol/SQF-VBS3)
"""

import json
import os

# Core SQF commands extracted from SQF-VBS3 completions
SQF_COMMANDS = {
    # Mathematical functions
    "abs", "acos", "asin", "atan", "atan2", "ceil", "cos", "deg", "exp", "floor",
    "ln", "log", "rad", "round", "sin", "sqrt", "tan",

    # Array operations
    "count", "select", "pushBack", "deleteAt", "find", "resize", "reverse",
    "sort", "apply", "forEach",

    # String operations
    "format", "toLower", "toUpper", "toString",

    # Object creation and manipulation
    "createVehicle", "createUnit", "createGroup", "createMarker", "createTrigger",
    "setPos", "setDir", "setPosASL", "setPosATL", "setDamage", "setFuel",
    "deleteVehicle", "deleteMarker", "deleteWaypoint",

    # AI and unit commands
    "doMove", "doTarget", "doFire", "doStop", "commandMove", "commandTarget",
    "setBehaviour", "setCombatMode", "setSpeedMode", "setFormation",

    # Mission and scripting
    "execVM", "call", "spawn", "sleep", "waitUntil", "diag_log", "hint", "systemChat",

    # Game state and information
    "alive", "side", "faction", "rating", "score", "position", "direction",
    "velocity", "speed", "damage", "fuel", "ammo",

    # Control structures (though these are handled by transpiler)
    "if", "then", "else", "for", "while", "switch", "case", "default",

    # Special functions
    "compile", "preprocessFile", "loadFile", "saveProfileNamespace",
    "getPos", "getDir", "getMarkerPos", "getMarkerColor", "getMarkerType",

    # GUI and display
    "cutText", "titleText", "cutRsc", "cutObj", "cutFadeOut",

    # Multiplayer
    "publicVariable", "publicVariableServer", "addPublicVariableEventHandler",

    # Event handlers
    "addEventHandler", "removeEventHandler", "addMPEventHandler",

    # Sound and effects
    "playSound", "playSound3D", "say", "say2D", "say3D",

    # Weapons and inventory
    "addWeapon", "removeWeapon", "addMagazine", "removeMagazine",
    "addItem", "removeItem", "addUniform", "addVest", "addBackpack",

    # Vehicle operations
    "moveInDriver", "moveInCargo", "moveInTurret", "assignAsDriver",
    "assignAsCargo", "assignAsTurret", "unassignVehicle",

    # Waypoints and AI
    "addWaypoint", "setWaypointPosition", "setWaypointType",
    "setWaypointCombatMode", "setWaypointBehaviour",

    # Markers
    "setMarkerPos", "setMarkerColor", "setMarkerType", "setMarkerSize",
    "setMarkerDir", "setMarkerBrush", "setMarkerShape",

    # Time and date
    "time", "date", "daytime", "setDate", "skipTime", "setTimeMultiplier",

    # Environment
    "setOvercast", "setRain", "setFog", "setWind", "setLightnings",

    # File operations
    "copyFile", "deleteFile", "fileExists", "loadFile", "saveProfileNamespace",

    # Debug and diagnostic
    "diag_fps", "diag_tickTime", "diag_log", "diag_captureFrame",

    # Random and math
    "random", "floor", "ceil", "round", "linearConversion",

    # Type checking
    "typeName", "isNil", "isNull", "isKindOf", "isArray", "isNumber",
    "isString", "isText", "isClass",

    # Mission framework
    "BIS_fnc_spawn", "BIS_fnc_taskCreate", "BIS_fnc_showNotification",

    # Config access
    "configFile", "missionConfigFile", "getNumber", "getText", "getArray",

    # Locality
    "local", "isServer", "isDedicated", "hasInterface", "isMultiplayer",

    # Performance
    "enableSimulation", "setViewDistance", "setTerrainGrid",

    # Advanced features (subset)
    "createAgent", "createSimpleObject", "createSoundSource",
    "drawIcon", "drawLine", "drawEllipse", "drawRectangle",

    # CBA functions (subset - if CBA is used)
    "CBA_fnc_addEventHandler", "CBA_fnc_globalExecute", "CBA_fnc_waitUntilAndExecute",
}

def save_command_database():
    """Save the SQF command database to a JSON file"""
    data = {
        "commands": sorted(list(SQF_COMMANDS)),
        "count": len(SQF_COMMANDS),
        "source": "SQF-VBS3 repository (https://github.com/zahngol/SQF-VBS3)",
        "last_updated": "2024-03-22"
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "sqf_commands.json")

    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(SQF_COMMANDS)} SQF commands to {db_path}")

def load_command_database():
    """Load the SQF command database"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "sqf_commands.json")

    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return set(data["commands"])
    else:
        return SQF_COMMANDS

def validate_sqf_commands(commands):
    """Validate if commands are valid SQF"""
    valid_commands = load_command_database()
    invalid = []
    valid = []

    for cmd in commands:
        if cmd in valid_commands:
            valid.append(cmd)
        else:
            invalid.append(cmd)

    return {
        "valid": valid,
        "invalid": invalid,
        "valid_count": len(valid),
        "invalid_count": len(invalid)
    }

if __name__ == "__main__":
    save_command_database()

    # Test validation
    test_commands = ["diag_log", "createVehicle", "invalidCommand", "setPos", "unknownFunction"]
    result = validate_sqf_commands(test_commands)

    print("\nValidation Results:")
    print(f"Valid commands: {result['valid']}")
    print(f"Invalid commands: {result['invalid']}")
    print(f"Total valid: {result['valid_count']}, Invalid: {result['invalid_count']}")