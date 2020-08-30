"""Module for Fetching all query execution data from Athena."""
import logging
from datetime import datetime, timedelta, timezone

import boto3
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from athenahero import db
from athenahero.database.models.query_execution import QueryExecution


def _get_next_query_ids(athena_client, next_token, workgroup):
    if next_token is not None:
        return athena_client.list_query_executions(NextToken=next_token, MaxResults=50, WorkGroup=workgroup)
    else:
        return athena_client.list_query_executions(MaxResults=50, WorkGroup=workgroup)


def _get_successful_queries(athena_client, query_ids):
    query_executions = athena_client.batch_get_query_execution(QueryExecutionIds=query_ids).get("QueryExecutions")
    return [q for q in query_executions if q["Status"].get("State") == "SUCCEEDED"]


def _extract_workgroup_names_from_payload(workgroups_payload):
    return [i["Name"] for i in workgroups_payload["WorkGroups"]]


def _list_all_workgroups(athena_client):
    response = athena_client.list_work_groups()
    all_workgroups = _extract_workgroup_names_from_payload(response)
    while response.get("NextToken") is not None:
        response = athena_client.list_work_groups(NextToken=response["NextToken"])
        all_workgroups += _extract_workgroup_names_from_payload(response)
    return sorted(list(set(all_workgroups)))


def _parse_raw_query_execution(raw_query_execution):
    # parse content into local vars
    encryption_option, kms_key = None, None
    if raw_query_execution.get("EncryptionConfiguration") is not None:
        encryption_option = raw_query_execution["EncryptionConfiguration"].get("EncryptionOption")
        kms_key = raw_query_execution["EncryptionConfiguration"].get("KmsKey")
    statistics = raw_query_execution["Statistics"]

    query_execution = QueryExecution(
        id=raw_query_execution["QueryExecutionId"],
        query_text=raw_query_execution["Query"],
        statement_type=raw_query_execution["StatementType"],
        output_location=raw_query_execution["ResultConfiguration"].get("OutputLocation"),
        encryption_option=encryption_option,
        kms_key=kms_key,
        context_database=raw_query_execution["QueryExecutionContext"].get("Database"),
        context_catalog=raw_query_execution["QueryExecutionContext"].get("Catalog"),
        status=raw_query_execution["Status"].get("State"),
        last_state_change_reason=raw_query_execution["Status"].get("StateChangeReason"),
        submission_datetime=raw_query_execution["Status"].get("SubmissionDateTime"),
        completion_datetime=raw_query_execution["Status"].get("CompletionDateTime"),
        workgroup=raw_query_execution["WorkGroup"],
        engine_execution_time_in_millis=statistics.get("EngineExecutionTimeInMillis"),
        total_execution_time_in_millis=statistics.get("TotalExecutionTimeInMillis"),
        query_queue_time_in_millis=statistics.get("QueryQueueTimeInMillis"),
        query_planning_time_in_millis=statistics.get("QueryPlanningTimeInMillis"),
        service_processing_time_in_millis=statistics.get("ServiceProcessingTimeInMillis"),
        data_manifest_location=statistics.get("DataManifestLocation"),
        data_scanned_in_bytes=statistics.get("DataScannedInBytes"),
    )

    return query_execution


def populate_month_of_executions(athena_client=None, deltadays=30):
    logging.info("[query_execution_job] Starting")
    if athena_client is None:
        athena_client = boto3.client("athena")
    min_day = datetime.now(timezone.utc) - timedelta(days=deltadays)
    min_found = datetime.now(timezone.utc)
    next_token = None
    all_workgroups = _list_all_workgroups(athena_client)

    for workgroup in all_workgroups:
        logging.info(f"[query_execution_job] Fetching data for workgroup {workgroup}")
        while min_found > min_day:
            next_queries = _get_next_query_ids(athena_client, next_token, workgroup)
            next_ids = next_queries.get("QueryExecutionIds")
            if not next_ids:
                break

            executions = _get_successful_queries(athena_client, next_ids)
            _save_batch_query_executions_to_db(executions)
            min_found = min([i["Status"].get("CompletionDateTime") for i in executions])
            logging.info(f"[query_execution_job] Fetched queries up to {min_found}")

            if next_queries.get("NextToken") is None:
                break
            next_token = next_queries["NextToken"]

        min_day = datetime.now(timezone.utc) - timedelta(days=deltadays)
        min_found = datetime.now(timezone.utc)
        next_token = None

    logging.info("[query_execution_job] Done!")


def _save_batch_query_executions_to_db(batch_query_executions):
    for raw_query_execution in batch_query_executions:
        query_execution = _parse_raw_query_execution(raw_query_execution)
        _save_query_execution_to_db(query_execution)


def _save_query_execution_to_db(query_execution):
    db.session.add(query_execution)
    try:
        db.session.commit()
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        db.session.rollback()
