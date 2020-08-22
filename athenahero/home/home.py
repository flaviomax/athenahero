from flask import Blueprint, render_template
from .monthly_chart_data_generator import data_read_by_day, data_read_by_workgroup, get_naive_queries_data

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/')
def home():
    """Landing page."""

    # Data read Daily
    labels, values = data_read_by_day()
    
    data_read_by_day_vars = {
        'values': values,
        'labels': [i.strftime('%Y-%m-%d') for i in labels],
        'legend':'Total Data Scanned in GB by day'
    }
    total_data_scanned = 0
    for value in values:
        total_data_scanned += value
    # total_data_scanned = "%.2f" % round(total_data_scanned,2)

    # Data read by workgroup
    w_labels, w_values = data_read_by_workgroup()
    data_read_by_workgroup_vars = {
        'values': w_values,
        'labels': w_labels,
        'legend':'Total Data Scanned in GB by Workgroup'
    }

    return render_template(
        'home.html',
        data_read_by_day_vars=data_read_by_day_vars,
        total_data_scanned=total_data_scanned,
        data_read_by_workgroup_vars=data_read_by_workgroup_vars
    )

@home_bp.route('/naive-queries')
def naive_queries():
    naive_queries_data = get_naive_queries_data()
    
    return render_template(
        'naive_queries.html',
        total_read_naive_queries=naive_queries_data["total_bytes_read"][0],
        # TODO: do not index this
        most_expensive_queries=naive_queries_data["most_expensive_queries"]
    )