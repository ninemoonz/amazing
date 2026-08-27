PYTHON     = python3
SRC        = a_maze_ing.py
CONFIG     = config.txt
OUTPUT     = maze.txt

.PHONY: run clean fclean re mypy

install:
	pip install mazegen-1.0.0-py3-none-any.whl

run:
	$(PYTHON) $(SRC) $(CONFIG)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache

fclean: clean
	rm -f $(OUTPUT)

re: fclean run

mypy:
	mypy $(SRC)
