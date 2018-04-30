# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required

from .models import Part

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
def parts(request):
	if request.method == "POST":		
		if 'cart' not in request.session:
			request.session['cart'] = []
		id_part = request.POST.get('id_part', None)
		request.session['cart'].append({'id_part': id_part, 'cant': 0, })

	q = request.GET.get('q', None)
	page = request.GET.get('page', 1)
	category = request.GET.get('category', None)
		
	parts_list = Part.objects.all()
		
	if category != None and category != '0':
		parts_list = parts_list.filter(category=category)
	else:
		category = '0'

	if q != None and q != '':
		parts_list = parts_list.filter(description__contains=q.strip())
	else:
		q = ''

	paginator = Paginator(parts_list, 1)
	parts = paginator.page(page)
		
	return render(request, 'parts.html', {'parts' : parts, 'category': category, 'q':q})	


@login_required()
def shopingcart(request):
	return render(request, 'shopingcart.html')

@login_required()
def ordersmanagercart(request):
	return render(request, 'ordersmanagercart.html')


@login_required()
def orderssupervisorcart(request):
	return render(request, 'orderssupervisorcart.html')
