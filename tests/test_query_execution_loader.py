import uuid
import boto3
import pytest

from botocore.exceptions import HTTPClientError
from athenahero.query_execution_loader.query_execution_loader_job import _parse_raw_query_execution, _list_all_workgroups

from .test_base import app, db, session


def test_query_execution_parser(session):
    temp_uuid = uuid.uuid4()
    raw_query_execution = {
        "Query": "SELECT * FROM test_table",
        "QueryExecutionContext": {},
        "QueryExecutionId": temp_uuid,
        "ResultConfiguration": {"OutputLocation": f"s3://aws-athena-query-results-account-us-west-2/{temp_uuid}.csv"},
        "StatementType": "DML",
        "Statistics": {
            "DataScannedInBytes": 1174405,
            "EngineExecutionTimeInMillis": 1753,
            "QueryPlanningTimeInMillis": 896,
            "QueryQueueTimeInMillis": 181,
            "ServiceProcessingTimeInMillis": 1,
            "TotalExecutionTimeInMillis": 1935,
        },
        "Status": {
            "CompletionDateTime": "2020-08-10 08:07:48.637000-03:00",
            "State": "SUCCEEDED",
            "SubmissionDateTime": "2020-08-10 08:07:46.702000-03:00",
        },
        "WorkGroup": "primary",
    }
    query_execution = _parse_raw_query_execution(raw_query_execution)
    assert query_execution is not None
    assert query_execution.id == temp_uuid

    # use db as model validator
    session.add(query_execution)
    session.commit()
    assert query_execution.query.get(temp_uuid) is not None

def test_boto3_http_prevention(session):
    athena_client = boto3.client('athena')
    with pytest.raises(HTTPClientError):
        workgroups = _list_all_workgroups(athena_client)
