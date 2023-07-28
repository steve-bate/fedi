import click

from fedi.commands.mastodon import mastodon as mastodon_group
from fedi.utils import format_json


@mastodon_group.group
def timeline():
    """Access to timeline data"""


@timeline.command()
@click.pass_obj
@click.option("--max-id")
@click.option("--min-id")
@click.option("--since-id")
@click.option("--limit")
@click.option("--only-media", is_flag=True)
@click.option("--remote", is_flag=True)
def public(api: str, max_id, min_id, since_id, limit, only_media, remote):
    """Retrieve basic information about the instance,
    including the URI and administrative contact email."""
    print(
        format_json(
            api.timeline_public(
                max_id,
                min_id,
                since_id,
                limit,
                only_media,
                remote,
            )
        )
    )


@timeline.command()
@click.pass_obj
@click.option("--max-id")
@click.option("--min-id")
@click.option("--since-id")
@click.option("--limit")
@click.option("--only-media", is_flag=True)
def local(api: str, max_id, min_id, since_id, limit, only_media):
    """Retrieve basic information about the instance,
    including the URI and administrative contact email."""
    print(
        format_json(
            api.timeline_local(
                max_id,
                min_id,
                since_id,
                limit,
                only_media,
            )
        )
    )


# TODO Need authorization?
@timeline.command()
@click.pass_obj
@click.option("--max-id")
@click.option("--min-id")
@click.option("--since-id")
@click.option("--limit")
@click.option("--only-media", is_flag=True)
@click.option("--remote", is_flag=True)
@click.argument("hashtag")
def hashtag(api: str, hashtag, max_id, min_id, since_id, limit, only_media, remote):
    """Retrieve basic information about the instance,
    including the URI and administrative contact email."""
    print(
        format_json(
            api.timeline_hashtag(
                hashtag,
                max_id,
                min_id,
                since_id,
                limit,
                only_media,
                remote,
            )
        )
    )
