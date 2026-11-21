import bcrypt

from auth.database import get_connection
from auth.database import get_connection

def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed):

    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )
from auth.database import get_connection


def register_user(name, email, password):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, hashed_password)
        )

        conn.commit()

        return True, "Account created successfully."

    except Exception:

        return False, "Email already exists."

    finally:

        conn.close()


def login_user(email, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return False, None

    if verify_password(password, user["password"]):
        return True, user

    return False, None
def add_to_watchlist(user_id, symbol, company):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO watchlist(
                user_id,
                symbol,
                company
            )

            VALUES(?,?,?)
            """,
            (user_id, symbol, company)
        )

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()
def remove_from_watchlist(user_id, symbol):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM watchlist

        WHERE user_id=?
        AND symbol=?
        """,
        (user_id, symbol)
    )

    conn.commit()

    conn.close()

def get_watchlist(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM watchlist

        WHERE user_id=?

        ORDER BY company
        """,
        (user_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data