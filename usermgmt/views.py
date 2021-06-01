from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from usermgmt.serializers import *
from overall.views import *
from django.views.decorators.csrf import csrf_exempt
from mailing.views import * 



defaultpassword = 'tdspassword'
# @csrf_exempt
class userMgmt:
    @api_view(['GET', 'POST', 'DELETE'])
    def object_list_v1(request):

        # to update - start
        dataObject = DecorShopUser
        dataObjectFriendlyName = "User"
        dataObjectFilterList = {}
        dataObjectSerializer = UserSerializer  
        natural_key = 'email'

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
            count = 0 
            try:
                count = dataObject.objects.filter(email = cleanstring(object_data[natural_key]).lower()).count()     
            except:
                count = -1

            object_serializer = dataObjectSerializer(data=object_data)
            
            if count == 0:
                if object_serializer.is_valid():
                    object_serializer.save()
                    success = True
                    message = dataObjectFriendlyName + " Created!"
                    data = object_serializer.data
                    user_detail = DecorShopUser.objects.get(id=data['id'])
                    user_detail.set_password(defaultpassword)
                    user_detail.username = data['email']
                    user_detail.save()

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
        dataObject = DecorShopUser
        dataObjectFriendlyName = "User"
        dataObjectSerializer = UserSerializer    
        natural_key = "email"
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
            past_email = dataObject.objects.get(id = id).email
            object_serializer = dataObjectSerializer(object, data=object_data) 

            if object_serializer.is_valid(): 
                if past_email == cleanstring(object_data['email']).lower():
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
                    data = object_serializer.data
                    message = dataObjectFriendlyName + " email can't be updated!"
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
            if not object.is_superuser:
                object.delete() 
                success = True
                message = dataObjectFriendlyName + ' was deleted successfully!'
                obj= {
                    'success':True,
                    'message': message
                    }
                return JsonResponse(obj)
            else:
                success = False
                message = dataObjectFriendlyName + ' cannot be deleted!'
                obj= {
                    'success':True,
                    'message': message
                    }

                return JsonResponse(obj)
        
            
# logging in with password

    @api_view(['POST'])
    # @csrf_exempt
    def login_view(request):
        obj = {}
        obj['success'] = False
        email           = request.POST.get("email", None) 
        password        = request.POST.get("password", None)  
        secret_string   = request.POST.get("sec_string", None) 
        auth_token      = request.POST.get("auth_token", None)
        # print(password)
        if email:
            email = email.lower()
            email = cleanstring(email)
        obj['data'] = {}
        obj['auth'] = False

        # obj['user'] = {}
        message = ""
        if auth_token:
            try:
                user = DecorShopUser.objects.get(auth_token=auth_token,is_active=True)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                message = "User Found"
                login(request, user)
                obj['data']['auth_token'] = auth_token
                obj['data']['id'] = user.id
                obj['data']['first_name'] = user.first_name
                obj['data']['last_name'] = user.last_name
                obj['data']['email'] = user.email
                obj['data']['is_staff'] = user.is_staff
                obj['auth'] = True
                message = "Login Success!"
                success = True
                print(1)
            except:
                obj['auth'] = False
                message = "Auth Token Expired"
                obj['data'] = None
                success = False

        elif password:
            try:
                user = DecorShopUser.objects.get(email=email,is_active=True)
                print(2)
                if user:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    message = "User Found"
                    # print(2)
                    if user.check_password(password):
                        # print(3)
                        login(request, user)
                        # print(4)
                        new_string = str(user.id) + random_str_generator()
                        # print(5)
                        user.auth_token = new_string
                        # print(6)
                        obj['data']['auth_token'] = new_string
                        obj['data']['id'] = user.id
                        obj['data']['first_name'] = user.first_name
                        obj['data']['last_name'] = user.last_name
                        obj['data']['email'] = user.email
                        obj['data']['is_staff'] = user.is_staff
                        obj['auth'] = True
                        print(3)
                        message = "Login Success!"
                        success = True
                        user.save()
                    else:
                        message = "Incorrect Password"
                        obj['auth'] = False
                        success = False

                else:
                    message = "User Doesn't exist"
                    obj['auth'] = False
                    obj['data'] = None
                    success = False
            except:
                if email:
                    message = "User Doesn't exist"
                obj['auth'] = False
                obj['data'] = None
                success = False
        elif secret_string:
            try:
                user = DecorShopUser.objects.get(email=email,is_active=True)
                print(2)
                if user:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    message = "User Found"
                    # print(2)
                    if user.secret_string == secret_string:
                        login(request, user)
                        new_string = str(user.id) + random_str_generator()
                        user.auth_token = new_string
                        obj['data']['auth_token'] = new_string
                        obj['data']['id'] = user.id
                        obj['data']['first_name'] = user.first_name
                        obj['data']['last_name'] = user.last_name
                        obj['data']['email'] = user.email
                        obj['data']['is_staff'] = user.is_staff
                        obj['auth'] = True
                        print(4)
                        message = "Login Success!"
                        success = True
                        user.save()
                    else:
                        message = "Incorrect Password"
                        obj['auth'] = False
                        success = False

                else:
                    message = "User Doesn't exist"
                    obj['auth'] = False
                    obj['data'] = None
                    success = False
            except:
                if email:
                    message = "User Doesn't exist"
                obj['auth'] = False
                obj['data'] = None
                success = False
        else:
            message = "Invalid Parameters"
            obj['auth'] = False
            obj['data'] = None
            success = False

        obj['success'] = success
        obj['message'] = message
        response = HttpResponse(json.dumps(obj), content_type='application/json')
        return response

    def send_password_reset(request):
        obj = {}
        obj['success'] = False
        email           = request.POST.get("email", None) 
        randstring = ""
        try:
            user = DecorShopUser.objects.get(email=email,is_active=True)
            if user:
                print('a')
                randstring = str(user.id) + random_str_generator()
                message = "Reset Request Success"
                user.secret_string = randstring
                user.save()
                print('b')
                send_password_reset_email(name=user.first_name, email=user.email, secret_string=randstring.encode('utf-8'))
                print('c')
            else:
                message = "User Doesn't exist"
        except:
            message = "User Doesn't exist"
            obj['data'] = None
        obj['success'] = True
        obj['message'] = message
        response = HttpResponse(json.dumps(obj), content_type='application/json')
        return response

    def reset_pass(request):
        obj = {}
        obj['success'] = False
        obj['data'] = {}
        obj['auth'] = False

        password        = request.POST.get("pass", None)    
        secret_string   = request.POST.get("sec_string", None) 
        try:
            user = DecorShopUser.objects.get(secret_string=secret_string,is_active=True)
            user.set_password(password)
            randstring = str(user.id) + random_str_generator()
            randstring2 = str(user.id) + random_str_generator()
            user.secret_string = randstring
            user.auth_token = randstring2
            user.save()

            obj['data']['auth_token'] = randstring2
            obj['data']['id'] = user.id
            obj['data']['first_name'] = user.first_name
            obj['data']['last_name'] = user.last_name
            obj['data']['email'] = user.email
            obj['data']['is_staff'] = user.is_staff
            obj['auth'] = True
            obj['message'] = "Password Reset Success"
        except:
            obj['message'] = "Invalid Request Please Try Resetting the Password Again"
        obj['status'] = True
        
        return HttpResponse(json.dumps(obj), content_type='application/json')
    # logging out

    def logout_view(request):
        obj = {}
        obj['success'] = False
        user_id   = request.POST.get("user_id", None) 
        
        user = DecorShopUser.objects.get(id=user_id)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.auth_token = str(user.id) + random_str_generator()
        user.save()
        logout(request)        

        obj['data'] = ""
        obj['success'] = True
        obj['message'] = "Logout Success"
        
        response = HttpResponse(json.dumps(obj), content_type='application/json')
        return response

