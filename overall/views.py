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

def random_str_generator(size=6, chars=string.ascii_uppercase + string.digits):
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


# def upload_image(request):
    
# def upload_file(request):
#     obj = {}
#     obj['status'] = False
#     obj['result'] = []
#     obj['message'] = "Request Recieved!"
#     filetype = get_param(request, 'filetype', None)
#     # if request.user.is_authenticated and request.user.is_staff:
#     if filetype:
#         if filetype=='image':
#             given_filename = request.FILES["file"].name
#             file = request.FILES["file"]
#             destination = open('filename.data', 'wb')
#             for chunk in file.chunks():
#                 destination.write(chunk)
#             destination.close()
#             s3 = boto3.resource('s3')
#             ts = time.time()
#             created_at = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#             final_filename = "img-" + random_str_generator(2) + str(ts).replace(".", "")  + ".jpg" 
#             s3.Object(bucket_name, 'images/' + final_filename).put(Body=open('filename.data', 'rb'))
#             filepath = "https://s3.amazonaws.com/"+bucket_name+"/images/"+final_filename
#             if request.user.is_anonymous:
#                 fileupload = FileUpload.objects.create(initial_file_name = given_filename,
#                                                         final_file_name  = final_filename,
#                                                         file_path        = filepath,
#                                                         uploaded_at      = created_at,
#                                                         file_type        = "image",
#                                                         created_by       = None
#                                                         )
#             else:
#                 fileupload = FileUpload.objects.create(initial_file_name = given_filename,
#                                                         final_file_name  = final_filename,
#                                                         file_path        = filepath,
#                                                         uploaded_at      = created_at,
#                                                         file_type        = "image",
#                                                         created_by       = request.user
#                                                         )
               
#             if os.path.exists('filename.data'):
#                 os.remove('filename.data')
#             obj['status'] = True
#             obj['message'] = "Image Uploaded!"
#             try:
#                 if fileupload.created_by:
#                     user_out = json.loads(str(fileupload.created_by))
#                 else:
#                     user_out = str(fileupload.created_by)
#             except:
#                 user_out = None

#             obj['result'].append(
#                 {'id':fileupload.id,
#                 'initial_file_name':fileupload.initial_file_name,
#                 'final_file_name':fileupload.final_file_name,
#                 'file_path':fileupload.file_path,
#                 'uploaded_at':str(fileupload.uploaded_at),
#                 'file_type':fileupload.file_type,
#                 'created_by':user_out
#                 })

#     return HttpResponse(json.dumps(obj), content_type='application/json')

