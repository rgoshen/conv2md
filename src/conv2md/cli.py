"""CLI module for conv2md - Converts conversations and websites to Markdown."""

import click
from pathlib import Path


@click.command()
@click.option('--input', required=True, help='Input file or URL to convert')
@click.option('--out', default='./out', help='Output directory (default: ./out)')
@click.version_option()
def main(input, out):
    """conv2md: Convert conversations, transcripts, and websites to Markdown.

    This is the foundation CLI interface. Full functionality will be implemented
    in Milestone 1 development phase.
    """
    # Validate input file exists (if not URL)
    if not input.startswith(('http://', 'https://')):
        input_path = Path(input)
        if not input_path.exists():
            click.echo(f"Error: Input file '{input}' not found", err=True)
            raise click.Abort()
    
    click.echo("conv2md CLI - Foundation Phase")
    click.echo("Full functionality coming in Milestone 1!")
    click.echo("Use --help for available options.")


if __name__ == "__main__":
    main()
