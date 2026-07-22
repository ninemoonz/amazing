import sys
from parser import parse_config, ConfigError
from validate_and_build import validate_and_build


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: parser.py <file>")
    else:
        config_data: dict[str, str]
        try:
            file_name: str = (sys.argv[1])
        except ConfigError as e:
            print(e)
            sys.exit(1)
        print("=== Config File Reader ===")
        config_data = parse_config(file_name)
        print(config_data)
        print("[FUNCTION OUTCOME]")
        validate_and_build(config_data)
