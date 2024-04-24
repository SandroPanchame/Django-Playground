from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage

def say_hello(request):
    try:
        # send_mail('subject','message', 'info@moshbuy.com', ['bob@moshbuy.com'])
        # mail for admins, the formating differs. html instead of plain text
        # mail_admins('subject', 'message', html_message='message')
        message = EmailMessage('subject', 'message','from@moshbuy.com', ['john@moshbuy.com'])
        message.attach_file('playground/static/images/images.png')
        message.send()
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
