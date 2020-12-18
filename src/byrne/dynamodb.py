from typing import List
from boto3 import Session
from amazondax import AmazonDaxClient
from boto3_type_annotations import dynamodb

from .datastructures import TableDefinition, KeyDefinition

class DynamoDb:
    def __init__(self, session: Session, dax_endpoints: List[str] = None):
        self.session = session
        self.client = session.client("dynamodb")
        self.dax = None

        if dax_endpoints is not None:
            self.dax = AmazonDaxClient(session, endpoints=dax_endpoints)

    def list_tables(self) -> List[str]:
        return self.client .list_tables()["TableNames"]

    def get_table_definition(self, name):
        definition = TableDefinition()
        response = self.client.describe_table(TableName=name)
        table = response["Table"]

        definition.name = table["TableName"]
        definition.arn = table["TableArn"]
        
        for attr in table["AttributeDefinitions"]:
            definition.attributes[attr["AttributeName"]] = attr["AttributeType"]

        definition.primary_key = KeyDefinition.from_key_schema(table['KeySchema'])

        for index_scope, index_dict in (("Global", definition.gsi), ("Local", definition.lsi)):
            index_type = f"{index_scope}SecondaryIndexes"
            if index_type in table:
                for index in table[index_type]:
                    keydef = KeyDefinition.from_key_schema(index["KeySchema"])
                    index_dict[index["IndexName"]] = keydef

        return definition

    @classmethod
    def get_default_client(cls, dax_endpoints = None):
        return cls(Session(), dax_endpoints)

    @property
    def data_client(self) -> dynamodb.Client:
        if self.dax is not None:
            return self.dax
        return self.client