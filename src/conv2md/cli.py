"""CLI module for conv2md - Converts conversations and websites to Markdown."""

import click
from pathlib import Path


@click.command()
@click.option('--input', required=True, help='Input file or URL to convert')
@click.option('--out', default='./out', help='Output directory (default: ./out)')
@click.version_option()
def main(input, out):
    """conv2md: Convert conversations, transcripts, and websites to Markdown.

    Supports JSON conversations, websites, and HTML files with deterministic
    output and comprehensive security validation.

    Examples:
        conv2md --input conversation.json --out ./output
        conv2md --input https://example.com/article --out ./docs
        conv2md --input transcript.json
    
    This is the foundation CLI interface. Full functionality will be implemented
    in Milestone 1 development phase.
    """
    # Validate input file exists (if not URL)
    if not input.startswith(('http://', 'https://')):
        input_path = Path(input)
        
        # Security: Prevent path traversal attacks
        try:
            resolved_path = input_path.resolve()
            if '..' in input_path.parts:
                click.echo(f"Error: Invalid path traversal detected in '{input}'", err=True)
                raise click.Abort()
        except (OSError, ValueError):
            click.echo(f"Error: Invalid path '{input}'", err=True)
            raise click.Abort()
        
        if not input_path.exists():
            click.echo(f"Error: Input file '{input}' not found", err=True)
            raise click.Abort()
    
    click.echo("conv2md CLI - Foundation Phase")
    click.echo("Full functionality coming in Milestone 1!")
    click.echo("Use --help for available options.")


if __name__ == "__main__":
    main()
