# -*- coding: utf-8 -*-
from odoo import models, api


class ReporteFactura(models.AbstractModel):

    _name = 'report.l10n_pe_custom_report.custom_invoice'


    @api.model
    def _get_report_values(self, docids, data=None):
        #model = self.env.context.get('active_model')
        #docs = self.env['account.invoice'].browse(self.env.context.get('active_id'))
        return {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'data': data,
            'docs': self.env['account.invoice'].browse(docids)
        }
