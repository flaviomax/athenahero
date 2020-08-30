import os
import uuid
from datetime import datetime, timedelta
from random import randint

import pytest

import athenahero
from athenahero import db as _db
from athenahero.database.models.query_execution import QueryExecution


@pytest.fixture(scope="session")
def app(request):
    conftest_file = os.path.join(os.getcwd(), "tests/conftest.py")
    app = athenahero.create_app(conftest_file)
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app, request):
    """Session-wide test database."""

    def teardown():
        _db.drop_all()

    # _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


def get_basic_query_execution():
    temp_uuid = uuid.uuid4()
    return QueryExecution(
        id=temp_uuid,
        query_text="select * from uau",
        statement_type="DML",
        output_location="",
        encryption_option=None,
        kms_key=None,
        context_database=None,
        context_catalog=None,
        status="SUCCEEDED",
        last_state_change_reason=None,
        submission_datetime=datetime.now() - timedelta(minutes=1),
        completion_datetime=datetime.now(),
        engine_execution_time_in_millis=123,
        total_execution_time_in_millis=123,
        query_queue_time_in_millis=123,
        query_planning_time_in_millis=123,
        service_processing_time_in_millis=123,
        data_manifest_location="uau.manifest",
        data_scanned_in_bytes=randint(1, 1000000),
        workgroup="test_workgroup",
    )


def test_db_insert(session):
    query_execution = get_basic_query_execution()
    temp_uuid = query_execution.id
    session.add(query_execution)
    session.commit()

    result = QueryExecution.query.get(temp_uuid)

    assert result is not None
    assert result.id == temp_uuid
