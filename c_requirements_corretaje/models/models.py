# -*- coding: utf-8 -*-

from odoo import models, fields, api

class partner(models.Model):
	_inherit = 'res.partner'
	num_contrato = fields.Char(string="Numero de contrato")
	estado_civil = fields.Char(string="Estado Civil")
	profesion = fields.Char(string="Profesión")

