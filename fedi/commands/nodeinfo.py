from urllib.parse import urlparse

import click

from fedi.cli import cli
from fedi.utils import format_json, http_get_json


@cli.command()
@click.pass_obj
@click.option("--index-only", help="Only show top-level nodeinfo index", is_flag=True)
@click.argument("prefix", required=False, metavar="URL")
def nodeinfo(config: dict, prefix: str, index_only: bool):
    """Retrieves nodeinfo data. By default, it will follow
    the nodeinfo index link to the actual nodeinfo data."""
    if prefix:
        prefix_url = urlparse(prefix)
        prefix = f"{prefix_url.scheme or 'https'}://{prefix_url.netloc or prefix}"
    else:
        prefix = config["server"]["prefix"]
    nodeinfo_index = http_get_json(f"{prefix}/.well-known/nodeinfo")
    if index_only:
        print(format_json(nodeinfo_index))
        return
    links = nodeinfo_index.get("links")
    if links:
        link = [link["href"] for link in links if "href" in link][-1]
        print(format_json(http_get_json(link)))
