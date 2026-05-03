from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Ticket

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    filter_by = request.args.get('filter', 'all')

    if filter_by == 'mine':
        tickets = Ticket.query.filter_by(assignee_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    elif filter_by == 'unassigned':
        tickets = Ticket.query.filter_by(assignee_id=None).order_by(Ticket.created_at.desc()).all()
    else:
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()

    return render_template('dashboard.html', tickets=tickets, filter_by=filter_by)