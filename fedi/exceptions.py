class ToolError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class ConfigError(ToolError):
    def __init__(self, msg: str):
        super().__init__(msg)
