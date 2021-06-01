from rest_framework import serializers 
from usermgmt.models import *
from overall.views import *

 
 
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DecorShopUser
#         fields = ('id',
#                   'first_name',
#                   'last_name',
#                   'email',
#                   'phone_number',
#                   )



class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    email = serializers.CharField(required=True, allow_null=False,allow_blank=False)
    first_name = serializers.CharField(required=False, allow_null=True,allow_blank=True)
    last_name = serializers.CharField(required=False, allow_null=True,allow_blank=True)
    # is_staff = serializers.CharField(required=False, allow_null=True,allow_blank=True)
    
    
    def validate_phone_number(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')
        
    def validate_email(self,value):
        return cleanstring(value).lower()

    def validate_first_name(self,value):
        return cleanstring(value).lower()


    def validate_last_name(self,value):
        return cleanstring(value).lower()



    class Meta:
        model = DecorShopUser
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  'is_active',
                  'is_staff'
                  )

