from django.shortcuts import render
# Not like View from MVC, more of a request handler
# Create your views here.

# request -> response
from django.http import HttpResponse
def say_hello(request):
    # These functions could pull from a database, send an email and so on
    # return HttpResponse('HelloWorld')
    # return render(request, 'hello.html')
    x = calculate()
    return render(request, 'hello.html', {'name' : 'Mosh'})

def calculate():
    x = 1
    y = 2
    return x