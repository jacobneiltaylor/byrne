from decimal import Decimal

import pytest

from support import helpers, data

from byrne.marshallers import AutoMarshaller


def _pack_attribute(autoset, attr):
    return AutoMarshaller(autoset).pack_attribute(attr)


def _unpack_attribute(number_cast, attr):
    return AutoMarshaller(number_cast=number_cast).unpack_attribute(attr)


PACK_ATTR_TESTS = helpers.make_params({
    "autoset": [data.MARSHAL_PACKED, True],
    "no_autoset": [data.MARSHAL_PACKED_LIST, False],
})

UNPACK_ATTR_TESTS = helpers.make_params({
    "float_cast": [data.MARSHAL_UNPACKED, float],
    "decimal_cast": [data.MARSHAL_UNPACKED_DECIMAL, Decimal],
})


@pytest.mark.parametrize("expect,autoset", PACK_ATTR_TESTS)
def test_pack_attribute(expect, autoset):
    """
        Test the ability of the AutoMarshaller class to "pack" native
        Python datastructures into DynamoDB datastructures
    """
    default_packed = _pack_attribute(autoset, data.MARSHAL_UNPACKED)
    decimal_packed = _pack_attribute(autoset, data.MARSHAL_UNPACKED_DECIMAL)
    helpers.assert_dict_eq(expect, default_packed)
    helpers.assert_dict_eq(expect, decimal_packed)


@pytest.mark.parametrize("expect,number_cast", UNPACK_ATTR_TESTS)
def test_unpack_attribute(expect, number_cast):
    """
        Test the ability of the AutoMarshaller class to "unpack"
        DynamoDB datastructures into native Python datastructures
    """
    set_unpacked = _unpack_attribute(number_cast, data.MARSHAL_PACKED)
    list_unpacked = _unpack_attribute(number_cast, data.MARSHAL_PACKED_LIST)
    helpers.assert_dict_eq(expect, set_unpacked)
    helpers.assert_dict_eq(expect, list_unpacked)
