import sys
import typing


def parse_config(file_name: str) -> dict[str, int]:
    try:
        config: dict[str, int] = {}
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
        print(f"Error opening file '{sys.argv[1]}' : {e}")
    finally:
        if f:
            f.close()
            print(f"File '{file_name}' closed")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: parser.py <file>")
    else:
        config_data: dict[str, int]
        file_name: str = (sys.argv[1])
        print("=== Config File Reader ===")
        config_data = parse_config(file_name)
        print(config_data)
