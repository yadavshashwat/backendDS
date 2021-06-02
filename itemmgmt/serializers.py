from rest_framework import serializers 
from itemmgmt.models import *
from overall.views import *
from django.forms.models import model_to_dict
from rest_framework.serializers import Serializer, FileField

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
    category_details = ItemCategorySerializer(source="category",read_only=True)
    image_details = ItemImageSerializer(source='itemimage_set', many=True,read_only=True)   

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
        except ValueError:
            raise serializers.ValidationError('You must supply an valid category id')

    def validate_name(self,value):
        return cleanstring(value).lower()

    def validate_dimensions(self,value):
        return cleanstring(value).lower()

    def validate_description(self,value):
        return cleanstring(value).lower()

    class Meta:
        model = Item
        fields = ('id','name','description','dimensions','sell_price','category','category_details','image_details')


