
clean:
	rm -rf venv
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache

venv: clean
	python3 -m venv venv

install:
	venv/bin/pip install -r requirements.txt