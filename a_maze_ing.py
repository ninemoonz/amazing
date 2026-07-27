import sys
from parser import parse_config
from validate_and_build import key_check, parse_dimension, perfect_check

if __name__ == "__main__":
    raw = parse_config("config.txt")
    print(raw)
    missing = key_check(raw)
    print(missing)
    width = parse_dimension(raw, "WIDTH")
    height = parse_dimension(raw, "HEIGHT")
    print(width, height, type(width), type(height))
    perfect = perfect_check(raw, "PERFECT")
    print(perfect, type(perfect))
