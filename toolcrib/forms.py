# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User

from .models import Part


class PartForm(forms.Form):
	num_part = forms.CharField(max_length=70, required=True, strip=True)
	
	category = forms.ChoiceField(
		required=True, choices=(
			('1','SUPPLY'),
			('2','SPARE PARTS')
		)
	)

	image = forms.ImageField(required=True)


class UserForm(forms.Form):
	username = forms.CharField(max_length=191, required=True, strip=True)
	email = forms.CharField(max_length=191, required=True, strip=True)
	password = forms.CharField(max_length=191, required=True, strip=True)
	group = forms.ChoiceField(
		required=True, choices=(
			('Manager','Manager'),
			('Supervisor','Supervisor'),
			('Technical','Technical'),
			('Production','Production')
		)
	)