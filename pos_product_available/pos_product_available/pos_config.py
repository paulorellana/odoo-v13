# -*- coding: utf-8 -*-

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Picking location',
        related='picking_type_id.default_location_src_id'
    )
