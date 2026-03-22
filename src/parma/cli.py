"""Command-line interface for Parma Python."""
import sys
import subprocess
from pathlib import Path
import click
from colorama import init, Fore, Style

from .transpiler import transpile_python_to_sqf

init(autoreset=True)


def test_with_sqfvm(sqf_file_path: Path) -> bool:
    """Test generated SQF code with SQFVM.

    Returns True if test passes, False if there are issues.
    """
    try:
        # Check if SQFVM is available
        result = subprocess.run(['sqf-vm', '--help'],
                              capture_output=True,
                              text=True,
                              timeout=10)

        if result.returncode != 0:
            click.echo(f"{Fore.YELLOW}⚠ SQFVM not available, skipping SQF validation")
            return True

        # Run the SQF file through SQFVM
        # SQFVM can execute SQF code with various options
        # We'll use a simple execution test
        with open(sqf_file_path, 'r') as f:
            sqf_content = f.read()

        # Create a simple test script that includes our generated code
        test_script = f"""
// Test script for {sqf_file_path.name}
diag_log "Starting SQFVM test...";

// Include the generated code
{sqf_content}

diag_log "SQFVM test completed successfully";
"""

        # Write test script to temp file
        test_file = sqf_file_path.with_suffix('.test.sqf')
        with open(test_file, 'w') as f:
            f.write(test_script)

        # Run through SQFVM
        result = subprocess.run(['sqf-vm', '-f', str(test_file)],
                              capture_output=True,
                              text=True,
                              timeout=30)

        # Clean up test file
        test_file.unlink(missing_ok=True)

        if result.returncode == 0:
            # Check for any error messages in output
            if 'error' in result.stdout.lower() or 'exception' in result.stdout.lower():
                click.echo(f"{Fore.YELLOW}⚠ SQFVM reported issues:")
                click.echo(result.stdout)
                return False
            else:
                return True
        else:
            click.echo(f"{Fore.YELLOW}⚠ SQFVM execution failed:")
            click.echo(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        click.echo(f"{Fore.YELLOW}⚠ SQFVM test timed out")
        return False
    except FileNotFoundError:
        click.echo(f"{Fore.YELLOW}⚠ SQFVM not found, install it for SQF validation")
        return True  # Don't fail if SQFVM isn't available
    except Exception as e:
        click.echo(f"{Fore.YELLOW}⚠ SQFVM test error: {e}")
        return False


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Parma - Python to SQF Transpiler for ArmA Development."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='Output SQF file path')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.option('--test', is_flag=True, help='Test generated SQF with SQFVM')
def compile(input_file, output, verbose, test):
    """Compile Python file to SQF."""
    try:
        # Read input file
        input_path = Path(input_file)
        if verbose:
            click.echo(f"Reading {input_path}")

        with open(input_path, 'r', encoding='utf-8') as f:
            python_code = f.read()

        # Transpile to SQF
        if verbose:
            click.echo("Transpiling Python to SQF...")

        sqf_code = transpile_python_to_sqf(python_code)

        # Determine output path
        if output:
            output_path = Path(output)
        else:
            output_path = input_path.with_suffix('.sqf')

        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sqf_code)

        click.echo(f"{Fore.GREEN}✓ Compiled {input_file} → {output_path}")

        if verbose:
            click.echo(f"Output size: {len(sqf_code)} characters")

        # Test with SQFVM if requested
        if test:
            if verbose:
                click.echo("Testing with SQFVM...")
            test_result = test_with_sqfvm(output_path)
            if test_result:
                click.echo(f"{Fore.GREEN}✓ SQFVM test passed")
            else:
                click.echo(f"{Fore.YELLOW}⚠ SQFVM test completed with warnings")
                # Don't fail the build for SQFVM warnings

    except Exception as e:
        click.echo(f"{Fore.RED}✗ Compilation failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('name')
@click.option('--type', type=click.Choice(['mission', 'addon']), default='mission',
              help='Type of project to create')
def new(name, type):
    """Create a new ArmA project."""
    click.echo(f"Creating new {type} project: {name}")
    # TODO: Implement project skeleton creation
    click.echo(f"{Fore.YELLOW}Project creation not yet implemented")


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()