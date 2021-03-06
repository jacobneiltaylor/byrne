# Byrne
> A intelligent DynamoDB frontend for Python3


## Basic Usage

### Importing the package

```python
    import boto3  # require to build a client
    import byrne
```

### Creating a client

```python
    session = boto3.Session()
    base_client = session.client("dynamodb")
    client = byrne.DynamoDB(base_client)
    client.list_tables()  # ["table", "names"]
```

### Creating a Table

```python
    table_def = byrne.datastructures.TableDefinition(
        "TableName",
        {
            "id": "S"
        },
        byrne.datastructures.KeyDefinition("id")
    )

    client.create_table(table_def)
```

## FAQ

 1. How do I install `byrne`?
    - Simply run `pip3 install byrne` - the PyPI package is automatically kept up to date with this repository.

 2. Why does this require Python 3.7?
    - We use dataclasses heavily to model table metadata and to simplify query expressions.

 3. Why is this better than using the default client in `boto3`?
    - Support for asyncronous result pagination.
    - Allows for integrated object mapping.
    - Configurable value marshalling and unmarshalling.
    - A more Pythonic interface.
    - Builtin support for working with DAX.

 4. How is the package tested?
    - The testing regimen is automated through `tox`.
    - Tests are run against a DynamoDB Local instance for all supported Python versions.
    - The tests are run against the live DynamoDB service in AWS us-east-1 for the latest Python version.
    - Code coverage is tracked through [Coveralls](https://coveralls.io/github/jacobneiltaylor/byrne).

 5. Why is the DAX code path untested?
    - We are working on creating a testing strategy for DAX workflows.
    - DAX is expensive, we can't justify having a dedicated cluster running only for testing.

 6. I can't run the test cases on my local machine! Help!
    - There are 5 test environments defined in `tox.ini`:
        1. `test`: Runs test suite against "real" DynamoDB.
        2. `test_local`: Runs test suite against DynamoDB Local.
        3. `test_coverage`: Same as `test`, with coverage reporting.
        4. `test_coverage_local`: Same as `test_local`, with coverage reporting.
        5. `flake8`: Runs PEP8 conformance testing.
    - The live test cases require AWS credentials on your machine.
    - These credentials need access rights to assume a role used for testing.
    - Access to this role is only granted to trusted contributors.
    - You should be able to run the local environments after executing the `run_dynamodb_local.sh` script.
    - `flake8` should run without any fuss.
