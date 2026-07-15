# file to store the code for all the DB CRUD operations

from db import get_connection

def signup_user(user):
    # user is a dict

    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """ 

                    """
                )
        finally:
            conn.close()
    except Exception as e:
        print('SignUp User Error : ', e)