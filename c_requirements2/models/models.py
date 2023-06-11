# -*- coding: utf-8 -*-

from odoo import models, fields, api

class product2(models.Model):
	_inherit = 'product.template'
	estado = fields.Selection([('Disponible','DISPONIBLE'),('Vendido','VENDIDO'),('Separado','SEPARADO')],string="Estado")
	