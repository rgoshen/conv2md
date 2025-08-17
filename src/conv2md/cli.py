"""CLI module for conv2md - Converts conversations and websites to Markdown."""

import click


@click.command()
@click.option('--input', help='Input file or URL to convert')
@click.version_option()
def main(input):
    """conv2md: Convert conversations, transcripts, and websites to Markdown.

    This is the foundation CLI interface. Full functionality will be implemented
    in Milestone 1 development phase.
    """
    click.echo("conv2md CLI - Foundation Phase")
    click.echo("Full functionality coming in Milestone 1!")
    click.echo("Use --help for available options.")


if __name__ == "__main__":
    main()
