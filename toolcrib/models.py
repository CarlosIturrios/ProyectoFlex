# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class users(models.Model):
	"""
	Model representa a un usuario dentro del sistema.
	"""
	numEmpleado = models.CharField(max_lenght = 70) #llave primaria
	nombreEmpleado = models.CharField(max_lenght = 250)
	psw = models.CharField(max_lenght = 30)
	correo = models.CharField(max_lenght = 250) #campo unico
	LOAN_USERTYPE = (
		('1','ADMINISTRADOR')
		('2','SUPERVISOR')
		('3','TECNICO')
		('4','PRODUCCION')
	)
	userType = models.CharField(max_lenght = 1, choices = LOAN_USERTYPE, blank = true, default = '1', help_text = 'Tipo o division de usuarios')

class partes(models.Model):
	"""
	Model representa a un producto o herramienta
	"""
	numParte = models.CharField(max_lenght = 70) #llave primaria
	description = models.TextField()
	imagen = models.TextField()
	invType = models.CharField(max_lenght = 100)
	LOAN_CATEGORIA = (
		('1','SUPPLY')
		('2','EXPERT PARTS')
	)
	categoria = models.CharField(max_lenght = 1, choices = LOAN_CATEGORIA, blank = true, default = '1', help_text = 'Tipo o division de categorias')

	LOAN_CLASS = (
		('1','MXN')
		('2','USD')
	)
	clase = models.CharField(max_lenght = 1, choices = LOAN_CLASS, blank = true, default = '1', help_text = 'Tipo de moneda')
	model = models.CharField(max_lenght = 100)
	price = models.FloatField()
	quantity = models.PositiveIntegerField()
	maxquantity = models.PositiveIntegerField()
	minquantity = models.PositiveIntegerField()
	location = models.CharField(max_lenght = 200)

class pedidos(models.Model):
	"""
	Model representa a un pedido
	"""
	folio = models.PositiveIntegerField() #llave primaria AutoIncrementable
	fechaSolicitado = models.DateTimeField()
	LOAN_URGENCIA = (
		('1','Normal')
		('2','Sin Urgencia')
		('3','URGENTE')
	)
	urgencia = models.CharField(max_lenght = 1, choices = LOAN_URGENCIA, blank = true, default = '1', help_text = 'Nivel de urgencia del pedido')
	LOAN_STATUS = (
		('1','Pendiente')
		('2','Aprovado')
		('3','Cancelado')
		('4','Finalizado')
	)
	status = models.CharField(max_lenght = 1, choices = LOAN_USERTYPE, blank = true, default = '1', help_text = 'estatus del proceso del pedido')
	fechaRealizado = models.DateTimeField()
	comentarios = models.TextField()
	costCenter = models.CharField(max_lenght = 100)
	numEmpleado = models.ForeignKey('users', null = false)

class detallesPedidos(models.Model):
	"""
	Model Representa todos los datos necesarios para mostrar los pedidos y sus atributos
	"""
	folio = models.ForeignKey('pedidos', null = false)	
	numParte = models.ForeignKey('users', null = false)
	quantity = models.PositiveIntegerField()
	