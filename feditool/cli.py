import os

import click
import jinja2
import tomllib as toml

templates = jinja2.Environment()


class ConfigError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


@click.group
@click.pass_context
@click.option("--config", default="feditool.toml", help="Config file path")
def cli(context: click.Context, config: str):
    """Fediverse/ActivityPub Tools"""
    if not os.path.exists(config):
        raise ConfigError(f"Cannot find config file: {config}")
    with open(config, "rb") as fp:
        context.obj = toml.load(fp)
