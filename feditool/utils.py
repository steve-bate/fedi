import json
import os
import sys
from urllib.parse import urlparse

import httpx
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JsonLexer


def get_json(url: str):
    response = httpx.get(
        url,
        headers={"Accept": "application/activity+json, application/ld+json"},
        follow_redirects=True,
    )
    response.raise_for_status()
    return response.json()


def is_absolute_url(s: str):
    try:
        url = urlparse(s)
        return url.netloc != "" and not None
    except:  # noqa
        ...


def is_writing_to_console():
    return os.isatty(sys.stdout.fileno())


def format_json(json_data: dict, use_color: bool | None = None):
    formatted_json = json.dumps(json_data, indent=2)
    if use_color or use_color is None and is_writing_to_console():
        lexer = JsonLexer()
        formatter = TerminalFormatter()
        return highlight(formatted_json, lexer, formatter)
    else:
        return formatted_json


def get_collection_items(
    data: dict | str, items: list = [], max_count: int | None = None
):
    if isinstance(data, str):
        data = get_json(data)
    items.extend(data.get("orderedItems", []))
    if len(items) >= max_count:
        return items[:max_count]
    items.extend(data.get("items", []))
    if len(items) >= max_count:
        return items[:max_count]
    for key in ["first", "next"]:
        if key in data:
            items.extend(get_collection_items(data[key], items, max_count))
            if len(items) >= max_count:
                return items[:max_count]
    return items
