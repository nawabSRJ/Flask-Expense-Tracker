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