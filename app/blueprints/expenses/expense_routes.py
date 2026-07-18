from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from datetime import datetime
import db_ops

expense_bp = Blueprint('expense', __name__, url_prefix='/expense')

ALLOWED_PAYMENT_MODES = ('cash', 'card', 'upi', 'netbanking')


def validate_expense(data):
    # returns (True, None) if valid, else (False, "reason")

    if not data['category_id']:
        return False, 'Category is required'

    if not data['category_id'].isdigit():
        return False, 'Invalid category'

    if not data['amount']:
        return False, 'Amount is required'

    try:
        amount_val = float(data['amount'])
        if amount_val <= 0:
            return False, 'Amount must be greater than 0'
    except ValueError:
        return False, 'Amount must be a valid number'

    if not data['expense_date']:
        return False, 'Date is required'

    try:
        datetime.strptime(data['expense_date'], '%Y-%m-%d')
    except ValueError:
        return False, 'Invalid date format'

    if data['payment_mode'] not in ALLOWED_PAYMENT_MODES:
        return False, 'Invalid payment mode'

    if data['description'] and len(data['description']) > 255:
        return False, 'Description too long (max 255 characters)'

    return True, None


@expense_bp.route('/add', methods=['POST'])
def add_expense():
    # NEW — matches your actual session structure
    user = session.get('user')
    if not user:
        flash('Please log in to continue', 'danger')
        return redirect(url_for('auth.login'))

    user_id = user['id']

    data = {
        'category_id': request.form.get('category_id'),
        'amount': request.form.get('amount'),
        'description': request.form.get('description', '').strip(),
        'expense_date': request.form.get('expense_date'),
        'payment_mode': request.form.get('payment_mode')
    }

    valid, error_msg = validate_expense(data)
    if not valid:
        flash(error_msg, 'danger')
        return redirect(url_for('user.dashboard'))

    success = db_ops.add_expense(user_id, data)

    if success:
        flash('Expense added successfully', 'success')
    else:
        flash('Something went wrong while adding expense', 'danger')

    return redirect(url_for('user.dashboard'))