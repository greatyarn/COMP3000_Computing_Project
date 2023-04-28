import psycopg2
from SavingUser import *
from otpCreate import *
from email_send import *


def upload_user(user_name, otp):

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

    print(type(user_name))  # Testing Purposes
    print("User Name by db.py: " + user_name)

    # upload user data
    cursor.execute(
        "INSERT INTO users (user_name, otp) VALUES (%s, %s)", (user_name, otp))

    conn.commit()
    conn.close()
    cursor.close()
