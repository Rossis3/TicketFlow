from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Ticket, User, ActivityLog
from app.models import Ticket, User, ActivityLog, Comment

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

@tickets.route('/tickets/<int:ticket_id>/comment', methods=['POST'])
@login_required
def add_comment(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    body = request.form.get('body')

    if body:
        comment = Comment(
            body=body,
            author_id=current_user.id,
            ticket_id=ticket.id
        )
        db.session.add(comment)

        log = ActivityLog(
            action=f'Comment added by {current_user.username}',
            user_id=current_user.id,
            ticket_id=ticket.id
        )
        db.session.add(log)
        db.session.commit()
        flash('Comment added!')

    return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))


@tickets.route('/tickets/<int:ticket_id>/reassign', methods=['POST'])
@login_required
def reassign_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role != 'admin' and current_user.id != ticket.creator_id:
        flash('Only the creator or an admin can reassign this ticket.')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))

    new_assignee_id = request.form.get('assignee_id') or None
    old_assignee = ticket.assignee.username if ticket.assignee else 'Nobody'
    ticket.assignee_id = new_assignee_id

    new_assignee = User.query.get(new_assignee_id).username if new_assignee_id else 'Nobody'
    log = ActivityLog(
        action=f'Reassigned from {old_assignee} to {new_assignee} by {current_user.username}',
        user_id=current_user.id,
        ticket_id=ticket.id
    )
    db.session.add(log)
    db.session.commit()

    flash('Ticket reassigned!')
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))


@tickets.route('/tickets/<int:ticket_id>/delete', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role != 'admin' and current_user.id != ticket.creator_id:
        flash('Only the creator or an admin can delete this ticket.')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))

    # Delete related records first
    ActivityLog.query.filter_by(ticket_id=ticket.id).delete()
    Comment.query.filter_by(ticket_id=ticket.id).delete()

    db.session.delete(ticket)
    db.session.commit()

    flash('Ticket deleted.')
    return redirect(url_for('main.dashboard'))