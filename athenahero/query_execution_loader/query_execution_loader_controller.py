import json

from flask import Blueprint, make_response, request

from athenahero import db
from athenahero.database.models.query_execution import QueryExecution

# Blueprint Configuration
query_execution_loader_bp = Blueprint(
    'query_execution_loader_bp', __name__,
)

def persist_query_execution(query_execution):
    db.session.add(query_execution)
    db.session.commit()

@query_execution_loader_bp.route('/query_execution_loader', methods=['POST'])
def query_execution_loader():
    """Persist one query execution object."""
    # TODO: send this to a `utils` file 
    request_data = json.loads(request.data)

    # TODO: validate request
    query_execution = QueryExecution(
        id=request_data['id'],
        query=request_data['id']
    )
    persist_query_execution(query_execution)

    response = make_response(
        {'message':'All Done!'},
        200,
    )
    response.headers['Content-Type'] = "application/json"
    return response
