# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.addons.l10n_pe_edi_nubefact.models.oauth import send_doc_xml
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_send_invoice(self):
        # _logger.info("-->> action_send_invoice")
        if not (self.current_log_status_id and (self.journal_id.invoice_type_code_id == "01" or self.journal_id.tipo_comprobante_a_rectificar == "01")):
            self.action_generate_and_signed_xml()

        if self.current_log_status_id.status in ["P","R", "N",False]:
            try:
                vals = send_doc_xml(self)
                self.current_log_status_id.write(vals)
            except Exception as e:
                return vals

