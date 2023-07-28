import json
import sys

import click
import httpx

from feditool.cli import ToolContext, templates
from feditool.commands.ap import activitypub
from feditool.config import BearerToken
from feditool.exceptions import ToolError
from feditool.utils import raise_for_status, resolve_uri


@activitypub.command
@click.pass_obj
@click.argument("box_uri")
@click.argument("filepaths", nargs=-1)
def post(context: ToolContext, box_uri: str, filepaths: str | None):
    """Post a resource to an inbox or outbox"""
    actor_config, box_uri = resolve_uri(context, box_uri)
    headers = {"Content-Type": "application/activity+json"}
    if isinstance(actor_config.credentials, BearerToken):
        headers["Authorization"] = f"Bearer {actor_config.credentials.token}"

    def post(text: str):
        tmpl = templates.from_string(text)
        data = json.loads(tmpl.render({"actor": actor_config}))
        response = httpx.post(
            box_uri, json=data, headers=headers, verify=False, timeout=None
        )
        raise_for_status(response)

    if len(filepaths) > 0:
        for file in filepaths:
            with open(file) as fp:
                post(fp.read())
    else:
        data = json.load(sys.stdin)
        if isinstance(data, dict):
            post(data)
        elif isinstance(data, list):
            for item in data:
                post(item)
