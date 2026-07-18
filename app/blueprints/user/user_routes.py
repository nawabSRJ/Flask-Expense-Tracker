from flask import Blueprint, request, render_template, session, redirect, url_for, flash
import db_ops

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    user = session.get('user')
    if not user:
        flash('Please log in to continue', 'danger')
        return redirect(url_for('auth.login'))

    user_id = user['id']

    summary = db_ops.get_dashboard_summary(user_id)
    recent_expenses = db_ops.get_recent_expenses(user_id)
    categories = db_ops.get_categories(user_id)

    return render_template(
        'user/dashboard.html',
        user=user,
        summary=summary,
        recent_expenses=recent_expenses,
        categories=categories
    )