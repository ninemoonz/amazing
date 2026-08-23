from src.error_class import ConfigError


def parse_config(file_name: str) -> dict[str, str]:
    config: dict[str, str] = {}
    with open(file_name) as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if line == "" or line.startswith("#"):
                continue
            if "=" not in line:
                raise ConfigError(f"Bad syntax on line {line_number}: {line}")
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config
