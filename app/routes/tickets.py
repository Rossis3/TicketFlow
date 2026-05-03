from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Ticket, User, ActivityLog

tickets = Blueprint('tickets', __name__)

@tickets.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    users = User.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        assignee_id = request.form.get('assignee_id') or None

        ticket = Ticket(
            title=title,
            description=description,
            priority=priority,
            assignee_id=assignee_id,
            creator_id=current_user.id
        )
        db.session.add(ticket)
        db.session.flush()  # gives ticket an id before commit

        log = ActivityLog(
            action=f'Ticket created by {current_user.username}',
            user_id=current_user.id,
            ticket_id=ticket.id
        )
        db.session.add(log)
        db.session.commit()

        flash('Ticket created!')
        return redirect(url_for('main.dashboard'))

    return render_template('new_ticket.html', users=users)


@tickets.route('/tickets/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    users = User.query.all()
    return render_template('view_ticket.html', ticket=ticket, users=users)


@tickets.route('/tickets/<int:ticket_id>/status', methods=['POST'])
@login_required
def update_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.id != ticket.assignee_id and current_user.role != 'admin':
        flash('Only the assignee or an admin can change status.')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))

    new_status = request.form.get('status')
    old_status = ticket.status
    ticket.status = new_status

    log = ActivityLog(
        action=f'Status changed from {old_status} to {new_status} by {current_user.username}',
        user_id=current_user.id,
        ticket_id=ticket.id
    )
    db.session.add(log)
    db.session.commit()

    flash('Status updated!')
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))