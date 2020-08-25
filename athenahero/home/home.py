from functools import wraps

from flask import Blueprint, make_response, render_template, request

from athenahero.config import config

from .monthly_chart_data_generator import (
    data_read_by_day,
    data_read_by_workgroup,
    get_naive_queries_data,
    get_queries_data,
)

# Blueprint Configuration
home_bp = Blueprint("home_bp", __name__, template_folder="templates", static_folder="static")


def auth_required(f):
    @wraps(f)
    def check_auth(*args, **kwargs):
        if config.ATHENAHERO_USERNAME is None and config.ATHENAHERO_PASSWORD is None:
            return f(*args, **kwargs)

        auth = request.authorization
        if (
            auth is not None
            and auth.username is not None
            and auth.password is not None
            and auth.username == config.ATHENAHERO_USERNAME
            and auth.password == config.ATHENAHERO_PASSWORD
        ):
            return f(*args, **kwargs)

        return make_response("Login Invalid", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})

    return check_auth


@home_bp.route("/")
@auth_required
def home():
    """Landing page."""

    # Data read Daily
    labels, values = data_read_by_day()

    data_read_by_day_vars = {
        "values": values,
        "labels": [i.strftime("%Y-%m-%d") for i in labels],
        "legend": "Total Data Scanned in GB by day",
    }
    total_data_scanned = 0
    for value in values:
        total_data_scanned += value
    # total_data_scanned = "%.2f" % round(total_data_scanned,2)

    # Data read by workgroup
    w_labels, w_values = data_read_by_workgroup()
    data_read_by_workgroup_vars = {
        "values": w_values,
        "labels": w_labels,
        "legend": "Total Data Scanned in GB by Workgroup",
    }

    return render_template(
        "home.html",
        data_read_by_day_vars=data_read_by_day_vars,
        total_data_scanned=total_data_scanned,
        data_read_by_workgroup_vars=data_read_by_workgroup_vars,
    )


@home_bp.route("/cost/queries")
@auth_required
def queries():
    most_expensive_queries = get_queries_data()

    return render_template("queries.html", most_expensive_queries=most_expensive_queries)


@home_bp.route("/cost/naive-queries")
@auth_required
def naive_queries():
    naive_queries_data = get_naive_queries_data()

    return render_template(
        "naive_queries.html",
        total_read_naive_queries=naive_queries_data["total_bytes_read"][0],
        # TODO: do not index this
        most_expensive_queries=naive_queries_data["most_expensive_queries"],
    )
