from rest_framework import serializers 
from usermgmt.models import *
 
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecorShopUser
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  'password'
                  )

