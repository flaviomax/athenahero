from flask import Blueprint, make_response
from athenahero import db
from athenahero.database.models.query_execution import QueryExecution


# Blueprint Configuration
query_execution_loader_bp = Blueprint(
    'query_execution_loader_bp', __name__,
)

@query_execution_loader_bp.route('/query_execution_loader', methods=['POST'])
def query_execution_loader():
    """Persist one query execution object."""

    headers = {"Content-Type": "application/json"}
    return make_response(
        'Test worked!',
        200,
    )
