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
    "b": 123,
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

MARSHAL_PACKED_NO_AUTOSET = helpers.load_attr("packed_no_autoset")

TABLE_RECORD_BASIC = helpers.load_record("basic")

TABLE_KEY_BASIC = helpers.load_key("basic")
