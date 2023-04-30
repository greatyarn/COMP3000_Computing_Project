import psycopg2
from SavingUser import *
from otpCreate import *
from email_send import *
from SavingEmail import *


def upload_user(user_name, otp, email_address):

    # Create a connection object to the PostgreSQL database server
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="db",
        user="admin",
        password="admin"
    )

    # Create a cursor object
    cursor = conn.cursor()

    user_name = str(user_name)
    otp = int(otp)
    email_address = str(email_address)

    print(type(user_name))  # Testing Purposes
    print("User Name by db.py: " + user_name)

    # upload user data
    cursor.execute(
        "INSERT INTO users (user_name, email_address, otp) VALUES (%s, %s, %s)", (user_name, email_address, otp))

    conn.commit()
    conn.close()
    cursor.close()


def email_check(email_address):

    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="db",
        user="admin",
        password="admin"
    )

    cursor = conn.cursor()

    EMAIL_ADDRESS = str(email_address)

    cursor.execute(
        "SELECT email_address FROM users WHERE email_address = %s", (EMAIL_ADDRESS,))

    if cursor.fetchone() is None:
        print("Email not found")
        return False
    else:
        print("Email found")
        return True

    conn.commit()
    conn.close()
    cursor.close()
