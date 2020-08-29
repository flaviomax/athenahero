import pytest

from .test_base import app, db, session, get_basic_query_execution
from athenahero.home.monthly_chart_data_generator import data_read_by_day, data_read_by_workgroup, get_queries_data, get_naive_queries_data
from datetime import datetime, timedelta
from statistics import mean 

def bytes2gb(data):
    return data / 1000000000.0

@pytest.fixture(scope="function")
def seed_db_objects(session):
    # query 1 is just a basic query
    query_execution1 = get_basic_query_execution()
    
    query_execution2 = get_basic_query_execution()
    query_execution2.submission_datetime = datetime.now() - timedelta(days=2)
    query_execution2.completion_datetime = datetime.now() - timedelta(days=1, hours=23)

    query_execution3 = get_basic_query_execution()
    query_execution3.workgroup = 'test_workgroup2'
    query_execution3.query_text = "select * from uau2"
    # make sure this is the most expensive query
    query_execution3.data_scanned_in_bytes = query_execution3.data_scanned_in_bytes + 1000000

    # query 4 makes query 3 naive
    query_execution4 = get_basic_query_execution()
    query_execution4.data_scanned_in_bytes = query_execution3.data_scanned_in_bytes
    query_execution4.workgroup = 'test_workgroup2'
    query_execution4.submission_datetime = datetime.now() - timedelta(days=2)
    query_execution4.completion_datetime = datetime.now() - timedelta(days=1, hours=23)
    query_execution4.query_text = "select * from uau2"

    session.add(query_execution1)
    session.add(query_execution2)
    session.add(query_execution3)
    session.add(query_execution4)
    session.commit()

    return query_execution1, query_execution2, query_execution3, query_execution4


# TODO: test empty versions
def test_data_read_by_day(seed_db_objects):
    query_execution1, query_execution2, query_execution3, query_execution4 = seed_db_objects
    labels, values = data_read_by_day()

    # there may be some time conflicts here, but it is unlikely
    assert labels == (datetime.today().date() - timedelta(days=2), datetime.today().date())
    assert values[0] == bytes2gb(query_execution2.data_scanned_in_bytes + query_execution4.data_scanned_in_bytes)
    assert values[1] == bytes2gb(query_execution1.data_scanned_in_bytes + query_execution3.data_scanned_in_bytes)

def test_data_read_by_workgroup(seed_db_objects):
    query_execution1, query_execution2, query_execution3, query_execution4 = seed_db_objects
    labels, values = data_read_by_workgroup()

    assert len(labels) == len(values) == 2
    results = sorted(list(zip(labels, values)))
    assert results[0] == ('test_workgroup', bytes2gb(query_execution1.data_scanned_in_bytes + query_execution2.data_scanned_in_bytes))
    assert results[1] == ('test_workgroup2', bytes2gb(query_execution3.data_scanned_in_bytes + query_execution4.data_scanned_in_bytes))

def test_get_queries_data(seed_db_objects):
    query_execution1, query_execution2, query_execution3, query_execution4 = seed_db_objects
    most_expensive_queries = get_queries_data()

    assert len(most_expensive_queries) == 2

    result = most_expensive_queries[0]
    assert result[0] == query_execution3.query_text
    assert result[1] == 2
    data_read = [query_execution3.data_scanned_in_bytes, query_execution4.data_scanned_in_bytes]
    assert float(result[2]) == bytes2gb(mean(data_read))
    assert float(result[3]) == bytes2gb(sum(data_read))

    result = most_expensive_queries[1]
    assert result[0] == query_execution1.query_text
    assert result[1] == 2
    data_read = [query_execution1.data_scanned_in_bytes, query_execution2.data_scanned_in_bytes]
    assert float(result[2]) == bytes2gb(mean(data_read))
    assert float(result[3]) == bytes2gb(sum(data_read))

def test_get_naive_queries_data(seed_db_objects):
    query_execution1, query_execution2, query_execution3, query_execution4 = seed_db_objects
    naive_queries = get_naive_queries_data()

    assert naive_queries["total_bytes_read"][0] == bytes2gb(query_execution3.data_scanned_in_bytes)

    queries = naive_queries["most_expensive_queries"]
    assert len(queries) == 1
    result = queries[0]

    assert result[0] == query_execution3.query_text
    assert result[1] == 1
    assert float(result[2]) == bytes2gb(query_execution3.data_scanned_in_bytes)
    assert float(result[3]) == bytes2gb(query_execution3.data_scanned_in_bytes)
