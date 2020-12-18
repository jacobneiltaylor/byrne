import os
import json
import pytest

DATA_DIR = "data"


def get_test_rootdir():
    return os.path.basename(__file__)


def open_test_data_file(subdir, filename):
    return open(os.path.join(get_test_rootdir(), DATA_DIR, subdir, filename))


def load_record(name):
    with open_test_data_file("records", f"{name}.json") as datafile:
        return json.load(datafile)


def make_params(data: dict):
    return [pytest.param(*value, id=key) for key, value in data.items()]
