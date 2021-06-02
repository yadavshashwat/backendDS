"""backendHospital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url 

from usermgmt.views import *
from vendormgmt.views import *
from itemmgmt.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    # version 1 apis

    url(r'^api/v1/users$', userMgmt.object_list_v1),
    url(r'^api/v1/users/(?P<id>[0-9]+)$', userMgmt.object_detail_v1),

    url(r'^api/v1/user/login$', userMgmt.login_view),
    url(r'^api/v1/user/logout$', userMgmt.logout_view),
    url(r'^api/v1/user/reset_request$', userMgmt.send_password_reset),
    url(r'^api/v1/user/reset$', userMgmt.reset_pass),




    url(r'^api/v1/vendors$', vendorMgmt.object_list_v1),
    url(r'^api/v1/vendors/(?P<id>[0-9]+)$', vendorMgmt.object_detail_v1),

    url(r'^api/v1/itemcats$', itemCatMgmt.object_list_v1),
    url(r'^api/v1/itemcats/(?P<id>[0-9]+)$', itemCatMgmt.object_detail_v1),

    url(r'^api/v1/items$', itemMgmt.object_list_v1),
    url(r'^api/v1/items/(?P<id>[0-9]+)$', itemMgmt.object_detail_v1),
    url(r'^api/v1/itemimageupload/(?P<id>[0-9]+)$', itemMgmt.upload_item_image),


]



 
