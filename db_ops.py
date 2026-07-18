# file to store the code for all the DB CRUD operations

from db import get_connection
from werkzeug.security import check_password_hash

def signup_user(user):
    # user is a dict
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """ 
                    INSERT INTO users (name, phone, email, password_hash, gender, dob)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        user['name'],
                        user['phone'],
                        user['email'],
                        user['password_hash'],
                        user['gender'],
                        user['dob']
                    )
                )
        finally:
            conn.close()
    except Exception as e:
        print('SignUp User Error : ', e)


def existing_email(email):
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT 1
                    FROM users
                    WHERE email = %s
                    LIMIT 1
                    """,
                    (email,)
                )

                return cur.fetchone() is not None   # returns bool value

        finally:
            conn.close()
            # NOTE : This will always execute, even if return is encountered in the try block, the interpreter first runs the finally block and then returns

    except Exception as e:
        print("Existing Email Error:", e)
        return False


from werkzeug.security import check_password_hash

def find_user(email, password):
    try:
        conn = get_connection()

        try:
            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT *
                    FROM users
                    WHERE email = %s
                    """,
                    (email,)
                )

                row = cur.fetchone()

                if row is None:
                    return {
                        "error": True,
                        "row": None
                    }

                if not check_password_hash(
                    row["password_hash"],
                    password
                ):
                    return {
                        "error": True,
                        "row": None
                    }

                return {
                    "error": False,
                    "row": row
                }

        finally:
            conn.close()

    except Exception as e:
        print(e)
        return {
            "error": True,
            "row": None
        }
    


def add_expense(user_id, data):
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO expenses (user_id, category_id, amount, description, payment_mode, expense_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        user_id,
                        data['category_id'],
                        data['amount'],
                        data['description'],
                        data['payment_mode'],
                        data['expense_date']
                    )
                )
                conn.commit()
                return True
        finally:
            conn.close()
    except Exception as e:
        print('Add Expense Error:', e)
        return False


def get_categories(user_id):
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT category_id, name
                    FROM categories
                    WHERE user_id = %s
                    ORDER BY name
                    """,
                    (user_id,)
                )
                return cur.fetchall()
        finally:
            conn.close()
    except Exception as e:
        print('Get Categories Error:', e)
        return []


def get_recent_expenses(user_id, limit=5):
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.expense_id, e.amount, e.description, e.payment_mode,
                           e.expense_date, c.name AS category_name
                    FROM expenses e
                    JOIN categories c ON e.category_id = c.category_id
                    WHERE e.user_id = %s
                    ORDER BY e.expense_date DESC, e.created_at DESC
                    LIMIT %s
                    """,
                    (user_id, limit)
                )
                return cur.fetchall()
        finally:
            conn.close()
    except Exception as e:
        print('Get Recent Expenses Error:', e)
        return []


def get_dashboard_summary(user_id):
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # total spent this month
                cur.execute(
                    """
                    SELECT COALESCE(SUM(amount), 0) AS total
                    FROM expenses
                    WHERE user_id = %s
                      AND MONTH(expense_date) = MONTH(CURDATE())
                      AND YEAR(expense_date) = YEAR(CURDATE())
                    """,
                    (user_id,)
                )
                month_total = cur.fetchone()['total']

                # all-time total
                cur.execute(
                    """
                    SELECT COALESCE(SUM(amount), 0) AS total
                    FROM expenses
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )
                all_time_total = cur.fetchone()['total']

                # category-wise breakdown (this month)
                cur.execute(
                    """
                    SELECT c.name AS category_name, COALESCE(SUM(e.amount), 0) AS total
                    FROM categories c
                    LEFT JOIN expenses e
                        ON e.category_id = c.category_id
                        AND MONTH(e.expense_date) = MONTH(CURDATE())
                        AND YEAR(e.expense_date) = YEAR(CURDATE())
                    WHERE c.user_id = %s
                    GROUP BY c.category_id, c.name
                    HAVING total > 0
                    ORDER BY total DESC
                    """,
                    (user_id,)
                )
                category_breakdown = cur.fetchall()

                # total number of transactions
                cur.execute(
                    """
                    SELECT COUNT(*) AS count
                    FROM expenses
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )
                total_transactions = cur.fetchone()['count']

                return {
                    'month_total': month_total,
                    'all_time_total': all_time_total,
                    'category_breakdown': category_breakdown,
                    'total_transactions': total_transactions
                }
        finally:
            conn.close()
    except Exception as e:
        print('Get Dashboard Summary Error:', e)
        return {
            'month_total': 0,
            'all_time_total': 0,
            'category_breakdown': [],
            'total_transactions': 0
        }