from .helpers import set_optional_arg
from .dynamodb import DynamoDb
from .datastructures import TableDefinition
from .constants import DEFAULT_SELECT

class Table:
    """
        A low-level interface for interacting with DynamoDB Tables
    """
    def __init__(
        self,
        interface: DynamoDb,
        definition: TableDefinition,
        consistent_reads = True,
        read_limit = 50
    ):
        self.definition = definition
        self.dynamodb = interface
        self.consistent_reads = consistent_reads
        self.read_limit = read_limit

    @property
    def name(self):
        return self.definition.name

    def query(
        self,
        key_condition_exp: str,
        select: str = DEFAULT_SELECT,
        scan_forward: bool = True,
        start=None,
        index: str = None,
        filter_exp: str = None,
        projection_exp: str = None,
        attr_names: dict = None,
        attr_values: dict = None
    ):
        query_args = {
            "TableName": self.name,
            "KeyConditionExpression": key_condition_exp,
            "Select": select,
            "ScanIndexForward": scan_forward
        }

        set_optional_arg("ExclusiveStartKey", start, query_args)
        set_optional_arg("IndexName", index, query_args)
        set_optional_arg("FilterExpression", filter_exp, query_args)
        set_optional_arg("ExpressionAttributeNames", attr_names, query_args)
        set_optional_arg("ExpressionAttributeValues", attr_values, query_args)
        set_optional_arg("ProjectionExpression", projection_exp, query_args)

        return self.dynamodb.data_client.query(**query_args)

    def scan(
        self,
        select: str = DEFAULT_SELECT,
        scan_forward: bool = True,
        start=None,
        index: str = None,
        filter_exp: str = None,
        attr_names: dict = None,
        projection_exp: str = None,
        attr_values: dict = None
    ):
        scan_args = {
            "TableName": self.name,
            "Select": select,
            "ScanIndexForward": scan_forward
        }

        set_optional_arg("ExclusiveStartKey", start, scan_args)
        set_optional_arg("IndexName", index, scan_args)
        set_optional_arg("FilterExpression", filter_exp, scan_args)
        set_optional_arg("ExpressionAttributeNames", attr_names, scan_args)
        set_optional_arg("ExpressionAttributeValues", attr_values, scan_args)
        set_optional_arg("ProjectionExpression", projection_exp, scan_args)

        return self.dynamodb.data_client.scan(**scan_args)

    #def get_item(self, key, projection_exp: str = None, )

    #def put_item(self, record):
    #    put_args()
    #    self.dynamodb.data_client.put_item()

    @classmethod
    def get(cls, interface: DynamoDb, name: str):
        return cls(interface, interface.get_table_definition(name))