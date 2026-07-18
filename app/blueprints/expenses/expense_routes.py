from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from datetime import datetime
import db_ops

expense_bp = Blueprint('expense', __name__, url_prefix='/expense')

ALLOWED_PAYMENT_MODES = ('cash', 'card', 'upi', 'netbanking')


def validate_expense(data):
    # returns (True, None) if valid, else (False, "reason")
    # NOTE: category_id has already been resolved to a real numeric id
    # by the time this runs (see add_expense below), so 'new' is never seen here.

    if not data['category_id'] or not data['category_id'].isdigit():
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

    # Resolve "new category" BEFORE validation, since validate_expense
    # expects category_id to already be a real numeric id.
    if data['category_id'] == 'new':
        new_name = request.form.get('new_category_name', '').strip()

        if not new_name:
            flash('Category name is required', 'danger')
            return redirect(url_for('user.dashboard'))

        if len(new_name) > 50:
            flash('Category name too long (max 50 characters)', 'danger')
            return redirect(url_for('user.dashboard'))

        new_category_id = db_ops.create_category(user_id, new_name)

        if not new_category_id:
            flash('Could not create category', 'danger')
            return redirect(url_for('user.dashboard'))

        data['category_id'] = str(new_category_id)

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



# confirms whether the user is logged in and fetches that particular expense 
@expense_bp.route('/edit/<int:expense_id>', methods=['GET'])
def edit_expense_form(expense_id):
    user = session.get('user')
    if not user:
        flash('Please log in to continue', 'danger')
        return redirect(url_for('auth.login'))

    expense = db_ops.get_expense_by_id(expense_id, user['id'])
    if not expense:
        flash('Expense not found', 'danger')
        return redirect(url_for('user.dashboard'))

    categories = db_ops.get_categories(user['id'])
    return render_template('expenses/edit.html', expense=expense, categories=categories)


# actually edits the expenses
@expense_bp.route('/edit/<int:expense_id>', methods=['POST'])
def edit_expense(expense_id):
    user = session.get('user')
    if not user:
        flash('Please log in to continue', 'danger')
        return redirect(url_for('auth.login'))

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
        return redirect(url_for('expense.edit_expense_form', expense_id=expense_id))

    success = db_ops.update_expense(expense_id, user['id'], data)
    flash('Expense updated successfully' if success else 'Could not update expense',
          'success' if success else 'danger')
    return redirect(url_for('user.dashboard'))



@expense_bp.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    user = session.get('user')
    if not user:
        flash('Please log in to continue', 'danger')
        return redirect(url_for('auth.login'))

    success = db_ops.delete_expense(expense_id, user['id'])
    flash('Expense deleted' if success else 'Could not delete expense',
          'success' if success else 'danger')
    return redirect(url_for('user.dashboard'))