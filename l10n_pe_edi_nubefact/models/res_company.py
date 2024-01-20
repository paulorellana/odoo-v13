# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Company(models.Model):
	_inherit = "res.company"

	sunat_provider = fields.Selection(selection_add=[("nubefact","NUBEFACT")])