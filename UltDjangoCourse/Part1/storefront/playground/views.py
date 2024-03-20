from django.shortcuts import render
# Not like View from MVC, more of a request handler
# Create your views here.

# request -> response
from django.http import HttpResponse
from store.models import *
from tags.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F

def say_hello(request):
    # These functions could pull from a database, send an email and so on
    # return HttpResponse('HelloWorld')
    # return render(request, 'hello.html')
    # x = calculate()
    # Basics of managers and query sets
    # query_set = Product.objects.all()
    # Django doesn't wuery the dataset until the variable is used
    # list(query_set)
    # query_set[0:5]
    # try: 
    #     product = Product.objects.get(pk=1)
        # pk = 1 primary key
    # except ObjectDoesNotExist:
    #     pass
    # # pk = 1 primary key
    
    # product = Product.objects.filter(pk=0).first()
    # exists = Product.objects.filter(pk=0).exists()
    # when using the filter method call you need a keyword followed by a value
    # keyword = value
    # queryset = Product.objects.filter(unit_price__range=(20,30))
    # print(queryset.count())
    # print(list(queryset.values()))
    # queryset = Customer.objects.filter(email__icontains=".com")
    # Products: inventory<10 AND price<20 
    # (add an argument to filter or use an additional filter method call) 
    # Using the OR operator
    # queryset=Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # F is for referencing other fields
    # queryset=Product.objects.filter(inventory=F('collection__id'))
    #  '-' : reverse order
    # queryset=Product.objects.order_by('unit_price','-title')
    TaggedItem.objects.get_tags_for(Product,1)
   
    return render(request, 'hello.html', {'name' : 'Mosh'})

# def calculate():
#     x = 1
#     y = 2
#     return x