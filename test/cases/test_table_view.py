from support import helpers, data


@helpers.use_table("sortable")
def test_table_view_query(aws, ddb_table):
    view = helpers.get_byrne_table_view(aws, ddb_table)
    helpers.preload_table(view.table, data.ITEM_SET_SORTABLE)

    view.table.read_limit = 2  # set low read limit to test pagination

    names = [item["name"] for item in view.query(data.EXP_OBJ_SORTABLE_GTE)]

    assert "Teo Mcnamara" in names
    assert "Indigo Duffy" in names
    assert "Phoebe Quinn" not in names


@helpers.use_table("sortable")
def test_table_view_scan(aws, ddb_table):
    view = helpers.get_byrne_table_view(aws, ddb_table)
    helpers.preload_table(view.table, data.ITEM_SET_SORTABLE)

    results = list(view.scan())

    assert len(results) == 100
