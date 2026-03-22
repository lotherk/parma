#!/usr/bin/env python3
"""
Parma Examples Validation Script
Validates all examples and generates a comprehensive report
"""

import os
import subprocess
import json
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def validate_example(example_path, sqf_validator_path):
    """Validate a single example"""
    py_file = example_path.with_suffix('.py')
    sqf_file = example_path.with_suffix('.sqf')

    results = {
        'name': example_path.stem,
        'python_exists': py_file.exists(),
        'sqf_exists': sqf_file.exists(),
        'python_runs': False,
        'transpiles': False,
        'sqf_commands': 0,
        'sqf_valid': False
    }

    # Test Python execution
    if results['python_exists']:
        success, stdout, stderr = run_command(f'python3 {py_file.name}', cwd=str(example_path.parent))
        results['python_runs'] = success

    # Test transpilation
    success, stdout, stderr = run_command(f'parma compile {py_file.name}', cwd=str(example_path.parent))
    results['transpiles'] = success and '✓ Compiled' in stdout

    # Validate SQF if it exists
    if results['sqf_exists']:
        success, stdout, stderr = run_command(f'python3 {sqf_validator_path} {sqf_file.name}', cwd=str(example_path.parent))
        if success and 'SQF Commands Found:' in stdout:
            # Extract command count
            for line in stdout.split('\n'):
                if 'SQF Commands Found:' in line:
                    try:
                        results['sqf_commands'] = int(line.split(':')[1].strip())
                    except:
                        pass
            results['sqf_valid'] = results['sqf_commands'] > 0

    return results

def main():
    """Main validation function"""
    examples_dir = Path(__file__).parent
    sqf_validator = examples_dir.parent / 'sqf_validator.py'

    if not sqf_validator.exists():
        print("❌ SQF validator not found!")
        return

    print("🔍 Parma Examples Validation Report")
    print("=" * 50)

    # Find all examples
    examples = []
    for file in examples_dir.glob('*.py'):
        if file.name.startswith(('01_', '02_', '03_', '04_', '05_', '06_', '07_', '08_', '09_', '10_')):
            examples.append(file.with_suffix(''))

    examples.sort()

    results = []
    total_python = 0
    total_transpile = 0
    total_valid = 0

    for example in examples:
        result = validate_example(example, sqf_validator)
        results.append(result)

        status = "✅" if result['python_runs'] and result['transpiles'] and result['sqf_valid'] else "❌"
        print(f"{status} {result['name']}: Python={result['python_runs']}, SQF={result['sqf_commands']} cmds")

        total_python += result['python_runs']
        total_transpile += result['transpiles']
        total_valid += result['sqf_valid']

    print("\n" + "=" * 50)
    print(f"📊 Summary: {len(results)} examples")
    print(f"🐍 Python execution: {total_python}/{len(results)} ({total_python/len(results)*100:.1f}%)")
    print(f"🔄 Transpilation: {total_transpile}/{len(results)} ({total_transpile/len(results)*100:.1f}%)")
    print(f"🎯 SQF validation: {total_valid}/{len(results)} ({total_valid/len(results)*100:.1f}%)")

    # Save detailed results
    with open(examples_dir / 'validation_report.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📄 Detailed report saved to: {examples_dir / 'validation_report.json'}")

if __name__ == "__main__":
    main()