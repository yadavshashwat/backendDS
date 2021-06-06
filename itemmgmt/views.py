from itemmgmt.models import *
# from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from itemmgmt.serializers import *
from overall.views import *
import boto3
import time
import os
import operator
from backendDS.credentials import AWS_S3_ACCESS_KEY, AWS_S3_SECRET_KEY
from overall.models import states_ut_india, cities_india

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
            dataObjectFilterList['sort_by'] = [
                            {'value':'category','label':'Category'},
                            {'value':'sub_category','label':'Sub Category'},
                        ]
            dataObjectFilterList['order_by'] = [{'value':'asc','label':'Ascending'},
                            {'value':'desc','label':'Descending'}]

            category_list = ItemCategory.objects.all()
            dataObjectFilterList['category'] = []
            for item in category_list:
                dataObjectFilterList['category'].append({
                    'value':item.category,
                    'label':(item.category).title()
                    })
            dataObjectFilterList['category'] = {v['value']:v for v in dataObjectFilterList['category']}.values()
            dataObjectFilterList['category'] = sorted(dataObjectFilterList['category'], key=operator.itemgetter('value'))
            


            objects = dataObject.objects.all()

            # to update filters - start
            category = request.GET.get('category', None)
            search = request.GET.get('search', None)
            sort_by = request.GET.get('sort_by', None)
            order = request.GET.get('order', None)
            is_all = request.GET.get('is_all', None)

            if category !=None and category !="" and category != "none":
                category_list = category.split(",")
                objects = objects.filter(category__in=category_list)

            if search !=None and search !="" and search != "none":
                objects = objects.filter(Q(category__icontains=search) | Q(sub_category__icontains=search))

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
        
class itemMgmt:
    @api_view(['GET', 'POST', 'DELETE'])
    def object_list_v1(request):

        # to update - start
        dataObject = Item
        dataObjectFriendlyName = "Item"
        dataObjectFilterList = {}
        dataObjectSerializer = ItemSerializer  
        natural_key = 'name'
        # to update - end

        if request.method == 'GET':

            dataObjectFilterList['sort_by'] = [
                            {'value':'name','label':'Name'},
                            {'value':'category__category','label':'Category'},
                        ]
            dataObjectFilterList['order_by'] = [{'value':'asc','label':'Ascending'},
                            {'value':'desc','label':'Descending'}]

            category_list = ItemCategory.objects.all()
            dataObjectFilterList['category'] = []
            for item in category_list:
                dataObjectFilterList['category'].append({
                    'value':item.id,
                    'label':(item.category + " | " + item.sub_category).title()
                    })

            dataObjectFilterList['status'] = [
                                            {'value':'to_be_updated','label':'To Be Updated'},
                                            {'value':'rejected','label':'Rejected'},
                                            {'value':'shortlisted','label':'Shortlisted'},
                                            {'value':'ready','label':'Ready'}
                                            ]

            objects = dataObject.objects.all()

            # to update filters - start

            category = request.GET.get('category', None)
            statusitem = request.GET.get('status', None)
            search = request.GET.get('search', None)
            sort_by = request.GET.get('sort_by', None)
            order = request.GET.get('order', None)

            if category !=None and category !="" and category != "none":
                category_list = category.split(",")
                objects = objects.filter(category__in=category_list)

            if statusitem !=None and statusitem !="" and statusitem != "none":
                status_list = statusitem.split(",")
                objects = objects.filter(status__in=status_list)

            if search !=None and search !="" and search != "none":
                objects = objects.filter(Q(name__icontains=search) | Q(description__icontains=search))

            if sort_by !=None and sort_by !="" and sort_by != "none":
                if order == "asc":
                    objects = objects.order_by(sort_by)
                else:
                    objects = objects.order_by("-" + sort_by)

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
                count = dataObject.objects.filter(name = cleanstring(object_data[natural_key]).lower()).count()     
            except:
                count = -1

            object_serializer = dataObjectSerializer(data=object_data)
            if count == 0:
                if object_serializer.is_valid():
                    object_serializer.save()
                    success = True
                    message = dataObjectFriendlyName + " Created!"
                    data = object_serializer.data
                    # print(data)
                    itemObj = dataObject.objects.get(id=data['id'])
                    try:
                        vendor_id_list = object_data['vendorlist'].split(",")
                        vendObjects = Vendor.objects.filter(id__in=vendor_id_list)
                        for object in vendObjects:
                            VendorItem.objects.create(
                                item = itemObj,
                                vendor = object
                            )
                    except:
                        None
                    
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
        dataObject = Item
        dataObjectFriendlyName = "Item"
        dataObjectSerializer = ItemSerializer    
        # dataObjectSerializerOut = ItemSerializerOut    
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
                itemObj = dataObject.objects.get(id=data['id'])
                try:
                    vendor_id_list = object_data['vendorlist'].split(",")
                    # print(len(vendor_id_list))
                    if len(vendor_id_list)>0 and vendor_id_list[0] != "":
                        vendObjects = Vendor.objects.filter(id__in=vendor_id_list)
                    else:
                        vendObjects = []
                    ExistingVendorItems = VendorItem.objects.filter(item = itemObj)
                    existingVendors = []
                    for object in ExistingVendorItems:
                        if object.vendor in vendObjects:
                            existingVendors.append(object.vendor)
                        else:
                            object.delete()
                    
                    

                    for obj in vendObjects:
                        if obj in existingVendors:
                            pass
                        else:
                            VendorItem.objects.create(
                            item = itemObj,
                            vendor = obj
                            )
                except:
                    None
                
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

    # def upload_image(request):
    @api_view(['POST'])
    def upload_item_image(request,id):
        dataObject = Item
        dataObjectFriendlyName = "Item"
        bucket_name = "thedecorshop"
        files = request.FILES.getlist("file")
        # destination = open('filename.data', 'wb')
        print(files)
        print(len(files))
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
        totalOldImages = ItemImage.objects.filter(item = object).count()
        count = 0
        for file in files:
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
            final_filename = "img-" + random_str_generator(4) + str(ts).replace(".", "")  + ".jpg" 
            s3.Object(bucket_name, 'images/' + final_filename).put(Body=open('filename.data', 'rb'))


            filepath = "https://"+bucket_name +".s3.ap-south-1.amazonaws.com/images/" + final_filename
            if totalOldImages == 0 and count == 0:
                is_primary = True
            else:
                is_primary = False

            fileupload = ItemImage.objects.create(
                                                file_name  = final_filename,
                                                path       = filepath,
                                                file_type  = "image",
                                                item       = object,
                                                is_primary = is_primary
                                                )
        

            if os.path.exists('filename.data'):
                os.remove('filename.data')
            count = count + 1
            data.append({ 'id':fileupload.id,
                            'file_name':fileupload.file_name,
                           'path':fileupload.path,
                           'file_type':fileupload.file_type
                        })

        if count == len(files):
            success = True
            message = "Uploaded "+ str(count) +" of " + str(len(files)) +" images"
            obj = {
                    'success':success,
                    'object_id':object.id,
                    'message':message,
                    'data':data   
                    }
        else:
            success = False
            message = "Uploaded "+ str(count) +" of " + str(len(files)) +" images"
            obj = {
                    'success':success,
                    'object_id':object.id,
                    'message':message,
                    'data':data   
                    }

        return JsonResponse(obj, safe=False)

    @api_view(['DELETE'])
    def delete_item_image(request,id):
        dataObject = ItemImage
        dataObjectFriendlyName = "Item Image"
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
        s3.Object(bucket_name, 'images/' + object.file_name).delete()
        object.delete()
        success = True
        message = dataObjectFriendlyName + ' was deleted successfully!'
        obj= {
            'success':True,
            'message': message
            }
        return JsonResponse(obj)


class vendorItemMgmt:
    @api_view(['POST'])
    def object_create_v1(request):
        # to update - start
        dataObject = VendorItem
        dataObjectFriendlyName = "Vendor Item"

        dataObjectFilterList = {}
        dataObjectSerializer = VendorItemSerializer  
        natural_key_1 = 'vendor'
        natural_key_2 = 'item'
        # to update - end

        # if request.method == 'GET':
        #     dataObjectFilterList['sort_by'] = [
        #                     {'value':'category','label':'Category'},
        #                     {'value':'sub_category','label':'Sub Category'},
        #                 ]
        #     dataObjectFilterList['order_by'] = [{'value':'asc','label':'Ascending'},
        #                     {'value':'desc','label':'Descending'}]

        #     category_list = ItemCategory.objects.all()
        #     dataObjectFilterList['category'] = []
        #     for item in category_list:
        #         dataObjectFilterList['category'].append({
        #             'value':item.category,
        #             'label':(item.category).title()
        #             })
        #     dataObjectFilterList['category'] = {v['value']:v for v in dataObjectFilterList['category']}.values()
        #     dataObjectFilterList['category'] = sorted(dataObjectFilterList['category'], key=operator.itemgetter('value'))
            

        #     objects = dataObject.objects.all()

        #     # to update filters - start
        #     category = request.GET.get('category', None)
        #     search = request.GET.get('search', None)
        #     sort_by = request.GET.get('sort_by', None)
        #     order = request.GET.get('order', None)
        #     is_all = request.GET.get('is_all', None)

        #     if category !=None and category !="" and category != "none":
        #         category_list = category.split(",")
        #         objects = objects.filter(category__in=category_list)

        #     if search !=None and search !="" and search != "none":
        #         objects = objects.filter(Q(category__icontains=search) | Q(sub_category__icontains=search))

        #     if sort_by !=None and sort_by !="" and sort_by != "none":
        #         if order == "asc":
        #             objects = objects.order_by(sort_by)
        #         else:
        #             objects = objects.order_by("-" + sort_by)

        #     # to update filters - end

        #     # Setting up pagination
        #     if is_all != 0 and is_all !=None and is_all != "":
        #         pagination_out = pagination(object=objects,request=request)
        #     else:
        #         pagination_out = {'object':objects,'num_pages':1,'total_records':objects.count()}

        #     object_serializer = dataObjectSerializer(pagination_out['object'], many=True)
            
        #     num_pages = pagination_out['num_pages']
        #     total_records = pagination_out['total_records']
        #     data = object_serializer.data
        #     filters = dataObjectFilterList
        #     success = True
        #     message = "Found "+ dataObjectFriendlyName +" Records"
        #     obj = {
        #             'success':success,
        #             'filters':filters,
        #             'num_pages':num_pages,
        #             'total_records':total_records,
        #             'message':message,
        #             'data':data
        #             }

        #     return JsonResponse(obj, safe=False)
    
        object_data = JSONParser().parse(request)
        
        count = 0 
        try:
            count = dataObject.objects.filter(vendor = object_data[natural_key_1], item = object_data[natural_key_2]).count()     
        except:
            count = -1

        object_serializer = dataObjectSerializer(data=object_data)
        
        if count == 0:
            if object_serializer.is_valid():
                object_serializer.save()
                success = True
                message = dataObjectFriendlyName + " Added!"
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
    
        # elif request.method == 'DELETE':
        #     count = dataObject.objects.all().delete()
        #     success = True
        #     message = ('{} '+ dataObjectFriendlyName  + ' were deleted successfully!').format(count[0])
        #     obj= {
        #         'success':True,
        #         'message': message
        #         }
        #     return JsonResponse(obj)

    @api_view(['GET'])
    def object_list_item_vendor_v1(request,id):
        dataObject = VendorItem
        dataObjectFriendlyName = "Item Vendor"

        dataObjectFilterList = {}
        dataObjectSerializer = VendorItemSerializer  
        natural_key_1 = 'vendor'
        natural_key_2 = 'item'
        # to update - end

        dataObjectFilterList['sort_by'] = [
                        {'value':'vendor__company_name','label':'Company Name'},
                        {'value':'vendor__owner_name','label':'Owner Name'},
                        {'value':'vendor__contact_name','label':'Other Contact Name'},
                        {'value':'vendor__city','label':'City'},
                        {'value':'vendor__state','label':'State'},
                        {'value':'cost_price','label':'Cost Price'}
                    ]
        dataObjectFilterList['order_by'] = [{'value':'asc','label':'Ascending'},
                        {'value':'desc','label':'Descending'}]

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


        # to update filters - start

        state = request.GET.get('state', None)
        city = request.GET.get('city', None)
        search = request.GET.get('search', None)
        sort_by = request.GET.get('sort_by', None)
        order = request.GET.get('order', None)
        is_all = request.GET.get('is_all', None)
        objects = dataObject.objects.filter(item__id = id)
        
        if state !=None and state !="" and state != "none":
            state_list = state.split(",")
            objects = objects.filter(vendor__state__in=state_list)

        if city !=None and city !="" and city != "none":
            city_list = city.split(",")
            objects = objects.filter(vendor__city__in=city_list)

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

    def object_list_vendor_item_v1(request,id):
        dataObject = VendorItem
        dataObjectFriendlyName = "Vendor Item"

        dataObjectFilterList = {}
        dataObjectSerializer = VendorItemSerializer  
        natural_key_1 = 'vendor'
        natural_key_2 = 'item'
        # to update - end
        objects = dataObject.objects.filter(vendor__id = id)
        dataObjectFilterList['sort_by'] = [
                        {'value':'item__name','label':'Item Name'},
                        {'value':'cost_price','label':'Cost Price'},
                        # {'value':'sub_category','label':'Sub Category'},
                    ]
        dataObjectFilterList['order_by'] = [{'value':'asc','label':'Ascending'},
                        {'value':'desc','label':'Descending'}]

        category_list = ItemCategory.objects.all()
        dataObjectFilterList['category'] = []
        for item in category_list:
            dataObjectFilterList['category'].append({
                'value':item.id,
                'label':(item.category + " | " + item.sub_category).title()
                })

        dataObjectFilterList['status'] = [
                                        {'value':'to_be_updated','label':'To Be Updated'},
                                        {'value':'rejected','label':'Rejected'},
                                        {'value':'shortlisted','label':'Shortlisted'},
                                        {'value':'ready','label':'Ready'}
                                        ]


        # objects = dataObject.objects.filter(item__id = id)

        # to update filters - start
        category = request.GET.get('category', None)
        statusitem = request.GET.get('status', None)
        search = request.GET.get('search', None)
        sort_by = request.GET.get('sort_by', None)
        order = request.GET.get('order', None)
        is_all = request.GET.get('is_all', None)

        if category !=None and category !="" and category != "none":
            category_list = category.split(",")
            objects = objects.filter(item__category__in=category_list)

        if statusitem !=None and statusitem !="" and statusitem != "none":
            status_list = statusitem.split(",")
            objects = objects.filter(item__status__in=status_list)


        if search !=None and search !="" and search != "none":
            objects = objects.filter(Q(item__name__icontains=search))

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

    @api_view(['GET', 'PUT', 'DELETE'])
    def object_detail_v1(request, id):
        
        # to update - start
        dataObject = VendorItem
        dataObjectFriendlyName = "Vendor Item"
        dataObjectSerializer = VendorItemSerializer    
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
        