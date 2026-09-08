PYTHON     = python3
SRC        = a_maze_ing.py
CONFIG     = config.txt
OUTPUT     = maze.txt

BLUE = \033[34m
GREEN = \033[32m
YELLOW = \033[33m
RESET = \033[0m

.PHONY: run clean fclean re mypy build install

lint:
	@echo "$(BLUE)checking flake8$(RESET)"
	$(PYTHON) -m flake8 .
	@echo "$(BLUE)checking mypy$(RESET)"
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "$(GREEN)flake8 and mypy check successfully.$(RESET)"

lint-strict:
	@echo "$(BLUE)checking flake8$(RESET)"
	$(PYTHON) -m flake8 .
	@echo "$(BLUE)checking mypy --strict$(RESET)"
	$(PYTHON) -m mypy --strict .
	@echo "$(GREEN)flake8 and mypy strict check successfully.$(RESET)"

build:
	pip install build
	$(PYTHON) -m build

install:
	
	pip install dist/mazegen-1.0.0-py3-none-any.whl

debug:
	$(PYTHON) -m pdb $(SRC) $(CONFIG)

run:
	$(PYTHON) $(SRC) $(CONFIG)

clean:
	@echo "$(YELLOW) Cleaning up$(RESET)"
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf dist/
	rm -rf mazegen.egg-info/
	@echo "$(GREEN) Cleaning up complete.$(RESET)"


fclean: clean
	rm -f $(OUTPUT)

re: fclean run
