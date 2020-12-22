from support import helpers, data


def test_table_put_get_basic(aws, ddb_table):
    table = helpers.get_byrne_table(aws, ddb_table)
    table.put_item(data.TABLE_RECORD_BASIC)
    result = table.get_item(data.TABLE_KEY_BASIC)
    helpers.assert_dict_eq(data.TABLE_RECORD_BASIC, result["Item"])
