import click
from mastodon import Mastodon

from fedi.cli import cli


@cli.group
@click.pass_context
@click.argument("api_base_url")
def mastodon(context: click.Context, api_base_url: str):
    """Mastodon-specific tools"""
    context.obj = Mastodon(api_base_url=api_base_url)
