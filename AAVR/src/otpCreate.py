import random

# 6 digit otp creation
def otpCreate():
    print("Creating OTP")
    otp = ''

    for i in range(6):
        num = random.randint(0, 9)
        otp += str(num)

    return int(otp)


# print(otpCreate())
