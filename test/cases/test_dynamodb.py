from support import helpers

from byrne import DynamoDb
from byrne.datastructures import TableDefinition, KeyDefinition


def _get_default_tabledef(name):
    table_def = TableDefinition()
    table_def.name = name
    table_def.attributes["id"] = "S"
    table_def.primary_key = KeyDefinition("id")
    return table_def


def _get_complex_tabledef(name):
    table_def = TableDefinition()
    table_def.name = name
    table_def.attributes["post_name"] = "S"
    table_def.attributes["revision_id"] = "N"
    table_def.attributes["tag"] = "S"
    table_def.attributes["author"] = "S"
    table_def.primary_key = KeyDefinition("post_name", "revision_id")
    table_def.lsi["tag_index"] = KeyDefinition("post_name", "tag")
    table_def.gsi["author_index"] = KeyDefinition("author")
    return table_def


def test_name_normalisation(table_id):
    """
        Ensure _normalise_table_name is working as expected
    """
    table = helpers.get_ephemeral_table_name(table_id, "DummyName")
    table_def = _get_default_tabledef(table)
    result = DynamoDb._normalise_table_name(table_def)  # noqa
    assert result == table
    assert result == DynamoDb._normalise_table_name(table)  # noqa
    assert "DummyName" in result


def test_basic_creation_arg_generation(table_id):
    """
        Test generation of args for create_table for a basic table
    """
    table = helpers.get_ephemeral_table_name(table_id, "DummyName")
    table_def = _get_default_tabledef(table)
    expected = helpers.get_table_data("default")
    expected["TableName"] = table
    generated = DynamoDb.get_creation_args_for_definition(table_def)
    helpers.assert_dict_eq(expected, generated)


def test_complex_creation_arg_generation(table_id):
    """
        Test generation of args for create_table for a complex table
    """
    table = helpers.get_ephemeral_table_name(table_id, "DummyName")
    table_def = _get_complex_tabledef(table)
    expected = helpers.get_table_data("complex")
    expected["TableName"] = table
    generated = DynamoDb.get_creation_args_for_definition(table_def)
    helpers.assert_dict_eq(expected, generated)


def test_basic_table_create_delete(table_id, aws):
    """
        Test creation and deletion of a basic table
    """
    client = helpers.get_byrne_client(aws)
    table = helpers.get_ephemeral_table_name(table_id, "CreateDeleteBasic")
    table_def = _get_default_tabledef(table)
    client.create_table(table_def)
    client.wait_for_active(table)
    client.delete_table(table)
    client.wait_for_deletion(table)


def test_complex_table_create_delete(table_id, aws):
    """
        Test creation and deletion of a complex table
    """
    client = helpers.get_byrne_client(aws)
    table = helpers.get_ephemeral_table_name(table_id, "CreateDeleteComplex")
    table_def = _get_complex_tabledef(table)
    client.create_table(table_def)
    client.wait_for_active(table)
    client.delete_table(table)
    client.wait_for_deletion(table)
