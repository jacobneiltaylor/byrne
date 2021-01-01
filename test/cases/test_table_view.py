from support import helpers, data


@helpers.use_table("sortable")
def test_table_view_query(ddb_client, ddb_table):
    view = helpers.get_byrne_table_view(ddb_client, ddb_table)
    helpers.preload_table(view.table, data.ITEM_SET_SORTABLE)

    view.table.read_limit = 2  # set low read limit to test pagination

    names = [item["name"] for item in view.query(data.EXP_OBJ_SORTABLE_GTE)]

    assert "Teo Mcnamara" in names
    assert "Indigo Duffy" in names
    assert "Phoebe Quinn" not in names


@helpers.use_table("sortable")
def test_table_view_scan(ddb_client, ddb_table):
    view = helpers.get_byrne_table_view(ddb_client, ddb_table)
    helpers.preload_table(view.table, data.ITEM_SET_SORTABLE)

    view.table.read_limit = 25
    view.preload = False

    results = list(view.scan())

    assert len(results) == 100


def test_table_view_get_item(ddb_client, ddb_table):
    view = helpers.get_byrne_table_view(ddb_client, ddb_table)

    view.put_item({
        "id": "1",
        "name": "Tom Jones",
        "age": 42
    })

    item = view.get_item("1")

    assert item["name"] == "Tom Jones"
    assert item["age"] == 42


def test_table_view_delete_item(ddb_client, ddb_table):
    view = helpers.get_byrne_table_view(ddb_client, ddb_table)

    view.put_item({
        "id": "1",
        "name": "Tom Jones",
        "age": 42
    })

    item = view.get_item("1")

    assert item["name"] == "Tom Jones"
    assert item["age"] == 42

    view.delete_item("1")

    assert view.get_item("1") is None


def test_table_view_update_item(ddb_client, ddb_table):
    view = helpers.get_byrne_table_view(ddb_client, ddb_table)

    view.put_item({
        "id": "1",
        "name": "Tom Jones",
        "age": 42
    })

    item = view.get_item("1")

    assert item["name"] == "Tom Jones"
    assert item["age"] == 42

    view.update_item(data.EXP_OBJ_UPDATE, "1")

    assert view.get_item("1")["age"] == 43
