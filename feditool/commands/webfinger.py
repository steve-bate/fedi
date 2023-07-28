from urllib.parse import urlparse

import click

from feditool.cli import cli
from feditool.utils import format_json, get_json


@cli.command()
@click.option("--http", help="Don't use SSL", is_flag=True)
@click.option("--uri-only", help="Only show the actor URI", is_flag=True)
@click.argument("account")
def webfinger(account: str, uri_only: bool, http: bool):
    """Retrieves webinfo data."""
    parts = account.split("@")
    if len(parts) != 2:
        print("Invalid account syntax. Should be username@hostname")
    scheme = "http" if http else "https"
    url = f"{scheme}://{parts[1]}/.well-known/webfinger?resource=acct:{account}"
    data = get_json(url)
    if uri_only:
        links = data.get("links")
        if links:
            for link in links:
                if (
                    link.get("rel") == "self"
                    and link.get("type") == "application/activity+json"
                ):
                    print(link.get("href"))
    else:
        print(format_json(data))
