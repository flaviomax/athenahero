import boto3
import json
from datetime import datetime, timedelta, timezone
from athenahero.database.models.query_execution import QueryExecution

def _get_next_query_ids(athena_client, next_token):
    if next_token is not None:
        return athena_client.list_query_executions(
            NextToken=next_token,
            MaxResults=50
        )
    else:
        return athena_client.list_query_executions(
            MaxResults=50
        )

def _get_successful_queries(athena_client, query_ids):
    query_executions = athena_client.batch_get_query_execution(
        QueryExecutionIds=query_ids
    ).get('QueryExecutions')
    return [q for q in query_executions if q['Status'].get('State') == 'SUCCEEDED']

def _parse_raw_query_execution(raw_query_execution):
    # parse content into local vars
    encryption_option, kms_key = None, None
    if raw_query_execution.get('EncryptionConfiguration') is not None:
        encryption_option = raw_query_execution['EncryptionConfiguration'].get('EncryptionOption')
        kms_key = raw_query_execution['EncryptionConfiguration'].get('KmsKey')
    statistics = raw_query_execution['Statistics']

    query_execution = QueryExecution(
        id=raw_query_execution['QueryExecutionId'],
        query_text=raw_query_execution['Query'],
        statement_type=raw_query_execution['StatementType'],
        output_location=raw_query_execution['ResultConfiguration'].get('OutputLocation'),
        encryption_option=encryption_option,
        kms_key=kms_key,
        context_database=raw_query_execution['QueryExecutionContext'].get('Database'),
        context_catalog=raw_query_execution['QueryExecutionContext'].get('Catalog'),
        status=raw_query_execution['Status'].get('State'),
        last_state_change_reason=raw_query_execution['Status'].get('StateChangeReason'),
        submission_datetime=raw_query_execution['Status'].get('SubmissionDateTime'),
        completion_datetime=raw_query_execution['Status'].get('CompletionDateTime'),
        engine_execution_time_in_millis=statistics.get('EngineExecutionTimeInMillis'),
        total_execution_time_in_millis=statistics.get('TotalExecutionTimeInMillis'),
        query_queue_time_in_millis=statistics.get('QueryQueueTimeInMillis'),
        query_planning_time_in_millis=statistics.get('QueryPlanningTimeInMillis'),
        service_processing_time_in_millis=statistics.get('ServiceProcessingTimeInMillis'),
        data_manifest_location=statistics.get('DataManifestLocation'),
        data_scanned_in_bytes=statistics.get('DataScannedInBytes') 
    )

    print(query_execution)
    

def get_all_query_executions(deltadays=1):
    print('starting execution')
    athena_client = boto3.client('athena')
    min_day = datetime.now(timezone.utc) - timedelta(hours=deltadays)
    min_found = datetime.now(timezone.utc)
    next_token = None
    total_executions = []
    
    while min_found > min_day:
        next_queries = _get_next_query_ids(athena_client, next_token) 
        next_ids = next_queries.get('QueryExecutionIds')
        next_token = next_queries.get('NextToken')
        
        # TODO: for v0, we will only be fetching successful queries
        executions = _get_successful_queries(athena_client, next_ids)
        total_executions += executions
        min_found = min([i['Status'].get('CompletionDateTime') for i in executions])
        print(min_found)
        
    return total_executions

def save_execution_to_file():
    executions = get_all_query_executions()
    with open('uau.json', 'w') as f:
        f.write(json.dumps(executions, indent=4, sort_keys=True, default=str))

if __name__ == '__main__':
    save_execution_to_file()
