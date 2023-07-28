from fedi.cli import cli


@cli.group("ap")
def activitypub():
    """ActivityPub-specific tools"""
    ...
