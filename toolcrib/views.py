# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
def principal(request):
	return render(request, 'principal.html')

@permission_required('Part.can_add')
def ordersmanager(request):	
	return render(request, 'ordersmanager.html')

def orderssupervisor(request):
	return render(request, 'orderssupervisor.html')

def updateproduct(request):
	return render(request, 'updateproduct.html')

def updateuser(request):
	return render(request, 'updateuser.html')

def products(request):
	return render(request, 'products.html')