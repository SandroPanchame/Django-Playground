from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    # birth_date = serializers.DateField(read_only = False)
    # used to have birthdate as a field, need to seperate responsibilities
    
    def save(self, **kwargs):
        user = super().save(**kwargs)
        Customer.objects.create(user=user)
        return super().save(**kwargs)
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','password',
                  'email', 'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']