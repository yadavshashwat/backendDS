from rest_framework import serializers 
from vendormgmt.models import *
from overall.views import *

class VendorDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDocuments
        fields = ('id','path','file_name','friendly_name')


class VendorSerializer(serializers.ModelSerializer):
    contact_phone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    contact_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    pincode = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    state = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    source = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    owner_name = serializers.CharField(required=False, allow_null=True,allow_blank=True)
    owner_phone = serializers.CharField(required=False, allow_null=True,allow_blank=True)
    company_name = serializers.CharField(required=True, allow_null=False,allow_blank=False)
    document_details = VendorDocSerializer(source='vendordocuments_set', many=True,read_only=True)   
    
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



