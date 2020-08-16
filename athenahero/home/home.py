from flask import Blueprint, render_template
from .monthly_chart_data_generator import data_read_by_day

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/')
def home():
    """Landing page."""

    labels, values = data_read_by_day()
    
    legend = 'Data Scanned in GB'
    data_read_by_day_vars = {
        'values': values,
        'labels': [i.strftime('%Y-%m-%d') for i in labels],
        'legend':legend
    }

    return render_template('home.html', data_read_by_day_vars=data_read_by_day_vars)
