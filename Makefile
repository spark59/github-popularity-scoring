.PHONY: clean-venv new-venv install install-dev refresh test run

# Delete .venv
clean-venv:
	rm -rf .venv

# Create new venv
new-venv:
	python3 -m venv .venv

# Install only runtime dependencies
install:
	. .venv/bin/activate && pip install -r requirements.txt

# Install dev dependencies too
install-dev:
	. .venv/bin/activate && pip install -r requirements.txt -r dev-requirements.txt

# Full refresh: clean, create, and install
refresh: clean-venv new-venv install-dev

# Run test suite
test:
	. .venv/bin/activate && pytest

# Run dev server
run:
	. .venv/bin/activate && uvicorn app.main:app --reload