from datetime import datetime
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from config.celery import app
from account.send_email import send_confirmation_email, send_confirmation_password




@app.task()
def send_connfirmation_email_task(email, code):
    send_confirmation_email(email, code)


@app.task()
def send_confirmation_password_task(email, code):
    send_confirmation_password(email, code)

@app.task(bind=True)
def clear_tokens(self):
    BlacklistedToken.objects.filter(token__expires_at__lt=datetime.now()).delete()
    OutstandingToken.objects.filter(expires_at__lt=datetime.now()).delete()
    return 'Deleted expired tokens'
