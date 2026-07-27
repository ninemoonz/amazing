import sys
from parser import parse_config
from validate_and_build import key_check

if __name__ == "__main__":
    raw = parse_config("config.txt")
    print(raw)
    missing = key_check(raw)
    print(missing)
