import pytest
import decimal
import deepdiff

import constants
import helpers

from byrne.marshallers import AutoMarshaller


def _pack_attribute(autoset, attr):
    return AutoMarshaller(autoset).pack_attribute(attr)


def _assert_dict_eq(dct_a, dct_b):
    diff = deepdiff.DeepDiff(dct_a, dct_b, ignore_order=True)
    assert len(diff) == 0


PACK_ATTRIBUTE_TESTS = {
    "autoset": [constants.TEST_MARSHAL_PACKED, True],
    "no_autoset": [constants.TEST_MARSHAL_PACKED_NO_AUTOSET, False],
}

@pytest.mark.parameterise("expect,autoset", helpers.make_params(PACK_ATTRIBUTE_TESTS))
def test_pack_attribute(expect, autoset):
    _assert_dict_eq(_pack_attribute(autoset, constants.TEST_MARSHAL_UNPACKED), expect)
    _assert_dict_eq(_pack_attribute(autoset, constants.TEST_MARSHAL_UNPACKED_DECIMAL), expect)
