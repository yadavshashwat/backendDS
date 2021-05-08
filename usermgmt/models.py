from django.db import models
from django.contrib.auth.models import AbstractUser
import json
from overall.models import BaseModel
# Create your models here.

# user_type = ['admin','staff']

class DecorShopUser(AbstractUser):
    phone_number = models.IntegerField(null=True)
    secret_string = models.CharField(max_length=20, null=True)
    auth_token    = models.CharField(max_length=20, null=True)
    otp = models.IntegerField(null=True)
    otp_time = models.DateTimeField(null=True)
    # define user access list
    # access types = r, rw, a | r = read, rw = readwrite, a = admin (delete priviledges)
    # has_xyz_mgmt_acces = models.BooleanField(default=False)
    def __str__(self):
        return json.dumps({'id':self.id,'name':self.first_name})
    




