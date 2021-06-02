from math import trunc
from django.db import models
import json
from overall.models import BaseModel
# Create your models here.


class ItemCategory(BaseModel):
    category     = models.CharField(max_length=50,null=False)
    sub_category = models.CharField(max_length=50,null=False)
    description  = models.CharField(max_length=300,null=True,blank=True)
    def __str__(self):
        return json.dumps({'id':self.id,'category':self.category,'sub_category':self.sub_category})

class Item(BaseModel):
    name        = models.CharField(max_length=200,null=False)
    description = models.CharField(max_length=500,null=True,blank=True)
    dimensions  = models.CharField(max_length=200,null=True,blank=True)
    sell_price  = models.IntegerField(null=True,blank=True)
    category    = models.ForeignKey(ItemCategory,
                                on_delete=models.SET_NULL,
                                null=True,blank=True)
    def __str__(self):
        return json.dumps({'id':self.id,'name':self.name})

class ItemImage(BaseModel):
    path                    = models.CharField(max_length=200,null=False)
    file_name               = models.CharField(max_length=200)
    file_type               = models.CharField(max_length=200)
    is_primary              = models.BooleanField(default=False)
    item                    = models.ForeignKey(Item,
                                on_delete=models.CASCADE,
                                null=False)

    def __str__(self):
        return json.dumps({'id':self.id,'item':self.item.name,'path':self.path})















