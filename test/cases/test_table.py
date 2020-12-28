from support import helpers, data


def test_table_put_item_basic(aws, ddb_table):
    table = helpers.get_byrne_table(aws, ddb_table)
    table.put_item(data.TABLE_ITEM_BASIC)
    result = table.get_item(data.TABLE_KEY_BASIC)
    helpers.assert_dict_eq(data.TABLE_ITEM_BASIC, result["Item"])


def test_table_update_item_basic(aws, ddb_table):
    table = helpers.get_byrne_table(aws, ddb_table)
    table.put_item(data.TABLE_ITEM_BASIC)
    expression, names, values = data.UPDATE_EXP_BASIC

    table.update_item(
        data.TABLE_KEY_BASIC,
        expression,
        attr_names=names,
        attr_values=values
    )

    result = table.get_item(data.TABLE_KEY_BASIC)
    helpers.assert_dict_eq(data.TABLE_ITEM_BASIC_UPDATED, result["Item"])


def test_table_delete_item_basic(aws, ddb_table):
    table = helpers.get_byrne_table(aws, ddb_table)
    table.put_item(data.TABLE_ITEM_BASIC)
    table.delete_item(data.TABLE_KEY_BASIC)
    result = table.get_item(data.TABLE_KEY_BASIC)
    assert "Item" not in result


def test_table_query_basic(aws, ddb_table):
    table = helpers.get_byrne_table(aws, ddb_table)
    helpers.preload_table(table, data.ITEM_SET_BASIC)
    expression, names, values = data.QUERY_EXP_BASIC

    result = table.query(
        expression,
        attr_names=names,
        attr_values=values
    )

    assert result["Count"] == 1
    assert result["Items"][0]["name"]["S"] == "Bail Organa"


def test_table_scan_basic(aws, ddb_table):
    table = helpers.get_byrne_table(aws, ddb_table)
    helpers.preload_table(table, data.ITEM_SET_BASIC)
    expression, names, values = data.SCAN_FILTER_EXP_BASIC

    result = table.scan(
        filter_exp=expression,
        attr_names=names,
        attr_values=values
    )

    assert result["Count"] == 1
    assert result["Items"][0]["id"]["S"] == "6"
