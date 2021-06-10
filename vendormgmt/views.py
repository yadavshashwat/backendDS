from vendormgmt.models import Vendor
# from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from vendormgmt.serializers import *
from overall.views import *
import operator
from overall.models import cities_india, states_ut_india
from backendDS.credentials import AWS_S3_ACCESS_KEY, AWS_S3_SECRET_KEY
import time
import boto3
import os

class vendorMgmt:
    @api_view(['GET', 'POST', 'DELETE'])
    def object_list_v1(request):

        # to update - start
        dataObject = Vendor
        dataObjectFriendlyName = "Vendor"
        dataObjectFilterList = {}
        dataObjectSerializer = VendorSerializer  
        natural_key = 'company_name'
        # to update - end

        if request.method == 'GET':
            objects = dataObject.objects.all()
            dataObjectFilterList['sort_by'] = [
                            {'value':'company_name','label':'Company Name'},
                            {'value':'owner_name','label':'Owner Name'},
                            {'value':'contact_name','label':'Other Contact Name'},
                            {'value':'city','label':'City'},
                            {'value':'state','label':'State'}
                        ]
            dataObjectFilterList['order_by'] = [{'value':'asc','label':'Ascending'},
                            {'value':'desc','label':'Descending'}]

            dataObjectFilterList['source'] = []
            for source in objects:
                dataObjectFilterList['source'].append({
                    'value':source.source,
                    'label':(source.source).title()
                    })


            dataObjectFilterList['source'] = {v['value']:v for v in dataObjectFilterList['source']}.values()
            dataObjectFilterList['source'] = sorted(dataObjectFilterList['source'], key=operator.itemgetter('value'))


            dataObjectFilterList['cities'] = []
            for city in cities_india:
                dataObjectFilterList['cities'].append({
                    'value':city,
                    'label':(city).title()
                    })

            dataObjectFilterList['states'] = []
            for state in states_ut_india:
                dataObjectFilterList['states'].append({
                    'value':state,
                    'label':(state).title()
                    })


            # to update filters - start

            state = request.GET.get('state', None)
            city = request.GET.get('city', None)
            search = request.GET.get('search', None)
            sort_by = request.GET.get('sort_by', None)
            order = request.GET.get('order', None)
            is_all = request.GET.get('is_all', None)
            
            if state !=None and state !="" and state != "none":
                state_list = state.split(",")
                objects = objects.filter(state__in=state_list)

            if city !=None and city !="" and city != "none":
                city_list = city.split(",")
                objects = objects.filter(city__in=city_list)

            if search !=None and search !="" and search != "none":
                objects = objects.filter(Q(company_name__icontains=search) | Q(owner_name__icontains=search))

            if sort_by !=None and sort_by !="" and sort_by != "none":
                if order == "asc":
                    objects = objects.order_by(sort_by)
                else:
                    objects = objects.order_by("-" + sort_by)

            # to update filters - end

            # Setting up pagination
            if is_all != 0 and is_all !=None and is_all != "":
                pagination_out = pagination(object=objects,request=request)
            else:
                pagination_out = {'object':objects,'num_pages':1,'total_records':objects.count()}
            object_serializer = dataObjectSerializer(pagination_out['object'], many=True)
            
            num_pages = pagination_out['num_pages']
            total_records = pagination_out['total_records']
            data = object_serializer.data
            filters = dataObjectFilterList
            success = True
            message = "Found "+ dataObjectFriendlyName +" Records"
            obj = {
                    'success':success,
                    'filters':filters,
                    'num_pages':num_pages,
                    'total_records':total_records,
                    'message':message,
                    'data':data
                    }

            return JsonResponse(obj, safe=False)
    
        elif request.method == 'POST':
            object_data = JSONParser().parse(request)
            
            count = 0 
            try:
                count = dataObject.objects.filter(company_name = cleanstring(object_data[natural_key]).lower()).count()     
            except:
                count = -1

            object_serializer = dataObjectSerializer(data=object_data)
            
            if count == 0:
                if object_serializer.is_valid():
                    object_serializer.save()
                    success = True
                    message = dataObjectFriendlyName + " Created!"
                    data = object_serializer.data
                    obj= {
                        'success':True,
                        'message':message,
                        'data': data
                    }
                    return JsonResponse(obj, status=status.HTTP_201_CREATED) 
                
                else:
                    success = False
                    message = "Invalid Serializer!"
                    errors = object_serializer.errors
                    obj = {
                        'success':success,
                        'message': message,
                        'errors': errors
                    }
                    return JsonResponse(obj, status=status.HTTP_400_BAD_REQUEST)

            elif count == -1:
                if object_serializer.is_valid():
                    success = False
                    message = dataObjectFriendlyName + " Search Error!"
                    errors = []
                    obj = {
                        'success':success,
                        'message': message,
                        'errors': errors
                    }
                    return JsonResponse(obj, status=status.HTTP_400_BAD_REQUEST)
                else:
                    success = False
                    message = "Invalid Serializer!"
                    errors = object_serializer.errors
                    obj = {
                        'success':success,
                        'message': message,
                        'errors': errors
                    }
                    return JsonResponse(obj, status=status.HTTP_400_BAD_REQUEST)
            else:
                success = False
                message = dataObjectFriendlyName + " Already Exists!"
                errors = []
                obj = {
                    'success':success,
                    'message': message,
                    'errors': errors
                }
                return JsonResponse(obj)

        
        elif request.method == 'DELETE':
            count = dataObject.objects.all().delete()
            success = True
            message = ('{} '+ dataObjectFriendlyName  + ' were deleted successfully!').format(count[0])
            obj= {
                'success':True,
                'message': message
                }
            return JsonResponse(obj)

    @api_view(['GET', 'PUT', 'DELETE'])
    def object_detail_v1(request, id):
        
        # to update - start
        dataObject = Vendor
        dataObjectFriendlyName = "Vendor"
        dataObjectSerializer = VendorSerializer  
        dataObjectFilterList = {}

        # to update - end

        try: 
            object = dataObject.objects.get(id=id) 
        except dataObject.DoesNotExist: 
            message = 'The ' + dataObjectFriendlyName + ' does not exist'
            success = False
            obj = {
                    'message': message,
                    'success': success
                }
            return JsonResponse(obj, status=status.HTTP_404_NOT_FOUND) 
    
        if request.method == 'GET': 
            object_serializer = dataObjectSerializer(object) 
            message = dataObjectFriendlyName + " Found!"
            success = True
            data = object_serializer.data

            dataObjectFilterList['source'] = []

            for source in Vendor.objects.all():
                dataObjectFilterList['source'].append({
                    'value':source.source,
                    'label':(source.source).title()
                    })
            dataObjectFilterList['source'] = {v['value']:v for v in dataObjectFilterList['source']}.values()
            dataObjectFilterList['source'] = sorted(dataObjectFilterList['source'], key=operator.itemgetter('value'))


            dataObjectFilterList['cities'] = []
            for city in cities_india:
                dataObjectFilterList['cities'].append({
                    'value':city,
                    'label':(city).title()
                    })

            dataObjectFilterList['states'] = []
            for state in states_ut_india:
                dataObjectFilterList['states'].append({
                    'value':state,
                    'label':(state).title()
                    })
            
            obj ={
                    'success':success,
                    'message':message,
                    'data':data,
                    'filters':dataObjectFilterList
                }
            return JsonResponse(obj) 
    
        elif request.method == 'PUT': 
            object_data = JSONParser().parse(request) 
            object_serializer = dataObjectSerializer(object, data=object_data) 
            if object_serializer.is_valid(): 
                object_serializer.save() 
                success = True
                data = object_serializer.data
                message = dataObjectFriendlyName + " Updated!"
                obj ={
                    'success':success,
                    'message':message,
                    'data':data
                }
                return JsonResponse(obj) 
            else:
                success = False
                errors = object_serializer.errors
                message = "Unable to update " + dataObjectFriendlyName
                obj = {
                    'success':False,
                    'message':message,
                    'errors': errors
                }
            return JsonResponse(obj) 
    
        elif request.method == 'DELETE': 
            object.delete() 
            success = True
            message = dataObjectFriendlyName + ' was deleted successfully!'
            obj= {
                'success':True,
                'message': message
                }

            return JsonResponse(obj)
        
    @api_view(['POST'])
    def upload_document(request,id):
        dataObject = Vendor
        dataObjectFriendlyName = "Vendor"
        bucket_name = "thedecorshop"
        files = request.FILES.getlist("file")
        # file_name = request.POST.get('file_name', None)
        # print(file_name)
        # print(files)
        # files_name = request.FILES.getlist("file")

        # destination = open('filename.data', 'wb')
        # print(files)
        # print(len(files))
        obj = {}
        data = []

        try: 
            object = dataObject.objects.get(id=id) 

        except dataObject.DoesNotExist: 
            message = 'The ' + dataObjectFriendlyName + ' does not exist'
            success = False
            obj = {
                    'message': message,
                    'success': success
                }
            return JsonResponse(obj, status=status.HTTP_404_NOT_FOUND) 
        # print(len(file))
        
        count = 0
        for file in files:
            split_tup = os.path.splitext(file.name)
            destination = open('filename.data', 'wb')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
            session = boto3.Session(
                aws_access_key_id = AWS_S3_ACCESS_KEY,
                aws_secret_access_key = AWS_S3_SECRET_KEY,
            )
            s3 = session.resource('s3')
            ts = time.time()
            final_filename = "doc-" + random_str_generator(4) + str(ts).replace(".", "") + split_tup[1]
            s3.Object(bucket_name, 'documents/' + final_filename).put(Body=open('filename.data', 'rb'))
            filepath = "https://"+bucket_name +".s3.ap-south-1.amazonaws.com/documents/" + final_filename
            

            fileupload = VendorDocuments.objects.create(
                                                file_name  = final_filename,
                                                path       = filepath,
                                                vendor       = object,
                                                friendly_name = split_tup[0]
                                                )
        

            if os.path.exists('filename.data'):
                os.remove('filename.data')
            count = count + 1
            data.append({ 'id':fileupload.id,
                            'file_name':fileupload.file_name,
                           'path':fileupload.path,
                           'friendly_name':fileupload.friendly_name
                        })

        if count == len(files):
            success = True
            message = "Uploaded "+ str(count) +" of " + str(len(files)) +" documents"
            obj = {
                    'success':success,
                    'object_id':object.id,
                    'message':message,
                    'data':data   
                    }
        else:
            success = False
            message = "Uploaded "+ str(count) +" of " + str(len(files)) +" documents"
            obj = {
                    'success':success,
                    'object_id':object.id,
                    'message':message,
                    'data':data   
                    }

        return JsonResponse(obj, safe=False)

    @api_view(['DELETE'])
    def delete_document(request,id):
        dataObject = VendorDocuments
        dataObjectFriendlyName = "Vendor Document"
        bucket_name = "thedecorshop"
        # destination = open('filename.data', 'wb')
        
        obj = {}
        data = []
        try: 
            object = dataObject.objects.get(id=id) 

        except dataObject.DoesNotExist: 
            message = 'The ' + dataObjectFriendlyName + ' does not exist'
            success = False
            obj = {
                    'message': message,
                    'success': success
                }
            return JsonResponse(obj, status=status.HTTP_404_NOT_FOUND) 
        # print(len(file))

        session = boto3.Session(
            aws_access_key_id = AWS_S3_ACCESS_KEY,
            aws_secret_access_key = AWS_S3_SECRET_KEY,
        )
        s3 = session.resource('s3')
        print(object.file_name)
        s3.Object(bucket_name, 'documents/' + object.file_name).delete()
        object.delete()
        success = True
        message = dataObjectFriendlyName + ' was deleted successfully!'
        obj= {
            'success':True,
            'message': message
            }
        return JsonResponse(obj)

            