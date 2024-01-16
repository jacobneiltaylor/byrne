code:
    code {{ justfile_directory() }}

install:
    poetry install

format: install
    poetry run ruff format {{ justfile_directory() }}/src {{ justfile_directory() }}/test
    poetry run ruff check --fix {{ justfile_directory() }}/src {{ justfile_directory() }}/test

lint: install
    poetry run ruff check {{ justfile_directory() }}/src {{ justfile_directory() }}/test

typecheck: install
    poetry run mypy {{ justfile_directory() }}/src

debug-lint:
    poetry run ruff check --show-source -e {{ justfile_directory() }}/src {{ justfile_directory() }}/test

unit: install
    poetry run tox -e unit -- -- --cov={{ justfile_directory() }}/src/byrne

remote-unit: install
    poetry run tox -e remote_unit -- -- --cov={{ justfile_directory() }}/src/byrne

publish: install
    poetry publish -r pypi --build

test: lint typecheck unit
