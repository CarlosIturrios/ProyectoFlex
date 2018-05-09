# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import path

from django.db import models
from django.contrib.auth.models import User



def unique_file_path(instance, filename):	
    base, ext = path.splitext(filename)
    newname = "%s%s" % (instance.num_part, ext)
    return path.join('parts_img', newname)


# Create your models here.
class Part(models.Model):
	num_part = models.CharField(max_length=70, unique=True, null=False, blank=False)
	description = models.CharField(max_length=100, db_index=True, null=False, blank=False)
	inventory_type = models.CharField(max_length=100, db_index=True)
	image = models.ImageField(upload_to=unique_file_path, null=True, blank=False)	
	category = models.CharField(
		max_length=1, blank=False, default='1', choices=(
			('1','SUPPLY'),
			('2','SPARE PARTS')
		)
	)
	clas = models.CharField(
		max_length = 1, blank=False, default='1', choices =(
			('1','MXN'),
			('2','USD')
		)
	)
	location = models.CharField(max_length=200, null=True, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
	quantity = models.PositiveIntegerField(null=False, blank=False)
	max_quantity = models.PositiveIntegerField(null=False, blank=False)
	min_quantity = models.PositiveIntegerField(null=False, blank=False)

	def __str__(self):
		return self.num_part


class Order(models.Model):	
	status = models.CharField(
		max_length = 1, blank=False, default='1', choices =(
			('1','Pennding'),
			('2','Approved'),
			('3','Canceled'),
			('4','Done'),
		)
	)
	level = models.CharField(
		max_length = 1, blank=False, default='1', choices =(
			('1','Low'),
			('2','Medium'),
			('3','High'),
		)
	)
	
	cost_center = models.CharField(max_length=100, null=False, blank=False)
	comments = models.CharField(max_length=200, null=True, blank=True)
	
	user = models.ForeignKey(
		User, null=False, blank=False, related_name='order_set', on_delete=models.PROTECT
	)
	supervisor = models.ForeignKey(
		User, null=False, blank=False, related_name='superviced_order_set', on_delete=models.PROTECT
	)
		
	date_order = models.DateTimeField(null=False, blank=False, auto_now_add=True)
	date_approved = models.DateTimeField(null=True, blank=True)
	date_done = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return 'Order N: {0} Status: {1}'.format(self.id, self.get_status_display())


class OrderDetail(models.Model):
	order = models.ForeignKey(Order, null=False, blank=False, related_name='order_detail_set', on_delete=models.CASCADE)
	part = models.ForeignKey(Part, null=False, blank=False, related_name='part_detail_set', on_delete=models.PROTECT)
	quantity = models.PositiveIntegerField(null=False, blank=False)
	
	def __str__(self):
		return 'Part N. {0} Cant: {1}'.format(self.part.num_part, self.quantity)