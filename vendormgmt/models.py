from django.db import models
import json
from overall.models import BaseModel
# Create your models here.


class Vendor(BaseModel):
    company_name = models.CharField(max_length=100,null=False)
    owner_name = models.CharField(max_length=100,null=False)
    owner_phone = models.IntegerField(null=False)
    contact_name = models.CharField(max_length=100,null=True)
    contact_phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=300,null=True)
    city = models.CharField(max_length=150,null=True)
    state = models.CharField(max_length=150,null=True)
    pincode = models.IntegerField(null=True)
    source = models.CharField(max_length=100,null=True)
    def __str__(self):
        return json.dumps({'id':self.id,'name':self.company_name})








