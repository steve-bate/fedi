from dataclasses import dataclass

import click
import jinja2

from feditool.config import Configuration, InstanceConfig, load_config
from feditool.exceptions import ConfigError

templates = jinja2.Environment()


@dataclass
class ToolContext:
    config: Configuration
    instance: InstanceConfig


@click.group
@click.pass_context
@click.option("--config", default="feditool.toml", help="Config file path")
@click.option("--instance", help="The target instance name")
def cli(context: click.Context, config: str, instance: str):
    """Fediverse/ActivityPub Tools"""
    tool_config = load_config(config)
    instance_config = tool_config.get_instance(instance)
    if instance_config is None:
        raise ConfigError(f"Unknown instance: {instance}")
    context.obj = ToolContext(config=tool_config, instance=instance_config)
