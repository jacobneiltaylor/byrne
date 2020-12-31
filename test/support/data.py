from decimal import Decimal

from . import helpers

MARSHAL_UNPACKED_DECIMAL = {
    "a": "123",
    "b": Decimal("123"),
    "c": b"123",
    "d": ["1", "2", "3"],
    "e": [Decimal("1"), Decimal("2"), Decimal("3")],
    "f": [b"1", b"2", b"3"],
    "g": {"g1": "1", "g2": b"2", "g3": Decimal("3.14")},
    "h": [b"1", 2, "3"],
    "i": None,
    "j": True,
    "k": False
}

MARSHAL_UNPACKED = {
    "a": "123",
    "b": float(123),
    "c": b"123",
    "d": ["1", "2", "3"],
    "e": [float(1), float(2), float(3)],
    "f": [b"1", b"2", b"3"],
    "g": {"g1": "1", "g2": b"2", "g3": 3.14},
    "h": [b"1", 2, "3"],
    "i": None,
    "j": True,
    "k": False
}

MARSHAL_PACKED = helpers.load_attr("packed")

MARSHAL_PACKED_LIST = helpers.load_attr("packed_lists")

TABLE_ITEM_BASIC = helpers.load_item("basic")
TABLE_ITEM_BASIC_UPDATED = helpers.load_item("basic_updated")

TABLE_KEY_BASIC = helpers.load_key("basic")

UPDATE_EXP_BASIC = helpers.load_raw_expression("basic_update")
QUERY_EXP_BASIC = helpers.load_raw_expression("basic_query")
SCAN_FILTER_EXP_BASIC = helpers.load_raw_expression("basic_scan")

EXP_OBJ_SORTABLE_GTE = helpers.load_expression("sortable_gte")
EXP_OBJ_UPDATE = helpers.load_expression("update")

ITEM_SET_BASIC = helpers.load_item_set("basic")
ITEM_SET_SORTABLE = helpers.load_item_set("sortable")
