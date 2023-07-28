import time
from typing import Any

import click

from feditool.commands.ap import activitypub
from feditool.utils import get_collection_items, get_uri, resolve_uri


class CollectionState:
    def __init__(self, uri, items):
        self.uri = uri
        self.items = items


@activitypub.command
@click.pass_obj
@click.argument("uri", metavar="URI")
def monitor(config: dict[str, Any], uri: str):
    _, uri = resolve_uri(config, uri)
    print(uri)
    items = {get_uri(item) for item in get_collection_items(uri, max_count=None)}
    state = CollectionState(uri, items)
    while True:
        time.sleep(1)
        items = {get_uri(item) for item in get_collection_items(uri, max_count=None)}
        for item in items:
            if item not in state.items:
                print(item)
        state.items = items
