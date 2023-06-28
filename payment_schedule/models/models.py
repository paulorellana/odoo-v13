# -*- coding: utf-8 -*-

from odoo import models, fields, api
#En otro modulo el nombre de la class debe ser unico
# por ejemplo nombre_modulo1.class diferente al nombre_modulo2.class para el mismo modelo heredado x ejemplo product.template
 
class product3(models.Model):
	_inherit = 'product.template'
	payment_schedule_id= fields.One2many('payment.schedule','product_ps_id')
	partner_id = fields.Many2one('res.partner', string='Cliente')
	num_contrato = fields.Char(string="Num. de contrato")
	num_cuotas = fields.Integer(string="Num. de cuotas")
	num_cuotas_pagadas = fields.Float(string="Cuotas pagadas")
	num_cuotas_pendientes = fields.Float(string="Cuotas pendientes")

#Example related	
#id_order_p = fields.Many2one('mrp.production', string="Num.orden produccion:")
#product_id = fields.Many2one(related="id_order_p.product_id", string="Producto:")
#product_qty = fields.Float(related="id_order_p.product_qty",string="Cantidad producir:")
	
class paymentschedule(models.Model):
	_name = 'payment.schedule'
	product_ps_id = fields.Many2one('product.template', string="product ID")
	product_ps_id_show = fields.Char(related='product_ps_id.name', string='Lote')
	
	p_date = fields.Date(string='Fecha')
	p_amount = fields.Float(string='Monto Cuota/Inicial S/.')
	p_invoice = fields.Many2one('account.move','Factura/Boleta')
	p_obs = fields.Char(string='Nota')
	p_state = fields.Selection([('Pagado','PAGADA'),('Pendiente','PENDIENTE')],default='Pendiente',
			    				string="Estado de Cuota/Inicial")


class respartner2(models.Model):
	_inherit = 'res.partner'
	payment_schedule_id= fields.One2many('payment.schedule','product_ps_id')
	



	


									  
