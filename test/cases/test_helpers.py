from support import helpers

import byrne.helpers


def test_set_optional_arg():
    test_dict = {}

    byrne.helpers.set_optional_arg("should_exist", "some_value", test_dict)
    byrne.helpers.set_optional_arg("shouldnt_exist", None, test_dict)

    assert "should_exist" in test_dict
    assert "shouldnt_exist" not in test_dict
    assert test_dict["should_exist"] == "some_value"


def test_set_arg_if_not_empty():
    test_dict = {}

    byrne.helpers.set_arg_if_not_empty("should_exist", ["some_value"], test_dict)  # noqa: E501
    byrne.helpers.set_arg_if_not_empty("shouldnt_exist", [], test_dict)

    assert "should_exist" in test_dict
    assert "shouldnt_exist" not in test_dict
    assert isinstance(test_dict["should_exist"], list)
    assert len(test_dict["should_exist"]) == 1
    assert test_dict["should_exist"][0] == "some_value"


def test_first_kvp():
    assert byrne.helpers.first_kvp({"a": 1}) == ("a", 1)


def test_invert_dict():
    expect = {"a": 1, "b": 2}
    actual = byrne.helpers.invert_dict({1: "a", 2: "b"})
    helpers.assert_dict_eq(expect, actual)


def test_autoclassifier():
    assert byrne.helpers.autoclassifier(bool)(False)
    assert byrne.helpers.autoclassifier(str)("foo")
    assert not byrne.helpers.autoclassifier(list)(123)

