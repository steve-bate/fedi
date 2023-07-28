import json
import sys

import click
import httpx

from feditool.commands.ap import activitypub


@activitypub.command
@click.pass_obj
@click.argument("box_uri")
@click.argument("filepaths", nargs=-1)
def post(config: dict, box_uri: str, filepaths: str | None):
    """Post a resource to an inbox or outbox"""
    print(f"{box_uri=}")
    print(f"{filepaths=}")

    def post(data: dict):
        response = httpx.post(
            box_uri,
            json=data,
            headers={"Content-Type": "application/activity+json"},
        )
        response.raise_for_status()

    if len(filepaths) > 0:
        for file in filepaths:
            with open(file) as fp:
                post(json.load(fp))
    else:
        data = json.load(sys.stdin)
        if isinstance(data, dict):
            post(data)
        elif isinstance(data, list):
            for item in data:
                post(item)
