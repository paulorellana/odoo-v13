from odoo import api, fields, models
import logging
import base64

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    invoice_report_id = fields.Many2one(
        comodel_name='ir.actions.report',
        string='Selecciona Formato de Factura',
        domain='[("model", "=", "account.move")]',
        default=lambda self: self.env.ref('account.account_invoices')
    )
    automatic_print_electronic_invoice = fields.Boolean(
        string='Impresión automática formato de factura'
    )

    @api.onchange('iface_print_auto')
    def onchange_iface_print_auto(self):
        if self.iface_print_auto:
            self.automatic_print_electronic_invoice = False


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def generate_dynamic_report_pos_ui(self, pos_reference, ir_report_id):
        values = {
            'error': False,
            'report': False
        }
        order_id = self.search([
            ('pos_reference', '=', pos_reference)
        ], limit=1)
        try:
            ids_to_print = order_id.account_move.id
            report_id = self.env['ir.actions.report'].browse(ir_report_id)
            if not ids_to_print or not report_id:
                values['error'] = True
            else:
                report = report_id.render_qweb_pdf([ids_to_print])
                values['report'] = base64.b64encode(report[0])
        except Exception as error:
            values['error'] = True
        return values
