# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group

from .models import Part, Order, OrderDetail
from .forms import PartForm, UserForm

# Create your views here.
@login_required()
def principal(request):
	return render(request, 'principal.html')


@login_required()
@permission_required('toolcrib.add_part')
def ordersmanager(request):	
	# Order.status (2=approved)
	orders = Order.objects.filter(status='2')
	return render(request, 'ordersmanager.html', {'orders':orders})


@login_required()
def orderssupervisor(request):
	# Order.status (1=Pennding)
	orders = Order.objects.filter(status='1', supervisor=request.user)
	return render(request, 'orderssupervisor.html', {'orders':orders})


@login_required()
@permission_required('toolcrib.add_part')
def updateproduct(request):
	if request.method == 'POST':
		part = get_object_or_404(Part, num_part=request.POST.get('num_part'))
		form = PartForm(request.POST, request.FILES)
		if form.is_valid():
			part.category = form.cleaned_data['category']
			part.image = form.cleaned_data['image']
			part.save()
			return redirect('toolcrib:parts', )
	else:
		form = PartForm()
	return render(request, 'updateproduct.html', {'form': form})


@login_required()
@permission_required('toolcrib.add_part')
def updateuser(request):
	if request.method == 'POST':
		user = get_object_or_404(User, username=request.POST.get('username'))
		form = UserForm(request.POST)
		if form.is_valid():			
			group = Group.objects.get(name=form.cleaned_data['group'])
			user.email = form.cleaned_data['email']
			user.set_password(form.cleaned_data['password'])
			user.groups.clear()#Remove user from previous grups
			user.groups.add(group)#Add user to form group
			user.save()

			response = redirect('toolcrib:principal')
			response['Location'] += '?%s' % urllib.urlencode({'toast': 'User update successful'})
			return response
	else:
		form = UserForm()
	return render(request, 'updateuser.html',{'form':form})


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
		
	parts_list = Part.objects.filter(quantity__gt = 0)
		
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
			request.session['cart'] = []
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

		return redirect('toolcrib:shopingcart_complete')


@login_required()
@permission_required('toolcrib.add_part')
def ordersmanagercart(request, pk):
	order = get_object_or_404(Order, pk=pk)
	if request.method == "POST":
		comments = request.POST.get('comments', None)
		order.status = '4'
		order.comments = comments
		order.save()
		return redirect('toolcrib:ordersmanager')
	return render(request, 'ordersmanagercart.html', {'order': order})


@login_required()
def orderssupervisorcart(request, pk):	
	order = get_object_or_404(Order, pk=pk)
	if request.method == "POST":
		level = request.POST.get('level', None)
		comments = request.POST.get('comments', None)
		order.level = level
		order.status = '2'
		order.comments = comments
		order.save()
		return redirect('toolcrib:orderssupervisor')

	return render(request, 'orderssupervisorcart.html', {'order': order})



@login_required()
def orderCanceled(request, pk):
	order = get_object_or_404(Order, pk=pk)
	if request.method == "POST":
		order.status = '3'
		order.save()
		return redirect('toolcrib:orderssupervisor')
	return render(request, 'orderCanceled.html', {'order':order})


@login_required()
def shopingcart_complete(request):
	return render(request, 'shopingcart_complete.html')


@login_required()
def deleteCart(request):
	if request.method == "POST":
		del request.session['cart']
		return redirect('toolcrib:parts')
	return render(request, 'deleteCart.html')