from flask import Blueprint, render_template
from .monthly_chart_data_generator import data_read_by_day, data_read_by_workgroup

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
