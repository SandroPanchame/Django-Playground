from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers

def say_hello(request):
    # try:
        # send_mail('subject','message', 'info@moshbuy.com', ['bob@moshbuy.com'])
        # mail for admins, the formating differs. html instead of plain text
        # mail_admins('subject', 'message', html_message='message')
        # message = EmailMessage('subject', 'message','from@moshbuy.com', ['john@moshbuy.com'])
        # message.attach_file('playground/static/images/images.png')
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Mosh'}
    #     )
    #     message.send(['john@moshbuy.com'])
    # except BadHeaderError:
    #     pass
    notify_customers.delay('Hello')
    return render(request, 'hello.html', {'name': 'Mosh'})
