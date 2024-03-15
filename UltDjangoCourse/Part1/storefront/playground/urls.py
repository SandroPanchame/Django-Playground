# added after initial setup of app, shows up when starting project instead of app
# For mapping urls to functions
from django.urls import path
from . import views

# URLConf(iguration)
urlpatterns = [
    path('hello/', views.say_hello),
    # we would use playground/hello incase it wasn't being referenced in the main application
    # since it is being referenced in storefront/urls.py, we can be fine with just /hello
]