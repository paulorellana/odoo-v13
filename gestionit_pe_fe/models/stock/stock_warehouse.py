# -*- coding: utf-8 -*-
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError
from odoo import fields, models, api, _


class stockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    journal_ids = fields.Many2many('account.journal', string='Series permitidas')
    
    numero_anexo  =fields.Char("Número de anexo",default="0000",required=True,unique=True)
    street = fields.Char("Dirección",related="partner_id.street",readonly=False)
    ubigeo = fields.Char("Ubigeo",related="partner_id.ubigeo",readonly=False)