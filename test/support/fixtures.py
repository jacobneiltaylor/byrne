import os
import uuid

import boto3
from pytest import fixture, FixtureRequest

from . import helpers, constants


@fixture(scope="session")
def session_id():
    """
        Returns a random uuid for a unique test session
    """
    return helpers.get_uuid()


@fixture(scope="session")
def session_timestamp():
    """
        Returns a timestamp for the test session
    """
    return helpers.get_timestamp()


@fixture(scope="session")
def using_ddb_local():
    """
        Returns a timestamp for the test session
    """
    local = os.environ.get(constants.DYNAMODB_LOCAL_ENVVAR, None)

    if local is None:
        return False
    return True


@fixture(scope="session")
def aws(session_id, using_ddb_local):
    """
        Returns a Boto3 Session object
    """

    if using_ddb_local:
        return boto3.Session(
            f"{constants.DYNAMODB_LOCAL_ACCESS_KEY_ID}_{session_id}",
            constants.DYNAMODB_LOCAL_SECRET_ACCESS_KEY
        )

    aws_config = helpers.load_test_json_file("extra", "aws")

    account_id = aws_config["account_id"]
    role_name = aws_config["role_name"]
    region = aws_config["region"]
    external_id = os.environ.get(constants.STS_EXTERNAL_ID_ENVVAR, None)

    sts = boto3.Session(region_name=region).client("sts")

    assume_role_args = {
        "RoleArn": f"arn:aws:iam::{account_id}:role/{role_name}",
        "RoleSessionName": str(session_id),
        "DurationSeconds": aws_config["role_duration"]
    }

    if external_id is not None:
        assume_role_args["ExternalId"] = external_id

    test_role = sts.assume_role(**assume_role_args)
    creds = test_role["Credentials"]

    return boto3.Session(
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
        region_name=region
    )


@fixture(scope="session")
def ddb_client(aws, using_ddb_local):
    if using_ddb_local:
        endpoint = os.environ[constants.DYNAMODB_LOCAL_ENVVAR]
        return aws.client("dynamodb", endpoint_url=endpoint)
    return aws.client("dynamodb")


@fixture(scope="session")
def session_unified_id(session_id, session_timestamp):
    """
        Returns a uuid based on the session timestamp
        and random session id
    """
    return uuid.uuid5(session_id, str(session_timestamp))


@fixture(scope="session")
def table_id(session_unified_id):
    """
        Returns a short string based on the session id
        and timestamp for use in ephemeral table names.
    """
    return helpers.get_short_hash(str(session_unified_id))


@fixture(scope="function")
def ddb_table(request: FixtureRequest, table_id, ddb_client):
    """
        Returns a name of a ephemeral DynamoDB table
    """
    function = request.function
    function_name = function.__name__
    table = helpers.get_ephemeral_table_name(table_id, function_name)
    args = helpers.get_function_table_data(function)
    args["TableName"] = table
    ddb = helpers.get_byrne_client(ddb_client)
    ddb.client.create_table(**args)
    ddb.wait_for_active(table)
    yield table
    ddb.client.delete_table(TableName=table)
    ddb.wait_for_deletion(table)
