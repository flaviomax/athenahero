import uuid
import boto3
import pytest

from botocore.exceptions import HTTPClientError
from botocore.stub import Stubber, ANY
from athenahero.query_execution_loader.query_execution_loader_job import _parse_raw_query_execution, _list_all_workgroups, populate_month_of_executions, _get_successful_queries
from datetime import datetime, timedelta, timezone
from athenahero.database.models.query_execution import QueryExecution

from .test_base import app, db, session

def boto_list_query_executions_response(MaxResults=50, overload_vals = {}):
    if MaxResults == 0:
        payload = {}
    else:
        MaxResults = 50 if MaxResults > 50 else MaxResults
        ids = [str(uuid.uuid4()) for i in range(MaxResults)]
        payload = {
            "QueryExecutionIds": ids
        }
    return {**payload, **overload_vals}

def boto_batch_get_query_execution_response(query_ids = None, overload_vals = {}):
    if query_ids is None:
        query_ids = [str(uuid.uuid4()) for i in range(50)]
    payload = {
        "QueryExecutions": [get_query_execution_payload(query_id=i) for i in query_ids]
    }
    
    # mark one execution as failed
    if payload["QueryExecutions"]:
        payload["QueryExecutions"][-1]["Status"]["State"] = "FAILED"
    return payload

def get_query_execution_payload(query_id = None, overload_vals = {}):
    _id = query_id if query_id is not None else uuid.uuid4()
    payload = {
        "Query": "SELECT * FROM x",
        "QueryExecutionContext": { 
            "Database": "default" 
        },
        "QueryExecutionId": _id,
        "ResultConfiguration": {
            "OutputLocation": f"s3://aws-athena-query-results-account-region/{_id}.csv"
        },
        "StatementType": "DML",
        "Statistics": {
            "DataScannedInBytes": 54001664,
            "EngineExecutionTimeInMillis": 2168,
            "QueryPlanningTimeInMillis": 136,
            "QueryQueueTimeInMillis": 121,
            "ServiceProcessingTimeInMillis": 11,
            "TotalExecutionTimeInMillis": 2300
        },
        "Status": {
            "CompletionDateTime": datetime.now(timezone.utc) - timedelta(minutes=1),
            "State": "SUCCEEDED",
            "SubmissionDateTime": datetime.now(timezone.utc) - timedelta(minutes=10)
        },
        "WorkGroup": "primary"
    }
    return {**payload, **overload_vals}

def get_list_workgroups_response(overload_vals = {}):
    payload = {
        'WorkGroups': [
            {
                'Name': 'test_workgroup1',
                'State': 'ENABLED',
                'Description': '',
                'CreationTime': datetime(2015, 1, 1)
            },
            {
                'Name': 'test_workgroup2',
                'State': 'ENABLED',
                'Description': '',
                'CreationTime': datetime(2015, 1, 1)
            },
        ]
    }
    return {**payload, **overload_vals}


def test_query_execution_parser(session):
    temp_uuid = uuid.uuid4()
    payload = get_query_execution_payload(overload_vals={"QueryExecutionId":temp_uuid})
    query_execution = _parse_raw_query_execution(payload)
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

def test_workgroups_listing(session):
    athena_client = boto3.client('athena')
    workgroups_stubber = Stubber(athena_client)
    
    workgroups_first_response = get_list_workgroups_response({"NextToken": "abc"})
    workgroups_second_response = get_list_workgroups_response({
        'WorkGroups': [{
            'Name': 'test_workgroup3',
            'State': 'ENABLED',
            'Description': '',
            'CreationTime': datetime(2015, 1, 1)
        }]
    })
    workgroups_stubber.add_response('list_work_groups', workgroups_first_response, {})
    workgroups_stubber.add_response('list_work_groups', workgroups_second_response, {"NextToken": "abc"})
    
    with workgroups_stubber:
        workgroups = _list_all_workgroups(athena_client=athena_client)
    assert workgroups is not None
    assert len(workgroups) == 3
    assert 'test_workgroup1' in workgroups
    assert 'test_workgroup2' in workgroups
    assert 'test_workgroup3' in workgroups

def test_successful_queries_filter(session):
    athena_client = boto3.client("athena")
    query_ids = boto_list_query_executions_response(MaxResults=10)["QueryExecutionIds"]
    athena_stubber = Stubber(athena_client)
    athena_stubber.add_response(
        'batch_get_query_execution',
        boto_batch_get_query_execution_response(query_ids=query_ids),
        {"QueryExecutionIds": query_ids}
    )

    with athena_stubber:
        response = _get_successful_queries(athena_client=athena_client, query_ids=query_ids)

    assert response is not None
    assert len(response) == len(query_ids) - 1


def test_full_job(session):
    """Test a call to populate_month_of_executions."""
    athena_client = boto3.client('athena')
    athena_stubber = Stubber(athena_client)
    
    # ----------------------------------------------------
    # stub workgroups response
    # ----------------------------------------------------
    workgroups_first_response = get_list_workgroups_response({"NextToken": "abc"})
    workgroups_second_response = get_list_workgroups_response({
        'WorkGroups': [{
            'Name': 'test_workgroup3',
            'State': 'ENABLED',
            'Description': '',
            'CreationTime': datetime(2015, 1, 1)
        }]
    })
    athena_stubber.add_response('list_work_groups', workgroups_first_response, {})
    athena_stubber.add_response('list_work_groups', workgroups_second_response, {"NextToken": "abc"})
    
    # ----------------------------------------------------
    # stub operations for workgroup1
    # ----------------------------------------------------
    athena_stubber.add_response(
        'list_query_executions',
        boto_list_query_executions_response(),
        {'WorkGroup': 'test_workgroup1', 'MaxResults': 50}
    )
    workgroup1_response = boto_batch_get_query_execution_response()
    workgroup1_response["QueryExecutions"][10]["Status"]["CompletionDateTime"] = datetime.now(timezone.utc) - timedelta(days=90)
    for query_execution in workgroup1_response["QueryExecutions"]:
        query_execution["WorkGroup"] = "test_workgroup1"
    athena_stubber.add_response(
        'batch_get_query_execution',
        workgroup1_response,
        {"QueryExecutionIds": ANY}
    )

    # ----------------------------------------------------
    # stub operations for workgroup2
    # ----------------------------------------------------

    athena_stubber.add_response(
        'list_query_executions',
        boto_list_query_executions_response(MaxResults=0),
        {'WorkGroup': 'test_workgroup2', 'MaxResults': 50}
    )

    # ----------------------------------------------------
    # stub operations for workgroup3
    # ----------------------------------------------------
    athena_stubber.add_response(
        'list_query_executions',
        boto_list_query_executions_response(overload_vals={"NextToken": "abc"}),
        {'WorkGroup': 'test_workgroup3', 'MaxResults': 50}
    )
    workgroup3_first_response = boto_batch_get_query_execution_response()
    for query_execution in workgroup3_first_response["QueryExecutions"]:
        query_execution["WorkGroup"] = "test_workgroup3"
    athena_stubber.add_response(
        'batch_get_query_execution',
        workgroup3_first_response,
        {"QueryExecutionIds": ANY}
    )

    athena_stubber.add_response(
        'list_query_executions',
        boto_list_query_executions_response(),
        {'WorkGroup': 'test_workgroup3', 'MaxResults': 50, "NextToken": "abc"}
    )
    workgroup3_second_response = boto_batch_get_query_execution_response()
    for query_execution in workgroup3_second_response["QueryExecutions"]:
        query_execution["WorkGroup"] = "test_workgroup3"
    athena_stubber.add_response(
        'batch_get_query_execution',
        workgroup3_second_response,
        {"QueryExecutionIds": ANY}
    )

    # ----------------------------------------------------
    # finally, run the test
    # ----------------------------------------------------
    with athena_stubber:
        populate_month_of_executions(athena_client=athena_client)


    # ----------------------------------------------------
    # assertions
    # ----------------------------------------------------
    athena_stubber.assert_no_pending_responses()
    w1_queries = session.query(
        QueryExecution.id
    ).filter(
        QueryExecution.workgroup == 'test_workgroup1'
    ).all()

    assert w1_queries is not None
    assert len(w1_queries) == 49

    w2_queries = session.query(
        QueryExecution.id
    ).filter(
        QueryExecution.workgroup == 'test_workgroup2'
    ).all()

    assert w2_queries is not None
    assert len(w2_queries) == 0

    w3_queries = session.query(
        QueryExecution.id
    ).filter(
        QueryExecution.workgroup == 'test_workgroup3'
    ).all()

    assert w3_queries is not None
    assert len(w3_queries) == 98