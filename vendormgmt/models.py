# from django.conf import FILE_CHARSET_DEPRECATED_MSG
from django.db import models
import json
from overall.models import BaseModel
# Create your models here.


class Vendor(BaseModel):
    company_name = models.CharField(max_length=100,null=False)
    owner_name = models.CharField(max_length=100,null=True,blank=True)
    owner_phone = models.IntegerField(null=True,blank=True)
    contact_name = models.CharField(max_length=100,null=True,blank=True)
    contact_phone = models.IntegerField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address = models.CharField(max_length=300,null=True,blank=True)
    city = models.CharField(max_length=150,null=True,blank=True)
    state = models.CharField(max_length=150,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    source = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return json.dumps({'id':self.id,'name':self.company_name})


class VendorDocuments(BaseModel):
    path                    = models.CharField(max_length=200,null=False)
    file_name               = models.CharField(max_length=200)
    friendly_name           = models.CharField(max_length=200)
    vendor                  = models.ForeignKey(Vendor,
                                on_delete=models.CASCADE,
                                null=False)
    def __str__(self):
        return json.dumps({'id':self.id,'item':self.item.name,'path':self.path})









