from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User


def send_via_email(email):
    subject = 'ICU application'
    message = f'Accept you to use ICU application'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.save()


def send_otp_via_email(email):
    subject = 'Reset Password'
    otp = random.randint(1000, 9999)
    message = f'Your code is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
