from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    
    # Auth Urls
    url(r'login/$', auth_views.login, name='login'),
    url(r'logout/$', auth_views.logout, {'next_page': '/toolcrib/login/'}, name='logout'),

    # App views    
   	url(r'ordersmanager/$', views.ordersmanager, name='ordersmanager'),
 	url(r'orderssupervisor/$', views.orderssupervisor, name='orderssupervisor'),  
 	url(r'updateproduct/$', views.updateproduct, name='updateproduct'),	
 	url(r'updateuser/$', views.updateuser, name='updateuser'),
 	url(r'products/$', views.products, name='products'),
 	url(r'$', views.principal, name='principal'),

]