import os
import tomllib
from dataclasses import dataclass
from typing import Union

from dacite import from_dict

from fedi.exceptions import ConfigError


@dataclass
class BearerToken:
    token: str


@dataclass
class SignatureKeys:
    public_key: str
    private_key: str


@dataclass
class ActorConfig:
    username: str
    uri: str
    credentials: Union[BearerToken, SignatureKeys]
    token: str | None
    public_key: str | None
    private_key: str | None


@dataclass
class InstanceConfig:
    name: str
    prefix: str
    actor_uri_template: str | None
    actors: list[ActorConfig] | None

    def get_actor_by_username(self, name: str):
        if self.actors:
            for a in self.actors:
                if a.username == name:
                    return a


@dataclass
class Configuration:
    instances: list[InstanceConfig]

    def get_instance(self, name: str):
        for i in self.instances:
            if i.name == name:
                return i


def load_config(configpath: str) -> Configuration:
    if not os.path.exists(configpath):
        raise ConfigError(f"Cannot find config file: {configpath}")
    with open(configpath, "rb") as fp:
        data = tomllib.load(fp)
        return from_dict(data_class=Configuration, data=data)
