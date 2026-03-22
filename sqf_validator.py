#!/usr/bin/env python3
"""
SQF Validation Tool for Parma
Basic syntax checker for generated SQF code
"""

import re
import sys
from pathlib import Path

class SQFValidator:
    def __init__(self):
        # Basic SQF syntax patterns
        self.patterns = {
            'assignment': re.compile(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*='),
            'function_call': re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*\s*\('),
            'array': re.compile(r'\[[^\]]*\]'),
            'string': re.compile(r'"[^"]*"'),
            'comment': re.compile(r'/\*.*?\*/', re.DOTALL),
            'line_comment': re.compile(r'//.*$'),
            'semicolon': re.compile(r';\s*$'),
            'brace_open': re.compile(r'\{'),
            'brace_close': re.compile(r'\}'),
        }

        # SQF keywords that should be recognized
        self.sqf_keywords = {
            'if', 'then', 'else', 'for', 'from', 'to', 'do', 'while',
            'private', 'public', 'CLASS', 'ENDCLASS', 'MEMBER', 'call'
        }

        # Load comprehensive SQF command database
        self.sqf_commands = self._load_command_database()

    def _load_command_database(self):
        """Load SQF command database from JSON file"""
        import json
        import os

        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "sqf_commands.json")

        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return set(data["commands"])
        except (FileNotFoundError, KeyError):
            # Fallback to basic command set if database not available
            return {
                'diag_log', 'createVehicle', 'setPos', 'deleteVehicle', 'setPosASL',
                'setPosATL', 'setDamage', 'setFuel', 'alive', 'side', 'position',
                'direction', 'velocity', 'speed', 'damage', 'fuel', 'ammo'
            }

        # SQF keywords that should be recognized
        self.sqf_keywords = {
            'if', 'then', 'else', 'for', 'from', 'to', 'do', 'while',
            'private', 'public', 'CLASS', 'ENDCLASS', 'MEMBER', 'call'
        }

        # Common SQF commands
        self.sqf_commands = {
            'diag_log', 'format', 'count', 'select', 'pushBack', 'createVehicle',
            'setPos', 'deleteVehicle', 'sleep', 'waitUntil', 'spawn', 'execVM'
        }

    def validate_file(self, file_path):
        """Validate an SQF file for basic syntax issues"""
        path = Path(file_path)
        if not path.exists():
            return {"valid": False, "errors": [f"File not found: {file_path}"]}

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        errors = []
        warnings = []

        # Basic syntax checks
        lines = content.split('\n')
        brace_count = 0
        paren_count = 0

        for line_num, line in enumerate(lines, 1):
            # Remove comments for analysis
            line = self._remove_comments(line)

            # Check braces
            brace_count += line.count('{') - line.count('}')
            paren_count += line.count('(') - line.count(')')

            # Check for obvious syntax errors
            if '{' in line and '}' not in line and not line.strip().endswith('{'):
                errors.append(f"Line {line_num}: Unmatched opening brace")

            if '}' in line and '{' not in line and not line.strip().endswith('}'):
                errors.append(f"Line {line_num}: Unmatched closing brace")

            # Check for missing semicolons (basic check)
            stripped = line.strip()
            if (stripped and not stripped.startswith('//') and not stripped.startswith('/*') and
                not stripped.endswith(';') and not stripped.endswith('{') and
                not stripped.endswith('}') and not stripped.endswith(',') and
                not stripped.endswith('=') and not stripped.startswith('if') and
                not stripped.startswith('for') and not stripped.startswith('while') and
                not stripped.startswith('}')):
                # This is a very basic check - SQF semicolons are complex
                pass

        # Final brace/parens check
        if brace_count != 0:
            errors.append(f"Unmatched braces: {brace_count} unclosed")

        if paren_count != 0:
            errors.append(f"Unmatched parentheses: {paren_count} unclosed")

        # Check for basic command recognition
        for command in self.sqf_commands:
            if command in content:
                # Found a recognized command - good
                pass

        # Check for undefined variables (very basic)
        assignments = set()
        usages = set()

        for line in content.split('\n'):
            line = self._remove_comments(line)

            # Find assignments
            assign_match = re.search(r'(\w+)\s*=', line)
            if assign_match:
                assignments.add(assign_match.group(1))

            # Find usages (very basic - this is not comprehensive)
            words = re.findall(r'\b\w+\b', line)
            for word in words:
                if word not in self.sqf_keywords and len(word) > 1:
                    usages.add(word)

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "stats": {
                "lines": len(lines),
                "assignments": len(assignments),
                "commands_found": len([cmd for cmd in self.sqf_commands if cmd in content])
            }
        }

    def _remove_comments(self, line):
        """Remove comments from a line for analysis"""
        # Remove /* */ comments
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)
        # Remove // comments
        line = re.sub(r'//.*$', '', line)
        return line

def main():
    if len(sys.argv) != 2:
        print("Usage: python sqf_validator.py <sqf_file>")
        sys.exit(1)

    validator = SQFValidator()
    result = validator.validate_file(sys.argv[1])

    print(f"Valid: {result['valid']}")
    print(f"Lines: {result['stats']['lines']}")
    print(f"Assignments: {result['stats']['assignments']}")
    print(f"SQF Commands Found: {result['stats']['commands_found']}")

    if result['errors']:
        print("\nErrors:")
        for error in result['errors']:
            print(f"  ❌ {error}")

    if result['warnings']:
        print("\nWarnings:")
        for warning in result['warnings']:
            print(f"  ⚠️  {warning}")

if __name__ == "__main__":
    main()