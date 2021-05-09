from django.db import models
import json
from overall.models import BaseModel
# Create your models here.


class Vendor(BaseModel):
    company_name = models.CharField(max_length=100,null=False)
    owner_name = models.CharField(max_length=100,null=True)
    owner_phone = models.IntegerField(null=True)
    contact_name = models.CharField(max_length=100,null=True,blank=True)
    contact_phone = models.IntegerField(null=True,blank=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=300,null=True,blank=True)
    city = models.CharField(max_length=150,null=True,blank=True)
    state = models.CharField(max_length=150,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    source = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return json.dumps({'id':self.id,'name':self.company_name})








