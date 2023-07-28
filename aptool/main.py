import importlib
import os

from aptool import cli


def _import_commands():
    imported_modules = []
    current_directory = os.path.dirname(os.path.realpath(__file__))
    commands_path = os.path.join(current_directory, "commands")

    for file_name in os.listdir(commands_path):
        if file_name.endswith(".py") and file_name != "__init__.py":
            module_name = file_name[:-3]  # Remove the '.py' extension
            full_module_name = f"aptool.commands.{module_name}"
            module = importlib.import_module(full_module_name)
            imported_modules.append(module)


def main():
    _import_commands()
    cli.cli()


if __name__ == "__main__":
    main()
