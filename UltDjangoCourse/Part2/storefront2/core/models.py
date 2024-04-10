from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# was created later in the project. Best practice is to get this working at the start of th project
# core had to be added into the settings file along with the AUTH_USER_MODEL variable
# if you're not sure on what needs to be added, use the pass keyword for the initial migration
# running into issues now because other models were dependent on another 'User' class
class User(AbstractUser):
    email=models.EmailField(unique=True)