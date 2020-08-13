import os
import uuid

import pytest
from datetime import datetime
import athenahero
from athenahero.database.models.query_execution import QueryExecution
from athenahero import db

@pytest.fixture
def client():
    conftest_file = os.path.join(os.getcwd(), 'tests/conftest.py')
    app = athenahero.create_app(conftest_file)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

def test_db_insert(client):
    temp_uuid = uuid.uuid4()
    query_execution = QueryExecution(
        id=temp_uuid,
        query_text='select * from uau',
        statement_type='DML',
        output_location='',
        encryption_option=None,
        kms_key=None,
        context_database=None,
        context_catalog=None,
        status='SUCCEEDED',
        last_state_change_reason=None,
        submission_datetime=datetime.now(),
        completion_datetime=datetime.now(),
        engine_execution_time_in_millis=123,
        total_execution_time_in_millis=123,
        query_queue_time_in_millis=123,
        query_planning_time_in_millis=123,
        service_processing_time_in_millis=123,
        data_manifest_location='uau.manifest',
        data_scanned_in_bytes=123
    )
    db.session.add(query_execution)
    db.session.commit()

    result = QueryExecution.query.get(temp_uuid)

    assert result is not None
    print(result)
