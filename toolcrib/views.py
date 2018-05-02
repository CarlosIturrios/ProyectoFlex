# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User

from .models import Part, Order, OrderDetail

# Create your views here.
@login_required()
def principal(request):
	return render(request, 'principal.html')


@login_required()
@permission_required('toolcrib.add_part')
def ordersmanager(request):	
	orders = Order.objects.all()
	orders = orders.filter(status='2')
	return render(request, 'ordersmanager.html', {'orders':orders})


@login_required()
def orderssupervisor(request):
	# Order.status (1=Pennding)
	orders = Order.objects.filter(status='1', supervisor=request.user)
	return render(request, 'orderssupervisor.html', {'orders':orders})


@login_required()
@permission_required('toolcrib.add_part')
def updateproduct(request):
	return render(request, 'updateproduct.html')


@login_required()
@permission_required('toolcrib.add_part')
def updateuser(request):
	return render(request, 'updateuser.html')


@login_required()
def parts(request):
	if request.method == "POST":
		id_part = request.POST.get('id_part', None)
		cant = request.POST.get('cant', 1)
		
		if 'cart' not in request.session:
			request.session['cart'] = [{'id_part': id_part, 'cant': 1}]
		else:
			cart = request.session['cart']
			cart.append({'id_part': id_part, 'cant': cant})
			request.session['cart'] = cart

		return redirect('toolcrib:parts')


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

	paginator = Paginator(parts_list, 9)
	parts = paginator.page(page)
		
	return render(request, 'parts.html', {'parts' : parts, 'category': category, 'q':q})	


@login_required()
def shopingcart(request):
	if request.method == "GET":
		supervisors = User.objects.filter(groups__name='Supervisor')
		cart_v = []		
		if 'cart' not in request.session:
			return redirect('toolcrib:parts')	
		for item in request.session['cart']:
			p = Part.objects.get(id=item['id_part'])
			cart_v.append(
				{'cant': item['cant'], 'part': p}
			)
		return render(request, 'shopingcart.html', {'cart':cart_v, 'supervisors':supervisors})	
	
	elif request.method == "POST":
		supervisor = request.POST.get('supervisor', None)
		level = request.POST.get('level', None)
		cost_center = request.POST.get('cost_center', None)

		o = Order()
		o.level = level
		o.cost_center = cost_center
		o.supervisor = User(id=supervisor)
		o.user = request.user
		o.save()

		for item in request.session['cart']:
			o.order_detail_set.create(
				part=Part(id=item['id_part']),
				quantity=item['cant']
			)

		del request.session['cart']

		return redirect('toolcrib:parts')


@login_required()
@permission_required('toolcrib.add_part')
def ordersmanagercart(request):
	return render(request, 'ordersmanagercart.html')


@login_required()
def orderssupervisorcart(request):
	return render(request, 'orderssupervisorcart.html')
