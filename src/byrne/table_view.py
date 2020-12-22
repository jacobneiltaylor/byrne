from typing import Dict
from dataclasses import dataclass

from .datastructures import KeyDefinition
from .table import Table
from .marshallers import Marshaller, AutoMarshaller
from .recordmaps import RecordMap
from .paginators import QueryPaginator, ScanPaginator, Paginator  # noqa
from .constants import DEFAULT_SELECT  # noqa


class TableView:
    """
        A high-level interface for DynamoDB Tables
        Supports the following features:
            - Automatic expression synthesis for known keys
            - Attribute marshalling/unmarshalling
            - Datatype and class mapping
            - Result pagination
    """

    @dataclass
    class SecondaryIndex:
        name: str
        definition: KeyDefinition
        view: "TableView"

        def query(self):
            pass

    def __init__(
        self,
        table: Table,
        marshaller: Marshaller = None,
        recordmap: RecordMap = None
    ):
        self.table = table
        self.marshaller = marshaller
        self.recordmap = recordmap
        self.secondary_indexes = []

    def _make_index(self, name, definition):
        return self.SecondaryIndex(name, definition, self)

    def _build_secondary_indexes(self):
        def _import_from_dict(dct: Dict[str, KeyDefinition]):
            for k, v in dct.items():
                self.secondary_indexes.append(self._make_index(k, v))
        _import_from_dict(self.table.definition.lsi)
        _import_from_dict(self.table.definition.gsi)

    def _postprocess_read_record(self, record: dict):
        if self.marshaller is not None:
            record = {
                k: self.marshaller.unpack_attribute(v)
                for k, v
                in record.items()
            }
        if self.recordmap is not None:
            return self.recordmap.map_record(record)
        return record

    def _preprocess_write_record(self, data):
        if self.recordmap is not None:
            data = self.recordmap.unmap_object(data)
        if self.marshaller is not None:
            return {
                k: self.marshaller.pack_attribute(v) for k, v in data.items()
            }
        return data

    @classmethod
    def get_default_table_view(cls, table: Table):
        return cls(table, AutoMarshaller())

    def query(self, key_condition_exp, **kwargs) -> Paginator:
        kwargs["key_condition_exp"] = key_condition_exp

    def _get_primary_key_selector(self, value, sort=False):
        primary_key = self.table.definition.primary_key
        key_name = primary_key.partition_key

        if sort:
            assert primary_key.is_sortable
            key_name = primary_key.sort_key

        key_type = self.table.definition.attributes[key_name]

        return {key_name: {key_type: value}}

    def _build_key_args(self, partition_key, sort_key):
        key_args = self._get_primary_key_selector(partition_key)
        if sort_key is not None:
            key_args.update(self._get_primary_key_selector(sort_key, True))
        return key_args
