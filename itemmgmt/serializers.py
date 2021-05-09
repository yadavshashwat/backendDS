from rest_framework import serializers 
from itemmgmt.models import *
from overall.views import *
from django.forms.models import model_to_dict

class ItemCategorySerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    def validate_category(self,value):
        return cleanstring(value).lower()

    def validate_sub_category(self,value):
        return cleanstring(value).lower()

    def validate_description(self,value):
        return cleanstring(value).lower()

    class Meta:
        model = ItemCategory
        fields = '__all__'

class ItemSerializerIn(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    dimensions = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    sell_price = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    def validate_sell_price(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')

    def validate_name(self,value):
        return cleanstring(value).lower()

    def validate_dimensions(self,value):
        return cleanstring(value).lower()

    def validate_description(self,value):
        return cleanstring(value).lower()

    class Meta:
        model = Item
        exclude = ('category',)

class ItemSerializerOut(serializers.ModelSerializer):
    category_name = ItemCategorySerializer(source="category",read_only=True)
    class Meta:
        model = Item
        fields = ('name','description','dimensions','sell_price','category_name')


