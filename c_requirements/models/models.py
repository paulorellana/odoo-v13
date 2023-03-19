# -*- coding: utf-8 -*-

from odoo import models, fields, api

class product(models.Model):
	_inherit = 'product.template'
	n_porc_utilidad = fields.Float(string="%margen:")
	marca = fields.Char(string="Marca")
	descripcion = fields.Text(string="")
	cod_interno = fields.Text(string="Código interno")

	@api.onchange('n_porc_utilidad')
	def _n_porc_utilidad(self):
			self.list_price = self.standard_price*(1+self.n_porc_utilidad/100)

class partner(models.Model):
	_inherit = 'res.partner'
	abc = fields.Selection([('a','A'),('b','B'),('c','C')],string="Clasificación ABC:")

class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'
    marca = fields.Char(related='product_id.marca', readonly=True)

class Crmlead(models.Model):

    _inherit = 'crm.lead'
    begin_date = fields.Date(string="Fecha de incio:")
    finish_date = fields.Date(string="Fecha de finalización:")



#class company(models.Model):
#	_inherit = 'res.company'
#	logo2 = fields.Binary(string="Logo alternativo:")
#	tradename = fields.Char(string="Nombre Comercial:") 

#class product_uom(models.Model):
#	_inherit = 'product.uom'
#	code2 = fields.Char(string="Nombre corto reportes:")

#class mrp_production(models.Model):
#	_inherit = 'mrp.production'
#	_sale_order_id = fields.Many2one("sale.order")
	