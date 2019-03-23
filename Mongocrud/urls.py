
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import home,djex,login, logout,logo
from register.views import addPage,saveRecord,viewRecord,updateRecord,deleteRecord
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url('^admin/', admin.site.urls),
    url('dashboard',home,name='home'),
    url(r'^add/',addPage,name='signup'),
    url(r'save/',saveRecord,name='save'),
    url(r'^read/',viewRecord,name='read'),
    url(r'^update/(\d+)/',updateRecord,name='updatepg'),
    url(r'^update/',updateRecord,name='update'),
    url(r'^delete/(?P<id>\d+)',deleteRecord,name='delete'),
    #url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url('logout',logout,name='logout'),
    url('logo',logo,name='logo'),
    url('djongo/',djex),
    path(r'',login,name='login')
   
]
urlpatterns += staticfiles_urlpatterns()


