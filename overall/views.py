from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.core.paginator import Paginator

from overall.models import *

# import boto3
import datetime
import re
import random
import string
from datetime import datetime
import math

# Create your views here.


# Generic Functions
def cleanstring(query):
    query = query.strip()
    query = re.sub('\s{2,}', ' ', query)
    query = re.sub(r'^"|"$', '', query)
    return query


# <---------------- Set Cookie ------------------->

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)

# Random String Generator

def random_str_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

# Pagination Setup

def pagination(object,request):
        page_num = request.GET.get('page_num', "1")
        page_size = request.GET.get('page_size', "10")
        num_pages = 1
        total_records = object.count()
        if page_num != None and page_num != "":
            page_num = int(page_num)
            object = Paginator(object, int(page_size))
            try:
                object = object.page(page_num)
            except:
                object = object
            num_pages = int(math.ceil(total_records / float(int(page_size))))
        return({'object':object,'num_pages':num_pages,'total_records':total_records})

