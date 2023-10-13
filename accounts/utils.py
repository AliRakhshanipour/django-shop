from random import randint
from kavenegar import KavenegarAPI, APIException, HTTPException
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect


def send_otp_code(phone, otp_code):
    # try:
    #     api = KavenegarAPI(
    #         "5573454D375736516174694B482F4C7A5872456F71615376316777304239475737724D576F6953716A4B4D3D"
    #     )
    #     params = {
    #         "sender": "1000689696",
    #         "receptor": phone,
    #         "message": ".وب سرویس پیام کوتاه کاوه نگار",
    #     }
    #     response = api.sms_send(params)
    #     print(response)
    # except APIException as e:
    #     print(e)
    # except HTTPException as e:
    #     print(e)
    pass


def generate_otp_code():
    return randint(1000, 9999)


# def check_otp_code_expiration(code):
#     created_time = code.created.timestamp()
#     present_time = datetime.now().timestamp()
#     if created_time + 4 > present_time:
#         code.delete()
#         messages.error(request, "code is expired, please try again", "danger")
#         return redirect("accounts:user-register")
