# -*- coding: utf-8 -*-

from odoo import models, fields, api

class mrp_ap(models.Model):
	_name  = "avance.produccion"
	peso = fields.Float(string="Peso:")
	id_order_p = fields.Many2one('mrp.production', string="Num.orden produccion:")
	partner_id = fields.Many2one(related="id_order_p._sale_order_id.partner_id",string="Cliente:")
	product_id = fields.Many2one(related="id_order_p.product_id", string="Producto:")
	product_qty = fields.Float(related="id_order_p.product_qty",string="Cantidad producir:")
	name = fields.Char(string="Avance de produccion")


class mrp_production(models.Model):
	# orden de venta asociada a la orden de produccion
	_inherit = "mrp.production"
	_sale_order_id = fields.Many2one("sale.order", string="Seleccionar Pedido")
	maquina_nro = fields.Char("Maquina #")
	tiempo_prd = fields.Char("Tiempo produccion")
	refile = fields.Char("Refile")
	merma = fields.Char("Merma")
	total = fields.Char("Total")
	
class product(models.Model):
#     _name = 'po_model_module.po_model_module'
	_inherit = "product.template"
	structure = fields.Char(string="Estructura:")
	meters = fields.Char(string="Metraje:")
	#Datos del producto terminado
	ancho_final_manga = fields.Char(string="Ancho Final Manga mm")
	gramaje = fields.Char(string="Gramaje (g/m2)")
	peso_bobina = fields.Char(string="Peso de Bobina(kg.)")
	#Area de produccion extrusion
	gramaje_lineal = fields.Char (string="Gramaje lineal(g/m)")
	ancho_manga = fields.Char(string="Ancho de Manga (mm)")
	num_bandas=fields.Char(string="Número de Bandas:")
	bobinas_por_bajada = fields.Char(string="Bobinas por bajada:")
	#Formulacion global
	fuelle_lateral=fields.Char(string="Fuelle Lateral")
	perforaciones = fields.Char(string="Perforaciones")
	espesor = fields.Char(string="Espesor")
	tratamiento_corona = fields.Char(string="Tratamiento Corona")
	radio_cabezal=fields.Char(string="R de Cabezal")
	d_int_tuco = fields.Char(string="Diam.int.tuco")
	microperforada=fields.Char(string="Microperforada")
	sticker=fields.Char(string="Sticker")
	destino = fields.Char(string="Destino")








#https://youtu.be/v-Tcp_kun7s

#class product(models.Model):
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
