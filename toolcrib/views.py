# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required()
def principal(request):
	return render(request, 'principal.html')


@login_required()
@permission_required('toolcrib.add_part')
def ordersmanager(request):	
	return render(request, 'ordersmanager.html')


@login_required()
def orderssupervisor(request):
	return render(request, 'orderssupervisor.html')


@login_required()
def updateproduct(request):
	return render(request, 'updateproduct.html')


@login_required()
def updateuser(request):
	return render(request, 'updateuser.html')


@login_required()
def products(request):
	return render(request, 'products.html')