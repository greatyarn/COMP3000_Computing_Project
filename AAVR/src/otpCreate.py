import random


def otpCreate():
    print("Creating OTP")
    otp = ""

    # Create a for loop that will run 6 times
    for i in range(6):
        # Create a variable called num and set it to a random number between 0 and 9
        num = random.randint(0, 9)

        # Add the value of num to the end of the otp variable
        otp += str(num)

    return otp


# print(otpCreate())
