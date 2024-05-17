# -*- coding: utf-8 -*-
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError
from odoo import fields, models, api, _
from datetime import datetime, timedelta
from pytz import timezone

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    numero_guia = fields.Char("Número de Guía")
    tiene_guia_remision = fields.Boolean(
        "Tienes guía de Remisión", default=False)

    @api.onchange("tiene_guia_remision")
    def _set_default_tiene_guia_remision(self):
        for record in self:
            if not record.tiene_guia_remision:
                record.numero_guia = False

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search(['|', ('name', operator, name),
                                ('numero_guia', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super(StockPicking, self).name_search(name, args=args, operator=operator, limit=limit)

    def name_get(self):
        return [(rec.id, rec.name + (' - [' + rec.numero_guia+']')if rec.numero_guia else rec.name) for rec in self]

    def action_context_default_guia_remision(self):
        return {
            "default_documento_asociado": "movimiento_stock",
            "default_fecha_emision": datetime.now(tz=timezone("America/Lima")).date(),
            "default_fecha_inicio_traslado": datetime.now(tz=timezone("America/Lima")).date(),
            # "default_modalidad_transporte":"02",
            "default_motivo_traslado": "01",
            "default_movimiento_stock_ids": [(6, 0, [self.id])],
            "default_destinatario_partner_id": self.partner_id.id,
            "default_company_partner_id": self.partner_id.id,
            "default_company_id": self.company_id.id
        }

    def action_open_guia_remision(self):
        action = {
            "type": "ir.actions.act_window",
            "res_model": "gestionit.guia_remision",
            "context": self.action_context_default_guia_remision(),
            "target": "self",
            "view_mode": "form"
        }
        return action