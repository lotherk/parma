# SQF Syntax Reference for Parma Development

This document provides essential SQF (Squirrel) syntax information for improving the Parma Python-to-SQF transpiler. Since the official Bohemia Interactive wiki is currently inaccessible due to anti-bot protection, this reference is compiled from known SQF syntax rules.

## 1. Basic Syntax Rules

### Variables
```sqf
// Variable declaration and assignment
myVariable = 42;
playerName = "John Doe";
isAlive = true;

// Arrays
myArray = [1, 2, 3, "text"];
coordinates = [100, 200, 0];

// Accessing array elements
firstElement = myArray select 0;
lastElement = myArray select ((count myArray) - 1);
```

### Operators
```sqf
// Arithmetic
result = 5 + 3;      // 8
result = 10 - 4;     // 6
result = 3 * 4;      // 12
result = 15 / 3;     // 5

// Comparison
isEqual = (5 == 5);           // true
isGreater = (10 > 5);         // true
isLessOrEqual = (3 <= 3);     // true
notEqual = (5 != 3);          // true

// Logical
bothTrue = (true && true);    // true
eitherTrue = (true || false); // true
notTrue = !true;              // false
```

## 2. Control Structures

### If-Then-Else
```sqf
if (condition) then {
    // code to execute if true
    hint "Condition is true";
} else {
    // code to execute if false
    hint "Condition is false";
};

// Single line if
if (alive player) then { hint "Player is alive"; };
```

### For Loops
```sqf
// Count-based loop
for "_i" from 0 to 9 do {
    hint format["Iteration: %1", _i];
};

// ForEach loop
{
    hint format["Item: %1", _x];
} forEach [1, 2, 3, 4, 5];
```

### While Loops
```sqf
while {condition} do {
    // code
    sleep 1;
};
```

## 3. Functions and Commands

### Built-in Commands
```sqf
// Mathematical
abs -5;                    // 5
sqrt 16;                   // 4
round 3.7;                 // 4
floor 3.9;                 // 3
ceil 3.1;                  // 4

// String operations
format["Hello %1", name];  // "Hello John"
toUpper "hello";           // "HELLO"
toLower "HELLO";           // "hello"

// Array operations
count [1,2,3,4];           // 4
reverse [1,2,3];           // [3,2,1]
myArray pushBack "newItem";
removedItem = myArray deleteAt 0;

// Position/Math operations
player distance target;    // distance in meters
ATLToASL [0,0,0];          // convert position
vectorAdd [1,2,3] [4,5,6]; // [5,7,9]
```

### Custom Functions
```sqf
// Function definition (usually in config)
myFunction = {
    params ["_param1", "_param2"];
    private ["_localVar"];

    _result = _param1 + _param2;
    _result
};

// Function call
_result = [5, 3] call myFunction;
```

## 4. Object-Oriented Programming (OOP)

### Class Definition (using macros)
```sqf
CLASS("MyClass")
    PRIVATE VARIABLE("string","name");
    PUBLIC VARIABLE("scalar","health");

    PUBLIC FUNCTION("array","constructor") {
        MEMBER("name","Default Name");
        MEMBER("health",100);
    };

    PUBLIC FUNCTION("","setName") {
        params ["_newName"];
        MEMBER("name",_newName);
    };

    PUBLIC FUNCTION("string","getName") {
        MEMBER("name",nil)
    };
ENDCLASS
```

### Object Creation and Usage
```sqf
// Create object
myObject = ["new"] call MyClass;

// Call methods
["setName", "John"] call myObject;
_name = "getName" call myObject;

// Access variables
_health = MEMBER("health",nil);
```

## 5. Data Types

### Primitives
```sqf
// Numbers
integer = 42;
float = 3.14159;

// Strings
text = "Hello World";
formatted = format["Value: %1", variable];

// Booleans
isTrue = true;
isFalse = false;

// nil
empty = nil;
```

### Arrays
```sqf
// Simple arrays
numbers = [1, 2, 3, 4, 5];
mixed = [1, "text", true, objNull];

// Nested arrays
matrix = [[1,2], [3,4], [5,6]];
config = [["key1", "value1"], ["key2", "value2"]];

// Array manipulation
array resize 10;           // resize to 10 elements
array set [5, "newValue"]; // set element at index 5
```

### Code Blocks
```sqf
// Anonymous functions
myCode = {
    params ["_x", "_y"];
    _result = _x + _y;
    _result
};

// Executing code
_result = [5, 3] call myCode;

// Scheduling execution
[] spawn myCode;
[] execVM "script.sqf";
```

## 6. Important SQF Conventions

### Naming
```sqf
// Variables
localVar = 5;           // local scope
_globalVar = "value";   // global scope (avoid when possible)

// Functions
fn_myFunction = { ... }; // function variables
BIS_fnc_myFunction = { ... }; // official BIS functions
```

### Error Handling
```sqf
// Try-catch equivalent
_result = call {
    // code that might fail
    if (isNil "_someVar") exitWith { "error" };
    "success"
};
```

### Performance Considerations
```sqf
// Avoid in loops
count myArray;           // O(1) - fast
myArray find item;       // O(n) - slow in loops

// Use local variables
private ["_i", "_item"];
for "_i" from 0 to 999 do {
    _item = myArray select _i;
    // process _item
};
```

## 7. Common SQF Gotchas

### Semicolons
```sqf
// Always use semicolons
x = 5;          // Correct
y = 10          // Wrong - will cause errors

// Even in control structures
if (true) then {
    x = 1;      // Correct
    y = 2       // Wrong
};
```

### Array Bounds
```sqf
arr = [1,2,3];
element = arr select 5;  // Returns nil, no error
// Always check bounds
if ((count arr) > 5) then {
    element = arr select 5;
};
```

### String Operations
```sqf
// Concatenation
fullName = "John" + " " + "Doe";  // Works
// But prefer format for complex strings
message = format["%1 has %2 health", name, health];
```

This reference covers the essential SQF syntax needed for Parma development. Use this to improve transpiler accuracy and ensure generated SQF code follows proper Bohemia Interactive conventions.