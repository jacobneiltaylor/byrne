import hashlib
import json
import os
import time
import uuid

import deepdiff
import pytest

from byrne import DynamoDb, Table, TableView
from byrne.datastructures import Expression
from support import constants


def get_test_rootdir():
    return os.path.dirname(__file__)


def open_test_data_file(subdir, filename):
    return open(os.path.join(get_test_rootdir(), constants.FILE_DIR, subdir, filename))


def load_test_json_file(subdir, name):
    filename = f"{name}.json"
    with open_test_data_file(subdir, filename) as datafile:
        return json.load(datafile)


def load_attr(name):
    return load_test_json_file(constants.ATTRS_DIR, name)


def load_item(name):
    return load_test_json_file(constants.ITEMS_DIR, name)


def load_item_set(name):
    return load_test_json_file(constants.ITEM_SETS_DIR, name)


def load_key(name):
    return load_test_json_file(constants.KEYS_DIR, name)


def load_expression(name):
    return Expression(**load_test_json_file(constants.EXP_DIR, name))


def load_raw_expression(name):
    data = load_test_json_file(constants.RAW_EXP_DIR, name)
    return (data["expression"], data["names"], data["values"])


def make_params(data: dict):
    return [pytest.param(*value, id=key) for key, value in data.items()]


def get_ephemeral_table_name(session_name, test_name):
    return "_".join([constants.EPHEMERAL_TABLE_PREFIX, session_name, test_name])


def get_short_hash(data: str):
    digest = hashlib.sha512(data.encode(constants.ENCODING)).hexdigest()
    return digest[:10]


def get_timestamp():
    return int(time.time())


def get_uuid():
    return uuid.uuid4()


def get_table_data(name):
    return load_test_json_file(constants.TABLES_DIR, name)


def get_function_table_data(function):
    if hasattr(function, "table"):
        return get_table_data(function.table)
    return get_table_data("default")


def assert_dict_eq(dct_a, dct_b):
    diff = deepdiff.DeepDiff(dct_a, dct_b, ignore_order=True)
    assert len(diff) == 0


def get_byrne_client(ddb_client):
    return DynamoDb(ddb_client)


def get_byrne_table(ddb_client, name) -> Table:
    return Table.get_table(get_byrne_client(ddb_client), name)


def get_byrne_table_view(ddb_client, name) -> TableView:
    return TableView.get_default_table_view(get_byrne_table(ddb_client, name))


def preload_table(table: Table, items):
    for item in items:
        table.put_item(item)


def use_table(table):
    def decorator(func):
        func.table = table
        return func

    return decorator
