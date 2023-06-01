# -*- coding: utf-8 -*-

from odoo import models, fields, api

##     _name = 'po_model_module.po_model_module'
#	_inherit = 'product.template'
#	n_porc_utilidad = fields.Float(string="% Utilidad:")
	

#	@api.onchange('n_porc_utilidad')
#	def _n_porc_utilidad(self):
##          self.standard_price = self.list_price/(1+self.n_porc_utilidad/100)
#			self.list_price = self.standard_price*(1+self.n_porc_utilidad/100)

	
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
