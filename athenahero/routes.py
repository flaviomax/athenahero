from flask import current_app as app
from flask import render_template
from athenahero import db
from .database.models.query_execution import QueryExecution


@app.route('/')
def home():
    """Landing page."""

    _id = '8b37983f-438d-43e5-bc7c-2207997b3a09'
    query = 'select * from uau'
    qe = QueryExecution(
        id=_id,
        query=query
    )
    db.session.add(qe)
    db.session.commit()

    return render_template('home.html',
                           title="Jinja Demo Site",
                           description="Smarter page templates \
                                with Flask & Jinja.")
