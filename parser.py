import typing


class ConfigError(Exception):
    pass


def parse_config(file_name: str) -> dict[str, str]:
    try:
        config: dict[str, str] = {}
        f: typing.IO[str] | None = None
        f = open(file_name, "r")
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            config[key] = value
        return config
    except OSError as e:
        raise ConfigError(f"Error opening file '{file_name}': {e}")
    finally:
        if f:
            f.close()
            print(f"File '{file_name}' closed")
