"""CLI module for conv2md - Converts conversations and websites to Markdown."""

import click
from pathlib import Path


def validate_input(ctx, param, value):
    """Validate input parameter - handle URLs and file paths."""
    # Pass through URLs untouched
    if value.startswith(("http://", "https://")):
        return value

    # Use click.Path for file validation
    try:
        # Let click.Path handle exists=True, resolve_path=True, readable, etc.
        validated_path = click.Path(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ).convert(value, param, ctx)
        return Path(validated_path)
    except click.BadParameter:
        # Re-raise with our custom message for consistency
        if not Path(value).exists():
            raise click.BadParameter(f"Input file '{value}' not found")
        elif Path(value).is_dir():
            raise click.BadParameter(f"Input '{value}' is a directory, not a file")
        else:
            raise click.BadParameter(f"Input '{value}' is not readable")


@click.command()
@click.option(
    "--input",
    required=True,
    callback=validate_input,
    help="Input file or URL to convert",
)
@click.option(
    "--out",
    default="./out",
    show_default=True,
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    help="Output directory",
)
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
    # Input validation is now handled by the validate_input callback
    # input is either a str (URL) or a resolved Path object
    click.echo(f"Input: {input}")
    click.echo(f"Output: {out}")
    click.echo("conv2md CLI - Foundation Phase")
    click.echo("Full functionality coming in Milestone 1!")
    click.echo("Use --help for available options.")


if __name__ == "__main__":
    main()
