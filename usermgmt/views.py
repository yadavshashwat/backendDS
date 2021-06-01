from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view

from usermgmt.serializers import *
from overall.views import *

class userMgmt:
    @api_view(['GET', 'POST', 'DELETE'])
    def object_list_v1(request):

        # to update - start
        dataObject = DecorShopUser
        dataObjectFriendlyName = "User"
        dataObjectFilterList = {}
        dataObjectSerializer = UserSerializer  
        # to update - end

        if request.method == 'GET':
            objects = dataObject.objects.all()

            # to update filters - start
            name = request.GET.get('name', None)
            if name is not None:
                objects = objects.filter(name__icontains=name)
            
            # to update filters - end

            # Setting up pagination
            pagination_out = pagination(object=objects,request=request)
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
            # to update - case change - start
            try:
                object_data['name'] = cleanstring(object_data['name'].lower())
                object_data['address'] = cleanstring(object_data['address'].lower())
                object_data['city'] = cleanstring(object_data['city'].lower())
                object_data['state'] = cleanstring(object_data['state'].lower())
            except:
                None
                
            # to update - case change - end
            object_serializer = dataObjectSerializer(data=object_data)
            
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
        
        # elif request.method == 'DELETE':
        #     count = dataObject.objects.all().delete()
        #     success = True
        #     message = ('{} '+ dataObjectFriendlyName  + ' were deleted successfully!').format(count[0])
        #     obj= {
        #         'success':True,
        #         'message': message
        #         }
        #     return JsonResponse(obj)

    @api_view(['GET', 'PUT', 'DELETE'])
    def object_detail_v1(request, id):
        
        # to update - start
        dataObject = Hospital
        dataObjectFriendlyName = "Hospital"
        dataObjectSerializer = HospitalSerializer    
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
            obj ={
                    'success':success,
                    'message':message,
                    'data':data
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
            return JsonResponse(obj, status=status.HTTP_400_BAD_REQUEST) 
    
        elif request.method == 'DELETE': 
            object.delete() 
            success = True
            message = dataObjectFriendlyName + ' was deleted successfully!'
            obj= {
                'success':True,
                'message': message
                }

            return JsonResponse(obj)
        
            