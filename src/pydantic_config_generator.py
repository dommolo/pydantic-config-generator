import configparser
from pathlib import Path
from pydantic import BaseModel
import os
import sys
from typing import Any


def prompt_value(item, group: str = '', environ_as_default: bool = False) -> Any:
    if environ_as_default:
        env_value = os.environ.get(item.name.upper(), None)
        default_value = env_value if env_value else item.default
    else:
        default_value = item.default

    while True:
        msg = f'{group}{item.name}'

        if default_value is not None:
            msg = f'{msg} [{default_value}]'

        elif item.allow_none:
            msg = f'{msg}*'
        
        v = input(f'{msg}: ')

        if v == '':
            if default_value is None and not item.allow_none:
                print(f"Error: {item.name} is required")
                continue

            return default_value

        vv, verr = item.validate(v, {}, loc=item.name)
        if verr:
            print(f"Error: expected {item.type_} but got {type(v)}")
            continue

        return vv


def prompt_config(config: BaseModel, group: str = None, environ_as_default: bool = False) -> BaseModel:
    output = {}

    if group is None:
        group = config.__name__ + '.'

    for key, field in config.__fields__.items():
        if issubclass(field.type_, BaseModel):
            if not field.required:
                s = input(
                    f'{group}{field.name} is optional. Skip? (y/n) [n]: ')
                if s == 'y':
                    continue

            output[key] = prompt_config(
                field.type_, group=f'{group}{field.name}.', environ_as_default=environ_as_default)
        else:
            value = prompt_value(field, group, environ_as_default=environ_as_default)

            if value != field.default:
                output[key] = value

    return output


def prompt(config_class: BaseModel, environ_as_default: bool = False):
    while True:
        try:
            data = prompt_config(config_class, environ_as_default=environ_as_default)
            config_class(**data)
            return data
        except Exception as e:
            print(f"Error: {e}")
            continue


def check_file(file: str):
    if Path(file).is_file():
        confirm = input(f'File {file} already exists, overwrite? (y/n): ')
    else:
        confirm = 'y'

    if confirm != 'y':
        print('Operation cancelled.')
        sys.exit(1)


def write_ini(data: dict, file: str = 'config.ini'):
    def add_section(config: configparser.ConfigParser, group: str = None, subdata: dict = {}):
        if group is not None:
            config.add_section(group)
        for key, value in subdata.items():
            if isinstance(value, dict):
                add_section(config, key, value)
            else:
                config.set(group, key, str(value))

    config = configparser.ConfigParser()
    add_section(config, None, data)

    with open(file, 'w') as f:
        config.write(f)

    print(f'File {file} created successfully.')


def write_env(data: dict, file: str = '.env', group_separator: str = '.', use_uppercase: bool = True):
    def add_group(group: str, subdata: dict):
        output = ''
        for key, value in subdata.items():
            name = key.upper() if use_uppercase else key

            if isinstance(value, dict):
                output += add_group(f'{name}{group_separator}', value)
            else:
                output += f'{group}{name}={value}\n'

        return output

    output = add_group('', data)
    with open(file, 'w') as f:
        f.write(output)

    print(f'File {file} created successfully.')


def create_ini(config: BaseModel, file: str = 'config.ini', environ_as_default: bool = False):
    check_file(file)

    data = prompt(config, environ_as_default)
    write_ini(data, file)


def create_env(config: BaseModel, file: str = '.env', group_separator: str = '.', use_uppercase: bool = True, environ_as_default: bool = False):
    check_file(file)

    data = prompt(config, environ_as_default)
    write_env(data, file, group_separator, use_uppercase)
