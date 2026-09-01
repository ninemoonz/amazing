"""Maze output file validator.

Validates that neighboring cells in the maze encoding share consistent
wall information. This script performs basic structural checks without
error handling for malformed files.

Usage:
    python3 output_validator.py <output_file>
"""

import sys

if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <output_file>")
    sys.exit(1)

g = []
for line in open(sys.argv[1]):
    if line.strip() == '':
        break
    g.append([int(c, 16) for c in line.strip(' \t\n\r')])

for r in range(len(g)):
    for c in range(len(g[0])):
        v = g[r][c]
        if not all([(r < 1 or v & 1 == (g[r-1][c] >> 2) & 1),
                    (c >= len(g[0])-1 or (v >> 1) & 1 == (g[r][c+1] >> 3) & 1),
                    (r >= len(g)-1 or (v >> 2) & 1 == g[r+1][c] & 1),
                    (c < 1 or (v >> 3) & 1 == (g[r][c-1] >> 1) & 1)]):
            print(f'Wrong encoding for ({c},{r})')
