import json
import os
import sys
from typing import Any
from urllib.parse import urlparse

import httpx
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JsonLexer

from feditool.cli import ToolContext, templates
from feditool.config import ActorConfig, BearerToken
from feditool.exceptions import ToolError


def http_get(
    url: str,
    *,
    accept: str | None = None,
    actor_config: ActorConfig | None = None,
):
    headers = {"Accept": accept or "application/activity+json, application/ld+json"}
    if actor_config and isinstance(actor_config.credentials, BearerToken):
        headers["Authorization"] = f"Bearer {actor_config.credentials.token}"
    response = httpx.get(
        url,
        headers=headers,
        follow_redirects=True,
        # A lot of development servers use unsigned certs :-()
        verify=False,
        timeout=None,
    )
    raise_for_status(response)
    return response


def http_get_json(url: str):
    response = http_get(url)
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


def get_uri(x: Any):
    if isinstance(x, dict) and "id" in x:
        return x["id"]
    return x


def get_collection_items(
    data: dict | str, items: list = [], max_count: int | None = None
):
    if isinstance(data, str):
        data = http_get_json(data)
    items.extend(data.get("orderedItems", []))
    if max_count and len(items) >= max_count:
        return items[:max_count]
    items.extend(data.get("items", []))
    if max_count and len(items) >= max_count:
        return items[:max_count]
    for key in ["first", "next"]:
        if key in data:
            page_uri = get_uri(data[key])
            items.extend(get_collection_items(page_uri, items, max_count))
            if max_count and len(items) >= max_count:
                return items[:max_count]
    return items


def resolve_actor_uri(context: ToolContext, username: str):
    actor_config = context.instance.get_actor_by_username(username)
    if actor_config:
        return actor_config, actor_config.uri
    if context.instance.actor_uri_template:
        tmpl = templates.from_string(context.instance.actor_uri_template)
        return None, tmpl.render(
            {
                "instance": context.instance,
                "actor": actor_config,
                "username": username,
            }
        )
    raise Exception(f"Cannot resolve actor URI for {username}")


def resolve_uri(context: ToolContext, s: str):
    if not s.startswith("@"):
        return s
    parts = s[1:].split(".")
    actor_name = parts[0]
    actor_config, actor_uri = resolve_actor_uri(context, actor_name)
    if len(parts) > 1:
        data = http_get_json(actor_uri)
        for part in parts[1:]:
            data = data[part]
            if isinstance(data, str):
                data = http_get_json(data)
        return actor_config, get_uri(data)
    return actor_config, actor_uri


def raise_for_status(response: httpx.Response):
    if response.is_error:
        raise ToolError(
            f"Request failed: status={response.status_code}, "
            f"reason={response.reason_phrase}, text={response.text}"
        )
