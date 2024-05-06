# coding: utf-8
from io import BytesIO
from odoo import models
import qrcode
import base64


class AccountInvoiceQRCode(models.Model):
    _inherit = 'account.move'

    def generate_qr_code(self):
        self.ensure_one()
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=3,
            border=1
        )
        data_qr = self.create_data_qr_code()
        qr.add_data(data_qr.encode('utf8'))

        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue())
        return img_str.decode("utf8")

    def create_data_qr_code(self):
        template = '{ruc}|{document_type_name}|{series}|{correlative}|{total_igv}|{total_amount}|' \
                   '{date_invoice}|{document_type_name_user}|{document_number_user}|\r\n'

        date_invoice = self.invoice_date.strftime('%d-%m-%Y') if self.invoice_date else ''
        data = template.format(
            ruc=self.company_id.vat or '',
            document_type_name='',
            series='',
            correlative='',
            total_igv=self.amount_tax or 0.0,
            total_amount=self.amount_total or 0.0,
            date_invoice=date_invoice,
            document_type_name_user='',
            document_number_user=self.partner_id.vat or '',
        )
        return data
