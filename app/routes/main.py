from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Ticket

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    filter_by = request.args.get('filter', 'all')
    status_filter = request.args.get('status', 'all')

    query = Ticket.query

    # Apply assignee filter
    if filter_by == 'mine':
        query = query.filter_by(assignee_id=current_user.id)
    elif filter_by == 'unassigned':
        query = query.filter_by(assignee_id=None)

    # Apply status filter
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)

    tickets = query.order_by(Ticket.created_at.desc()).all()

    return render_template('dashboard.html', tickets=tickets, filter_by=filter_by, status_filter=status_filter)