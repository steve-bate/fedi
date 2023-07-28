from json import JSONDecodeError
from typing import Any
from urllib.parse import urljoin

import click
import httpx

from feditool.cli import templates
from feditool.commands.ap import activitypub
from feditool.utils import format_json, get_collection_items


@activitypub.command
@click.pass_obj
@click.argument("uri")
@click.option(
    "--headers",
    is_flag=True,
    help="Include headers",
)
@click.option(
    "--items",
    type=int,
    default=40,
    show_default=True,
    metavar="MAX_COUNT",
    help="Return collection items",
)
@click.option(
    "--accept",
    default="application/activity+json",
    metavar="MIME_TYPE",
    help="Media type for Accept header",
)
def get(
    config: dict[str, Any],
    uri: str,
    headers: bool,
    accept: str,
    items: int | None = None,
):
    """GET a resource"""
    prefix = config["server"]["prefix"]
    if uri.startswith("@"):
        # actor alias
        uri = templates.from_string(config["actor"]["uri_template"]).render(
            {"prefix": prefix, "username": uri[1:]}
        )
    else:
        uri = urljoin(prefix, uri)

    try:
        response = httpx.get(uri, headers={"Accept": accept})
        if response.is_error:
            click.echo(
                f"Request failed: {response.status_code} {response.reason_phrase}"
            )
        try:
            body = response.json()
            if items and body.get("type") in ["Collection", "OrderedCollection"]:
                body = get_collection_items(body, max_count=items)
        except JSONDecodeError:
            body = response.text
        if headers:
            print(
                format_json(
                    {
                        "headers": {k: v for k, v in response.headers.items()},
                        "body": body,
                    }
                )
            )
        else:
            if not isinstance(body, str):
                print(format_json(body))
            else:
                print(body)
    except Exception as ex:
        click.echo(f"Request failed: {ex.args[0]}")
