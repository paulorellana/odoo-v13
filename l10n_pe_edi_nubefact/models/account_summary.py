# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.addons.l10n_pe_edi_nubefact.models.oauth import send_summary_xml
import logging
_logger = logging.getLogger(__name__)

class AccountSummary(models.Model):
    _inherit = "account.summary"

    def action_send_summary(self):
        _logger.info("-->> action_send_summary")
        if not self.current_log_status_id:
            self.action_generate_and_signed_xml()
        result = {}
        try:
            result = send_summary_xml(self)
            self.current_log_status_id.write(result)
        except Exception as e:
            return result