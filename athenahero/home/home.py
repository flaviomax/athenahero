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

    return render_template('home.html', values=values, labels=labels, legend=legend)
