from odoo import models, fields, api, _
import urllib.parse as parse
from odoo.exceptions import UserError
from itertools import groupby

class InventoryTransferDone(models.Model):
    _inherit = 'stock.picking'

    def inventory_whatsapp(self):
        record_phone = self.partner_id.mobile
        if not record_phone:
            view = self.env.ref('odoo_whatsapp_integration.warn_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "Please add a mobile number!"
            return {
                'name': 'Mobile Number Field Empty',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        if not record_phone[0] == "+":
            view = self.env.ref('odoo_whatsapp_integration.warn_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "No Country Code! Please add a valid mobile number along with country code!"
            return {
                'name': 'Invalid Mobile Number',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        else:
            return {'type': 'ir.actions.act_window',
                    'name': _('Whatsapp Message'),
                    'res_model': 'whatsapp.wizard',
                    'target': 'new',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'context': {
                        'default_template_id': self.env.ref('odoo_whatsapp_integration.whatsapp_inventory_template').id},
                    }

    def send_direct_message(self):
        record_phone = self.partner_id.mobile
        if not record_phone:
            view = self.env.ref('odoo_whatsapp_integration.warn_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "Please add a mobile number!"
            return {
                'name': 'Mobile Number Field Empty',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        if not record_phone[0] == "+":
            view = self.env.ref('odoo_whatsapp_integration.warn_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "No Country Code! Please add a valid mobile number along with country code!"
            return {
                'name': 'Invalid Mobile Number',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        else:
            prods = ""
            for rec in self:
                for id in rec.move_line_ids_without_package:
                    prods = prods + "*" +str(id.product_id.name) + " : " + str(id.qty_done) + "* \n"

            custom_msg = "Hello *{}*, your order *{}* is ready.\nOrder contains following items: \n{}".format(
                str(self.partner_id.name), str(self.name), prods)
            ph_no = [number for number in record_phone if number.isnumeric()]
            ph_no = "".join(ph_no)
            ph_no = "+" + ph_no

            link = "https://api.whatsapp.com/send?phone=" + ph_no
            message_string = parse.quote(custom_msg)

            url_id = link + "&text=" + message_string
            return {
                'type': 'ir.actions.act_url',
                'url': url_id,
                'target': 'new',
                'res_id': self.id,
            }

    def check_value(self, partner_ids):
        partners = groupby(partner_ids)
        return next(partners, True) and not next(partners, False)

    def multi_sms(self):
        inventory_order_ids = self.env['stock.picking'].browse(self.env.context.get('active_ids'))

        cust_ids = []
        inventory_nums = []
        for inventory in inventory_order_ids:
            cust_ids.append(inventory.partner_id.id)
            inventory_nums.append(inventory.name)

        # To check unique customers
        cust_check = self.check_value(cust_ids)

        if cust_check:
            inventory_numbers = inventory_order_ids.mapped('name')
            inventory_numbers = "\n".join(inventory_numbers)

            form_id = self.env.ref('odoo_whatsapp_integration.whatsapp_multiple_message_wizard_form').id
            product_all = []
            for each in inventory_order_ids:
                prods = ""
                for id in each.move_ids_without_package:
                    prods = prods + "*" +  "Product: " + str(id.product_id.name) + "* \n"
                product_all.append(prods)

            custom_msg = "Hi" + " " + self.partner_id.name + ',' + '\n' + "Your Orders" + '\n' + inventory_numbers + \
                         ' ' + '\n' + "are ready for review.\n"
            counter = 0
            for every in product_all:
                custom_msg = custom_msg + "Your order " + "*" + inventory_nums[
                    counter] + "*" + " contains following items: \n{}".format(every) + '\n'
                counter += 1

            final_msg = custom_msg + "\nDo not hesitate to contact us if you have any questions."

            ctx = dict(self.env.context)
            ctx.update({
                'default_message': final_msg,
                'default_partner_id': self.partner_id.id,
                'default_mobile': self.partner_id.mobile,
            })
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'whatsapp.wizard.multiple.contact',
                'views': [(form_id, 'form')],
                'view_id': form_id,
                'target': 'new',
                'context': ctx,
            }
        else:
            raise UserError(_('Please Select Orders of Unique Customers'))