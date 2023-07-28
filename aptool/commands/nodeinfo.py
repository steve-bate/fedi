from urllib.parse import urlparse

import click

from aptool.cli import cli
from aptool.utils import format_json, get_json


@cli.command()
@click.pass_obj
@click.option("--index-only", help="Only show top-level nodeinfo index", is_flag=True)
@click.argument("prefix", required=False, metavar="URL")
def nodeinfo(config: dict, prefix: str, index_only: bool):
    if prefix:
        prefix_url = urlparse(prefix)
        prefix = f"{prefix_url.scheme or 'https'}://{prefix_url.netloc or prefix}"
    else:
        prefix = config["server"]["prefix"]
    nodeinfo_index = get_json(f"{prefix}/.well-known/nodeinfo")
    if index_only:
        print(format_json(nodeinfo_index))
        return
    links = nodeinfo_index.get("links")
    if links:
        link = [link["href"] for link in links if "href" in link][-1]
        print(format_json(get_json(link)))
