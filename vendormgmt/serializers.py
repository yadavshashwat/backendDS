from rest_framework import serializers 
from vendormgmt.models import *
 
 
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id',
                  'company_name',
                  'owner_name',
                  'owner_phone',
                  'contact_name',
                  'contact_phone',
                  'email',
                  'city',
                  'address',
                  'pincode',
                  'source'
                  )

