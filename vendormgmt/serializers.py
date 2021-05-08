from rest_framework import serializers 
from vendormgmt.models import *
from overall.views import *

 
class VendorSerializer(serializers.ModelSerializer):
    contact_phone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    contact_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    pincode = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    def validate_contact_phone(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')
    
    def validate_pincode(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')
    
    def validate_contact_name(self,value):
        return cleanstring(value).lower()

    def validate_owner_name(self,value):
        return cleanstring(value).lower()

    def validate_contact_name(self,value):
        return cleanstring(value).lower()

    def validate_company_name(self,value):
        return cleanstring(value).lower()

    def validate_city(self,value):
        return cleanstring(value).lower()
    
    def validate_state(self,value):
        return cleanstring(value).lower()
    
    def validate_source(self,value):
        return cleanstring(value).lower()

    def validate_address(self,value):
        return cleanstring(value).lower()

    class Meta:
        model = Vendor
        fields = '__all__'



