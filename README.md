_This project has been created as part of the 42 curriculum by kkweon, myapaten_

## Description

**A-Maze-Ing** is a procedural maze generation and solving system that combines depth-first search maze generation with breadth-first search pathfinding. The application generates perfect and imperfect mazes on configurable grids, computes the shortest path from entry to exit, and provides an interactive terminal-based visualization with color-coded walls, entry/exit markers, and solution highlighting.

### Project Goal
To create a robust, configurable maze generator and solver demonstrating fundamental algorithms in graph theory (DFS for maze generation, BFS for shortest-path solving), with a focus on clean architecture, comprehensive documentation, and interactive user experience.

### Overview
- **Maze Generation**: Uses depth-first search with optional loop braiding to create perfect or imperfect mazes
- **Pathfinding**: Implements breadth-first search to find and display the shortest route from entry to exit
- **Visualization**: Renders mazes as ASCII art with ANSI terminal colors, entry/exit indicators, and solution path overlay
- **Configuration**: Fully parameterized via config file with support for custom dimensions, entry/exit points, and random seeds
- **Interactive Menu**: Terminal UI for maze regeneration, path toggling, color rotation, and clean exit

## Instructions

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd amazing2
   ```

2. **Check Python version:**
   - Requires Python 3.10+ (uses PEP 604 union syntax `int | None`)
   - Verify: `python3 --version`
   - If needed, install Python 3.13: `brew install python3.13`

3. **Create virtual environment (optional but recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

### Configuration

Create or modify `config.txt` with the following format:

```
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=14,14
OUTPUT_FILE=maze.txt
PERFECT=FALSE
SEED=42
```

**Config Parameters:**
- `WIDTH`: Maze grid width in cells (positive integer)
- `HEIGHT`: Maze grid height in cells (positive integer)
- `ENTRY`: Entry point as `x,y` (must be within grid bounds)
- `EXIT`: Exit point as `x,y` (must be different from ENTRY)
- `OUTPUT_FILE`: Path where generated maze will be written
- `PERFECT`: `TRUE` for perfect maze (single path between any two points), `FALSE` for maze with loops
- `SEED`: Optional integer for reproducible generation (omit or leave blank for random)

### Execution

```bash
python3 a_maze_ing.py config.txt
```

This will:
1. Parse and validate the configuration file
2. Generate a maze according to parameters
3. Compute the shortest path using BFS
4. Write maze data and solution to the output file
5. Display an interactive menu where you can:
   - `[1]` Regenerate a new maze with same config
   - `[2]` Show/Hide the solution path
   - `[3]` Rotate wall colors (pink, green, yellow, cyan, white)
   - `[4]` Quit the program

### Output Format

The generated `maze.txt` file contains:
- Maze grid: Hexadecimal-encoded cells (one character per cell)
- Blank line
- Entry coordinates: `x,y`
- Exit coordinates: `x,y`
- Solution route: Sequence of directions (N/E/S/W) representing the shortest path

**Example output:**
```
7735753577...
3c3c3c3c3c...
(blank line)
0,0
14,14
EESSWWEESSNNNWWWEE
```

### Validation

Optional: Verify maze encoding consistency:
```bash
python3 src/output_validator.py maze.txt
```

This validates that neighboring cells share consistent wall information.

## Resources

### Core Algorithm References
- **Maze Generation: Depth-First Search (DFS)**
  - Maze generation by recursive backtracking: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Depth-first_search
  - Creates perfect mazes (spanning trees of grid graph)
  
- **Pathfinding: Breadth-First Search (BFS)**
  - Shortest path in unweighted graphs: https://en.wikipedia.org/wiki/Breadth-first_search
  - Guarantees optimal (shortest) solution for unweighted mazes
  
- **Loop Addition: Braiding Algorithm**
  - Removes dead ends to create multiple valid paths
  - Reference: "Maze generation by recursive backtracking" literature

### Technical Documentation
- Python Type Hints (PEP 484): https://www.python.org/dev/peps/pep-0484/
- Python Docstring Convention (PEP 257): https://mimo.org/glossary/python/docstrings
- Python Collections module: https://docs.python.org/3/library/collections.html

### Code Quality
- flake8 linting: https://flake8.pycqa.org/
- Type hints throughout for code clarity and IDE support

### AI Assistance Used

**GitHub Copilot** (Claude Haiku 4.5) was used for:
- **Algorithm Implementation**: Initial BFS pathfinding algorithm with queue-based approach and parent tracking
- **Docstring Generation**: PEP 257-compliant docstrings for all modules, classes, and functions
- **Error Handling**: ConfigError, OffsetError, and PathFindingError exception design
- **Code Review & Debugging**: 
  - Python version compatibility fixes (3.9→3.13 for `int | None` syntax)
  - Hard-coded filename resolution (dynamic config-based paths)
  - Terminal color code implementation and ANSI escape sequences
- **Documentation**: README structure, installation instructions, usage examples
- **Refactoring**: Code organization, import restructuring, module separation

**Specific contributions:**
- `maze_generator.py`: BFS algorithm in `find_path()` method
- `src/parser.py`: Configuration file parsing with error handling
- `src/validate_and_build.py`: Configuration validation functions
- `src/menu.py`: Interactive menu loop with color rotation and path toggling
- All module docstrings and inline documentation

## Usage Example

### Basic Workflow

```bash
# 1. Run with default config
python3 a_maze_ing.py config.txt

# 2. See initial maze with entry (red) and exit (blue) markers
# 3. Press 2 to show the solution path (light shade marks route)
# 4. Press 3 to cycle through wall colors
# 5. Press 1 to generate a new maze with same dimensions
# 6. Press 4 to exit cleanly
```

### Custom Maze Generation

Create `large_maze.txt`:
```
WIDTH=50
HEIGHT=50
ENTRY=0,0
EXIT=49,49
OUTPUT_FILE=large_maze.txt
PERFECT=TRUE
SEED=12345
```

Then run:
```bash
python3 a_maze_ing.py large_maze.txt
```

## Feature List

✅ **Core Features**
- Procedural maze generation using DFS algorithm
- Perfect and imperfect (looped) maze variants
- Optimal shortest-path solving with BFS
- Hexadecimal maze encoding with bitmask wall representation
- Configurable grid dimensions and entry/exit points
- Reproducible generation with optional random seed
- ASCII art rendering with ANSI terminal colors

✅ **User Interface**
- Interactive terminal menu
- Real-time maze regeneration
- Solution path visualization with shade overlay
- Dynamic wall color rotation (5 color schemes)
- Entry/exit point highlighting
- Clean screen rendering and program exit

✅ **Code Quality**
- 100% PEP 257 docstring coverage
- Comprehensive type hints (Python 3.10+)
- Custom exception hierarchy
- Modular architecture with separation of concerns
- Virtual environment support
- Input validation and error handling

## Technical Choices

### Maze Generation Algorithm: Depth-First Search (Recursive Backtracking)

**Why DFS?**
1. **Simplicity & Correctness**: Guarantees a spanning tree (perfect maze) with one path between any two cells
2. **Common Standard**: Industry-standard for procedural maze generation in games and puzzles
3. **Efficient Memory**: Uses stack-based recursion naturally suited to the algorithm
4. **Extensible**: Easy to enhance with braiding (loop addition) for imperfect mazes
5. **Performance**: O(width × height) time complexity with minimal overhead

**Alternative Considered:** Prim's algorithm (would require priority queue, more complex for grid representation)

### Pathfinding: Breadth-First Search

**Why BFS?**
1. **Optimality**: Guarantees shortest path in unweighted graphs (mazes)
2. **Simplicity**: Easier to implement and understand than Dijkstra for unweighted cases
3. **Performance**: Linear time complexity O(width × height) on grid
4. **Clarity**: Explicit queue-based approach makes solution trackable

### Hexadecimal Cell Encoding

**Bitmask Representation:**
- Each cell stores a 4-bit value (0-15) where each bit represents a wall
- Bit 0 (value 1): NORTH wall
- Bit 1 (value 2): EAST wall
- Bit 2 (value 4): SOUTH wall
- Bit 3 (value 8): WEST wall

**Advantages:**
- Compact storage (one hex character per cell)
- Efficient bitwise operations for wall checking
- Easy validation (neighbors must have matching wall bits)

### Architecture: Separation of Concerns

- `maze_generator.py`: Algorithm implementation (DFS maze carving, BFS pathfinding)
- `src/parser.py`: File I/O and parsing
- `src/validate_and_build.py`: Configuration validation and dataclass construction
- `src/maze_display.py`: Rendering and visualization
- `src/menu.py`: User interaction and workflow orchestration
- `src/output_generator.py`: Maze serialization

**Benefit:** Each module is independently testable and reusable

### Reusable Components

**`MazeGen` class:**
- Standalone maze generation without dependencies beyond Python stdlib
- Can be imported and used in other projects: `from maze_generator import MazeGen`
- Methods usable individually: `gen_grid()`, `carve_maze()`, `find_path()`
- Configurable via constructor parameters (width, height, entry, exit, seed)

**`MazeCell` class:**
- Generic grid cell representation with wall encoding
- Reusable for other grid-based algorithms (pathfinding, game grids, etc.)

**`render_maze()` function:**
- Generic ASCII art renderer for any hex-encoded maze
- Color customization via `WALL_COLORS` list

**`parse_config()` and `build_config()`:**
- Generic configuration parsing framework
- Easily extended for other KEY=VALUE config formats

**`BFS pathfinding:**
- Standard graph algorithm applicable to any grid-based pathfinding
- Queue-based implementation usable in game AI, robotics, etc.

## Team and Project Management

**Original Project By:**
- kkweon
- myapaten

**Current Development:**
- Implemented as part of 42 curriculum (Common Core maze project)
- Feature completeness: 100% (generation, solving, visualization, menu)
- Documentation: 100% (all modules, functions, classes have PEP 257 docstrings)

**Key Milestones:**
1. ✅ Core maze generation algorithm (DFS)
2. ✅ Pathfinding algorithm (BFS)
3. ✅ Configuration parsing and validation
4. ✅ File I/O and output formatting
5. ✅ ASCII art rendering with ANSI colors
6. ✅ Interactive user interface
7. ✅ Comprehensive documentation (docstrings + README)
8. ✅ Python version compatibility (3.10+)

**Known Limitations:**
- Small mazes (< 7×5) may fail due to "42 logo" pattern sizing
- Menu is terminal-specific (uses `os.system('clear'/'cls')`)
- No network/multiplayer features
- No persistence beyond single session output files
