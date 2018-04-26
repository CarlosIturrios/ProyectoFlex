# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Part(models.Model):
	num_part = models.CharField(max_length=70, unique=True, null=False, blank=False)
	description = models.CharField(max_length=100, db_index=True, null=False, blank=False)
	inventory_type = models.CharField(max_length=100, db_index=True)
	image = models.ImageField(upload_to='toolcrib/static/media', null=True, blank=False)	
	category = models.CharField(
		max_length=1, blank=False, default='1', choices=(
			('1','SUPPLY'),
			('2','EXPERT PARTS')
		)
	)
	clas = models.CharField(
		max_length = 1, blank=False, default='1', choices =(
			('1','MXN'),
			('2','USD')
		)
	)
	location = models.CharField(max_length=200, null=True, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=4, null=False, blank=False)
	quantity = models.PositiveIntegerField(null=False, blank=False)
	max_quantity = models.PositiveIntegerField(null=False, blank=False)
	min_quantity = models.PositiveIntegerField(null=False, blank=False)

	def __str__(self):
		return self.num_part


class Order(models.Model):
	date_order = models.DateTimeField(null=True, blank=True)
	status = models.CharField(
		max_length = 1, blank=False, default='1', choices =(
			('1','PENDIENTE'),
			('2','APROBADO'),
			('3','CANCELADO'),
			('4','REALIZADO')
		)
	)
	level = models.CharField(
		max_length = 1, blank=False, default='1', choices =(
			('1','NORMAL'),
			('2','NO ES URGENTE'),
			('3','URGENTE')
		)
	)
	cost_center = models.CharField(max_length=100, null=False, blank=False)
	comments = models.CharField(max_length=200, null=True, blank=True)
	user = models.ForeignKey(User, unique=False)
	supervisor = models.ForeignKey(User, unique=False)
	date_done = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.status


class Order_Details(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	num_part = models.ForeignKey(Part, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(null=False, blank=False)
	
	def __str__(self):
		return self.order