"""Command-line interface for Parma Python."""
import sys
from pathlib import Path
import click
from colorama import init, Fore, Style

from .transpiler import transpile_python_to_sqf

init(autoreset=True)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Parma - Python to SQF Transpiler for ArmA Development."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='Output SQF file path')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def compile(input_file, output, verbose):
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