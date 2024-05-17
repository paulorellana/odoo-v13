import time
from odoo import fields,api,models,_
import logging
from odoo.exceptions import UserError, ValidationError


_logger = logging.getLogger(__name__)



class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    advance_payment_method = fields.Selection(selection=[('delivered','Emisión Regular'),
                                                         ('percentage','Adelanto de pago (Porcentaje)'),
                                                         ('fixed','Depósito (cantidad fija)')],string="Crear Comprobante")

    def _prepare_so_line(self, order, analytic_tag_ids, tax_ids, amount):
        res = super(SaleAdvancePaymentInv,self)._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
        _logger.info(res)
        return res

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)

        paymentterm_lines = []
        for pl in order.paymentterm_line:
            paymentterm_lines.append(self.env['paymentterm.line'].create(
                {'currency_id': pl.currency_id, 'date_due': pl.date_due, 'amount': pl.amount}).id)

        res.update({
            "invoice_type_code": order.tipo_documento,
            "descuento_global": order.descuento_global,
            "apply_global_discount": True if order.descuento_global > 0 else False,
            "apply_same_discount_on_all_lines": order.apply_same_discount_on_all_lines,
            "discount_on_all_lines": order.discount_on_all_lines,
            "paymentterm_line": [(6, 0, paymentterm_lines)],
            "journal_type":"sale"
        })

        warehouse_id = order.warehouse_id
        if warehouse_id:
            res["warehouse_id"] = warehouse_id.id
            journals = self.env["stock.warehouse"].browse(warehouse_id.id).journal_ids.filtered(
                lambda r: r.invoice_type_code_id == order.tipo_documento and r.type == "sale")
            if len(journals) > 0:
                res["journal_id"] = journals[0].id
            else:
                raise UserError(
                    "Debe configurar Diarios disponibles en sus almacénes. Contacte con su administrador.")
        else:
            raise UserError(
                "Su usuario no tiene almacenes disponibles. Contacte con su administrador.")

        return res