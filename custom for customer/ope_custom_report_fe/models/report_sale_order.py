# -*- coding: utf-8 -*-
from odoo import models, api


class ReporteCotizacion(models.AbstractModel):

    _name = 'report.l10n_pe_custom_report.custom_report_sale_order'

    @api.model
    def _get_report_values(self, docids, data=None):
        #model = self.env.context.get('active_model') 
        return {
          'doc_ids': docids,
          'doc_model': 'sale.order',
          'data': data,
          'docs': self.env['sale.order'].browse(docids)
        }