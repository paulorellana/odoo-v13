# -*- coding: utf-8 -*-

from odoo import models, fields, api

class product(models.Model):
#     _name = 'po_model_module.po_model_module'
	_inherit = 'product.template'
	n_porc_utilidad = fields.Float(string="% Utilidad:")
	marca = fields.Char(string="Marca:")
	descripcion = fields.Text(string="Descripcion:")

	@api.onchange('n_porc_utilidad')
	def _n_porc_utilidad(self):
#           self.standard_price = self.list_price/(1+self.n_porc_utilidad/100)
			self.list_price = self.standard_price*(1+self.n_porc_utilidad/100)

class partner(models.Model):
#     _name = 'po_model_module.po_model_module'
	_inherit = 'res.partner'
	abc = fields.Selection([(1,'A'),( 2,'B'),(3,'C')],string="Clasificación ABC:")

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
	