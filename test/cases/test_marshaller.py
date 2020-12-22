import pytest

from support import helpers, data

from byrne.marshallers import AutoMarshaller


def _pack_attribute(autoset, attr):
    return AutoMarshaller(autoset).pack_attribute(attr)


PACK_ATTR_TESTS = helpers.make_params({
    "autoset": [data.MARSHAL_PACKED, True],
    "no_autoset": [data.MARSHAL_PACKED_NO_AUTOSET, False],
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
