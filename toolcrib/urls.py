from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    
    # Auth Urls
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/toolcrib/login/'}, name='logout'),

    # App views    
   	url(r'^$', views.principal, name='principal'),
   	url(r'^ordersmanager/$', views.ordersmanager, name='ordersmanager'),
 	url(r'^orderssupervisor/$', views.orderssupervisor, name='orderssupervisor'),  
 	url(r'^updateproduct/$', views.updateproduct, name='updateproduct'),	
 	url(r'^updateuser/$', views.updateuser, name='updateuser'),
 	url(r'^parts/$', views.parts, name='parts'),
 	url(r'^shopingcart/$', views.shopingcart, name='shopingcart'),
 	url(r'^ordersmanagercart/$', views.ordersmanagercart, name='ordersmanagercart'),
 	url(r'^orderssupervisorcart/$', views.orderssupervisorcart, name='orderssupervisorcart'),
]