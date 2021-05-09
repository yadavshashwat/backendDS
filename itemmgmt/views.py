from itemmgmt.models import *
# from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from itemmgmt.serializers import *
from overall.views import *


class itemCatMgmt:
    @api_view(['GET', 'POST', 'DELETE'])
    def object_list_v1(request):

        # to update - start
        dataObject = ItemCategory
        dataObjectFriendlyName = "Item Category"
        dataObjectFilterList = {}
        dataObjectSerializer = ItemCategorySerializer  
        natural_key_1 = 'category'
        natural_key_2 = 'sub_category'
        # to update - end

        if request.method == 'GET':
            objects = dataObject.objects.all()

            # to update filters - start
            category = request.GET.get('category', None)
            search = request.GET.get('search', None)
            if category is not None:
                category_list = category.split(",")
                objects = objects.filter(category__in=category_list)

            if search is not None:
                objects = objects.filter(Q(category__icontains=search) | Q(sub_category__icontains=search))

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
            
            count = 0 
            try:
                count = dataObject.objects.filter(category = cleanstring(object_data[natural_key_1]).lower(), sub_category = cleanstring(object_data[natural_key_2]).lower()).count()     
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
                message = dataObjectFriendlyName + " Already Exists!"
                errors = []
                obj = {
                    'success':success,
                    'message': message,
                    'errors': errors
                }
                return JsonResponse(obj, status=status.HTTP_400_BAD_REQUEST)
      
        elif request.method == 'DELETE':
            count = dataObject.objects.all().delete()
            success = True
            message = ('{} '+ dataObjectFriendlyName  + ' were deleted successfully!').format(count[0])
            obj= {
                'success':True,
                'message': message
                }
            return JsonResponse(obj, status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET', 'PUT', 'DELETE'])
    def object_detail_v1(request, id):
        
        # to update - start
        dataObject = ItemCategory
        dataObjectFriendlyName = "Item Category"
        dataObjectSerializer = ItemCategorySerializer    
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

            return JsonResponse(obj, status=status.HTTP_204_NO_CONTENT)
        

class itemMgmt:
    @api_view(['GET', 'POST', 'DELETE'])
    def object_list_v1(request):

        # to update - start
        dataObject = Item
        dataObjectFriendlyName = "Item"
        dataObjectFilterList = {}
        dataObjectSerializerIn = ItemSerializerIn  
        dataObjectSerializerOut = ItemSerializerOut  
        natural_key = 'name'
        # to update - end

        if request.method == 'GET':
            objects = dataObject.objects.all()

            # to update filters - start



            search = request.GET.get('search', None)
            category = request.GET.get('category', None)

            if category is not None:
                category_list = category.split(",")
                objects = objects.filter(category__in=category_list)

            if search is not None:
                objects = objects.filter(Q(name__icontains=search) | Q(description__icontains=search))

            # to update filters - end

            # Setting up pagination
            pagination_out = pagination(object=objects,request=request)
            object_serializer = dataObjectSerializerOut(pagination_out['object'], many=True)
            
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
                count = dataObject.objects.filter(name = cleanstring(object_data[natural_key]).lower()).count()     
            except:
                count = -1

            object_serializer = dataObjectSerializerIn(data=object_data)
            
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
                message = dataObjectFriendlyName + " Already Exists!"
                errors = []
                obj = {
                    'success':success,
                    'message': message,
                    'errors': errors
                }
                return JsonResponse(obj, status=status.HTTP_400_BAD_REQUEST)
      
        elif request.method == 'DELETE':
            count = dataObject.objects.all().delete()
            success = True
            message = ('{} '+ dataObjectFriendlyName  + ' were deleted successfully!').format(count[0])
            obj= {
                'success':True,
                'message': message
                }
            return JsonResponse(obj, status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET', 'PUT', 'DELETE'])
    def object_detail_v1(request, id):
        
        # to update - start
        dataObject = Item
        dataObjectFriendlyName = "Item"
        dataObjectSerializerIn = ItemSerializerIn    
        dataObjectSerializerOut = ItemSerializerOut    
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
            object_serializer = dataObjectSerializerOut(object) 
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
            object_serializer = dataObjectSerializerIn(object, data=object_data) 
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

            return JsonResponse(obj, status=status.HTTP_204_NO_CONTENT)
