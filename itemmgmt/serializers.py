from rest_framework import serializers 
from itemmgmt.models import *
from overall.views import *
from django.forms.models import model_to_dict
from rest_framework.serializers import Serializer, FileField
from vendormgmt.serializers import *

class ItemCategorySerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    category = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    sub_category = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    
    def validate_category(self,value):
        return cleanstring(value).lower()

    def validate_sub_category(self,value):
        return cleanstring(value).lower()

    def validate_description(self,value):
        return cleanstring(value).lower()

    class Meta:
        model = ItemCategory
        fields = '__all__'

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('id','path','file_name','file_type','is_primary')

class ItemSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    dimensions = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    sell_price = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    category = serializers.CharField(required=False, allow_null=True, allow_blank=True,write_only=True)
    vendorlist = serializers.CharField(required=False, allow_null=True, allow_blank=True,read_only=True)
    category_details = ItemCategorySerializer(source="category",read_only=True)
    image_details = ItemImageSerializer(source='itemimage_set', many=True,read_only=True)   
    status = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    def validate_sell_price(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')
    
    def validate_category(self,value):
        if not value:
            return None
        try:
            catObject = ItemCategory.objects.get(id=value)
            return catObject
        except:
            raise serializers.ValidationError('You must supply an valid category id')


    def validate_name(self,value):
        return cleanstring(value).lower()

    def validate_dimensions(self,value):
        return cleanstring(value).lower()

    def validate_description(self,value):
        return cleanstring(value).lower()

    class Meta:
        model = Item
        fields = ('id','name','description','vendorlist','dimensions','status','sell_price','category','category_details','image_details')


class VendorItemSerializer(serializers.ModelSerializer):
    vendor = serializers.CharField(required=False, allow_null=True, allow_blank=True,write_only=True)
    item = serializers.CharField(required=False, allow_null=True, allow_blank=True,write_only=True)
    cost_price = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    item_details = ItemSerializer(source="item",read_only=True)
    vendor_details = VendorSerializer(source="vendor",read_only=True)

    def validate_cost_price(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')

    def validate_vendor(self,value):
        if not value:
            return None
        try:
            venObject = Vendor.objects.get(id=value)
            return venObject
        except:
            raise serializers.ValidationError('You must supply an valid vendor id')

    def validate_item(self,value):
        if not value:
            return None
        try:
            itemObject = Item.objects.get(id=value)
            return itemObject
        except:
            raise serializers.ValidationError('You must supply an valid item id')


    class Meta:
        model = VendorItem
        fields = ('id','cost_price','vendor','item','item_details','vendor_details')
