import psycopg2
from SavingUser import *
from otpCreate import *
from email_send import *


def upload_user():

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

    # upload user data
    cursor.execute(
        "INSERT INTO users (user_name, otp) VALUES (%s, %s)", (user_name, otp))
