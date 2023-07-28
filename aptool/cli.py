import click
import jinja2
import tomllib as toml

templates = jinja2.Environment()


@click.group
@click.pass_context
@click.option("--config", default="aptool.toml", help="Config file path")
def cli(context: click.Context, config: str):
    """ActivityPub Tools"""
    with open(config, "rb") as fp:
        context.obj = toml.load(fp)
