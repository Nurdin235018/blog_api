from django.core.mail import send_mail


def send_code(email, code):
    send_mail('Activation of account', f'You successfully login in our site. Activate code: {code}', 'test@gmail.com', [email])
