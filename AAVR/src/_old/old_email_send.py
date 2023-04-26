def email_send(user_name, otp):
    print("Sending Email")
    load_dotenv(find_dotenv())

    # Email Address for sender is written here
    email_address = os.getenv("EMAILSEND")
    password = os.getenv("EMAILPASS")

    # Email Address for receiver is written here
    email_address_receiver = os.getenv("EMAILSEND")

    # Email Subject
    subject = "Hello! Here is the OTP that you requested "

    # Email Body
    body = "Your OTP is " + otp + \
        ". Please say this OTP to verify your account to the robot once requested. Thank you very much!"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, password)
        server.sendmail(email_address, email_address_receiver, subject + body)
        server.quit()
    except Exception as E:
        print(str(E))
