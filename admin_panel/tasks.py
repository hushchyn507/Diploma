import asyncio
import time

from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from Diploma.celery import app


@app.task(bind=True)
def send_email(self,html_content="<p>This is an <strong>important</strong> message.</p>",to=['dg.junior19@gmail.com']):
    subject, from_email, = "hello", "hushchynd@gmail.com"
    to = to
    text_content = "This is an important message."
    html_content = html_content
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    time.sleep(10)
    msg.send()
    return 1
