import os
import json
import uuid
import time
import hashlib

import pytest
import deepdiff

from byrne import DynamoDb, Table

from . import constants


def get_test_rootdir():
    return os.path.dirname(__file__)


def open_test_data_file(subdir, filename):
    return open(os.path.join(
        get_test_rootdir(),
        constants.FILE_DIR,
        subdir,
        filename
    ))


def load_test_json_file(subdir, name):
    filename = f"{name}.json"
    with open_test_data_file(subdir, filename) as datafile:
        return json.load(datafile)


def load_attr(name):
    return load_test_json_file(constants.ATTRS_DIR, name)


def load_record(name):
    return load_test_json_file(constants.RECORDS_DIR, name)


def load_record_set(name):
    return load_test_json_file(constants.RECORD_SETS_DIR, name)


def load_key(name):
    return load_test_json_file(constants.KEYS_DIR, name)


def load_expression(name):
    data = load_test_json_file(constants.EXP_DIR, name)
    return (data["expression"], data["names"], data["values"])


def make_params(data: dict):
    return [pytest.param(*value, id=key) for key, value in data.items()]


def get_ephemeral_table_name(session_name, test_name):
    return "_".join([
        constants.EPHEMERAL_TABLE_PREFIX,
        session_name,
        test_name
    ])


def get_short_hash(data: str):
    digest = hashlib.sha512(data.encode(constants.ENCODING)).hexdigest()
    return digest[:10]


def get_timestamp():
    return int(time.time())


def get_uuid():
    return uuid.uuid4()


def get_table_data(name):
    return load_test_json_file(constants.TABLES_DIR, name)


def get_function_table_data(function_name):
    try:
        return get_table_data(function_name)
    except FileNotFoundError:
        return get_table_data("default")


def assert_dict_eq(dct_a, dct_b):
    diff = deepdiff.DeepDiff(dct_a, dct_b, ignore_order=True)
    assert len(diff) == 0


def get_byrne_client(aws):
    return DynamoDb(aws)


def get_byrne_table(aws, name) -> Table:
    return Table.get_table(get_byrne_client(aws), name)


def preload_table(table: Table, records):
    for record in records:
        table.put_item(record)
