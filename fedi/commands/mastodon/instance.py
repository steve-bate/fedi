import click
from mastodon import Mastodon

from fedi.commands.mastodon import mastodon as mastodon_group
from fedi.utils import format_json


@mastodon_group.group
def instance():
    """Instance information"""


@instance.command()
@click.pass_obj
def info(api: str):
    """Retrieve basic information about the instance,
    including the URI and administrative contact email."""
    print(format_json(api.instance()))


@instance.command()
@click.pass_obj
def activity(api: Mastodon):
    """Retrieve activity stats about the instance."""
    print(format_json(api.instance_activity()))


@instance.command()
@click.pass_obj
def peers(api: Mastodon):
    """Retrieve the instances that this instance knows about."""
    print(format_json(api.instance_peers()))


@instance.command()
@click.pass_obj
def health(api: Mastodon):
    """Basic health check. Returns True if healthy, False if not."""
    print(api.instance_health())


@instance.command()
@click.pass_obj
def nodeinfo(api: Mastodon):
    """Retrieves the instance’s nodeinfo information."""
    print(format_json(api.instance_nodeinfo()))


@instance.command()
@click.pass_obj
def rules(api: Mastodon):
    """Retrieves instance rules."""
    print(format_json(api.instance_rules()))
