from django.core.mail import send_mail
from django.conf import settings
import string
import random


from django.core.mail import send_mail
from django.conf import settings

#temporary password
def generate_temporary_password(length=10):
    """Generate a random temporary password."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def send_account_email(user_email, full_name, role, temp_password):
    role_text = "Faculty Admin" if role == 'ADMIN' else "Student"
    subject = "Your FASSA Account Has Been Created"
    message = f"""
Hello {full_name},

An account has been created for you as a FASSA {role_text}.
Here are your login details:

Email: {user_email}
Temporary Password: {temp_password}

Login here: http://127.0.0.1:8000/api/accounts/login/

Please change your password after logging in.

Regards,
FASSA
"""
    from_email = f"FASSA <{settings.EMAIL_HOST_USER}>"
    send_mail(subject, message, from_email, [user_email], fail_silently=False)

#verify account
def send_student_verification_otp(email, full_name, otp):
    subject = "Verify Your FASSA Account"
    message = f"""
Hello {full_name},

Your FASSA account verification OTP is: {otp}

It will expire in 5 minutes.

If you did not register, please ignore this email.

Regards,
FASSA
"""
    from_email = f"FASSA <{settings.EMAIL_HOST_USER}>"
    send_mail(subject, message, from_email, [email], fail_silently=False)


#reset password
def send_password_reset_otp(email, otp):
    """
    Sends a 6-digit OTP to the user's email for password reset.
    """
    subject = "FASSA Password Reset OTP"
    message = f"""
Hello,

Your OTP code to reset your FASSA password is:

{otp}

It expires in 5 minutes.

If you did not request this, please ignore this email.

Regards,
FASSA
"""
    from_email = f"FASSA <{settings.EMAIL_HOST_USER}>"
    send_mail(subject, message, from_email, [email], fail_silently=False)


# accounts/utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_verification_otp(email, otp):
    """
    Sends account verification OTP to user's email.
    """
    subject = "Your Account Verification Code"
    message = f"Your OTP code is: {otp}\nIt will expire in 5 minutes."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)



