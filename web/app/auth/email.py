from flask import render_template, current_app
from app.main.email import send_email


def send_password_reset_email(user):
    """
    Create message for reset password with token and call send email function
    """
    token = user.get_reset_password_token()
    send_email('[Assistant] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password_letter.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password_letter.html',
                                         user=user, token=token))
