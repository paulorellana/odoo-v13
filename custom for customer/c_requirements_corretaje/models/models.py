# -*- coding: utf-8 -*-

from odoo import models, fields, api
#En otro modulo el nombre de la class debe ser unico
# por ejemplo nombre_modulo1.class diferente al nombre_modulo2.class para el mismo modelo heredado x ejemplo product.template
 
class product2(models.Model):
	_inherit = 'product.template'
	estado = fields.Selection([('Disponible','DISPONIBLE'),('Vendido','VENDIDO'),('Separado','SEPARADO')],string="Estado")
class partner2(models.Model):
	_inherit = 'res.partner'
	estado_civil = fields.Selection([('Soltero','SOLTERO'),('Casado','CASADO'),('Viudo','VIUDO'),('Divorciado','DIVORCIADO'),
				  					 ('Soltera','SOLTERA'),('Casada','CASADA'),('Viuda','VIUDA'),('Divorciada','DIVORCIADA')
				                      ],string="Estado Civil")



									  
