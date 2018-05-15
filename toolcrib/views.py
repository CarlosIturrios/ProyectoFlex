# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse #email sender
from django.template import Context #email sender
from django.template.loader import render_to_string, get_template #email sender
from django.core.mail import EmailMessage, EmailMultiAlternatives #email sender
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.conf import settings

from datetime import datetime
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
	orders = Order.objects.filter(status='2').order_by('level').reverse()
	return render(request, 'ordersmanager.html', {'orders':orders})


@login_required()
@permission_required('toolcrib.change_order')
def orderssupervisor(request):
	# Order.status (1=Pennding)
	orders = Order.objects.filter(status='1', supervisor=request.user).order_by('level').reverse()
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
			response = redirect('toolcrib:updateproduct')
			toast_text = 'Tool {0} update successful'.format(part.num_part) 
			response['Location'] += '?%s' % urllib.urlencode({'toast': toast_text})
			return response
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
			toast_text = 'User {0} update successful'.format(user.username) 
			response = redirect('toolcrib:ordersmanager')
			response['Location'] += '?%s' % urllib.urlencode({'toast': toast_text})
			return response
	else:
		form = UserForm()
	return render(request, 'updateuser.html',{'form':form})


@login_required()
def parts(request):
	if request.method == "POST":
		id_part = request.POST.get('id_part', None)
		cant = request.POST.get('cant', None)
		
		if 'cart' not in request.session:
			request.session['cart'] = [{'id_part': id_part, 'cant': cant}]
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
		parts_list = parts_list.filter(description__icontains=q.strip()) | parts_list.filter(num_part__icontains=q.strip())
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

		o = Order()f
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
		supervisor_email = User.objects.get(id=supervisor)
		print(supervisor_email)
		subject = 'ToolCrib: New order #{0} created by {1}'.format(o.id, o.user.get_full_name())
		html_content = get_template('emails/order_created.html').render({'order': o})

		msg = EmailMessage(
			subject=subject,
			body=html_content,
			from_email=settings.DEFAULT_FROM_EMAIL,
			to=[supervisor_email.email],
			cc=[o.user.email,],
		)
		msg.content_subtype = "html"
		msg.send(fail_silently= not settings.DEBUG)

		toast_text = 'Order {0} done successful'.format(o.id) 
		response = redirect('toolcrib:parts')
		response['Location'] += '?%s' % urllib.urlencode({'toast': toast_text})
		return response


@login_required()
@permission_required('toolcrib.add_part')
def ordersmanagercart(request, pk):
	# Order.status (4=Done)
	order = get_object_or_404(Order, pk=pk)
	if request.method == "POST":
		comments = request.POST.get('comments', None)
		order.status = '4'
		order.comments = comments
		order.date_done = datetime.now()
		order.save()
		toast_text = 'Order {0} Done successful'.format(order.id) 
		response = redirect('toolcrib:ordersmanager')
		response['Location'] += '?%s' % urllib.urlencode({'toast': toast_text})

		subject = 'ToolCrib: order #{0} Done lets go to toolcrib'.format(order.id)
		html_content = get_template('emails/OrderDone.html').render({'order': order})

		msg = EmailMessage(
			subject=subject,
			body=html_content,
			from_email=settings.DEFAULT_FROM_EMAIL,
			to=[order.user.email,],
			cc=[order.supervisor.email,],
		)
		msg.content_subtype = "html"
		msg.send(fail_silently= not settings.DEBUG)

		return response

	return render(request, 'ordersmanagercart.html', {'order': order})


@login_required()
@permission_required('toolcrib.change_order')
def orderssupervisorcart(request, pk):	
	order = get_object_or_404(Order, pk=pk)
	if request.method == "POST":
		level = request.POST.get('level', None)
		comments = request.POST.get('comments', None)
		order.level = level
		order.status = '2'
		order.comments = comments
		order.date_approved = datetime.now()
		order.save()
		toast_text = 'Order {0} approved successful'.format(order.id) 
		response = redirect('toolcrib:orderssupervisor')
		response['Location'] += '?%s' % urllib.urlencode({'toast': toast_text})
		
		subject = 'ToolCrib: order #{0} approved by {1}'.format(order.id, order.supervisor)
		html_content = get_template('emails/OrderApproved.html').render({'order': order})

		msg = EmailMessage(
			subject=subject,
			body=html_content,
			from_email=settings.DEFAULT_FROM_EMAIL,
			to=['tool.crib.flex@gmail.com',],
			cc=[order.user.email, order.supervisor.email,],
		)
		msg.content_subtype = "html"
		msg.send(fail_silently= not settings.DEBUG)

		return response

	return render(request, 'orderssupervisorcart.html', {'order': order})


@login_required()
@permission_required('toolcrib.change_order')
def orderCanceled(request, pk):
	# Order.status (3=Cancel)
	order = get_object_or_404(Order, pk=pk)
	if request.method == "POST":
		order.status = '3'
		order.date_approved = datetime.now()
		order.save()
		
		subject = 'ToolCrib: Order #{0} was Canceled'.format(order.id)
		html_content = get_template('emails/OrderCancel.html').render({'order': order})

		msg = EmailMessage(
			subject=subject,
			body=html_content,
			from_email=settings.DEFAULT_FROM_EMAIL,
			to=[order.user.email,],
			cc=[order.supervisor.email,],
		)
		msg.content_subtype = "html"
		msg.send(fail_silently= not settings.DEBUG)

		return redirect('toolcrib:orderssupervisor')
	return render(request, 'orderCanceled.html', {'order':order})


@login_required()
def deleteCart(request):
	if request.method == "POST":
		del request.session['cart']
		return redirect('toolcrib:parts')
	return render(request, 'deleteCart.html')


@login_required()
def showorders(request):
	orders = Order.objects.all().order_by('status')
	return render(request,'showorders.html',{'orders':orders})