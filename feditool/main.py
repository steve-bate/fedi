import importlib
import os
import sys

import click

from feditool import cli
from feditool.exceptions import ToolError


def _import_commands():
    prefix = os.path.dirname(os.path.realpath(__file__))
    command_path = os.path.join(prefix, "commands")
    for base_dir, _, files in os.walk(command_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                module_name = os.path.splitext(file)[0]
                fqn = os.path.join(
                    base_dir.replace(prefix, os.path.basename(prefix)), module_name
                ).replace("/", ".")
                try:
                    importlib.import_module(fqn)
                except ImportError as e:
                    click.echo(
                        click.style(f"Could not import {fqn}, error={e}", fg="red")
                    )


def main():
    _import_commands()
    try:
        env_prefix = os.path.basename(
            os.path.dirname(os.path.realpath(__file__))
        ).upper()
        cli.cli(auto_envvar_prefix=env_prefix)
    except ToolError as ex:
        click.echo(click.style(ex.args[0], fg="red"))
        sys.exit(1)


if __name__ == "__main__":
    main()
