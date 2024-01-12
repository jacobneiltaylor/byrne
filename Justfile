code:
    code {{ justfile_directory() }}

install:
    poetry install

format: install
    poetry run ruff format {{ justfile_directory() }}/src {{ justfile_directory() }}/test
    poetry run ruff check --fix {{ justfile_directory() }}/src {{ justfile_directory() }}/test

lint: install
    poetry run ruff check {{ justfile_directory() }}/src {{ justfile_directory() }}/test

types: install
    poetry run mypy {{ justfile_directory() }}/src

debug-lint:
    poetry run ruff check --show-source -e {{ justfile_directory() }}/src {{ justfile_directory() }}/test

unit: install
    poetry run tox -e test_local -- -- --cov={{ justfile_directory() }}/src/byrne

test: lint types unit