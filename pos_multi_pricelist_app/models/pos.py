# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from functools import partial

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)

class currency(models.Model):
	_inherit = 'res.currency'

	company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
	converted_currency = fields.Float('Currency', compute="_onchange_currency")

	@api.depends('company_id')
	def _onchange_currency(self):
		res_currency = self.env['res.currency'].search([])
		company_currency = self.env.user.company_id.currency_id
		for i in self:
			if i.id == company_currency.id:
				i.converted_currency = 1
			else:
				rate = (round(i.rate,6) / company_currency.rate)
				i.converted_currency = rate


class ProductPricelist(models.Model):

	_inherit = 'product.pricelist'
	converted_currency = fields.Float('Currency',related='currency_id.converted_currency')



class PosPayment(models.Model):

	_inherit = "pos.payment"

	amount_currency = fields.Float(string="Currency Amount")
	currency = fields.Many2one("res.currency", string="Currency")

class PosPaymentMethod(models.Model):

	_inherit = "pos.payment.method"

	currency_id = fields.Many2one("res.currency", 'Currency',compute='_compute_currency')

	def _compute_currency(self):
		for pm in self:
			pm.currency_id = pm.company_id.currency_id.id
			if pm.cash_journal_id and pm.cash_journal_id.currency_id:
				pm.currency_id = pm.cash_journal_id.currency_id.id

class POSOrderLine(models.Model):
	_inherit = "pos.order.line"

	price_unit_currency = fields.Float(string="Precio Unitario (FC)",digits=0)
	price_subtotal_currency = fields.Float(string="Subtotal sin Impuestos (FC)",digits=0)
	price_subtotal_incl_currency = fields.Float(string="Subtotal(FC)",digits=0)
	foreign_currency = fields.Many2one("res.currency",string="Foreign Currency")


class POSOrder(models.Model):
	_inherit = "pos.order"

	foreign_currency = fields.Many2one("res.currency",string="Foreign Currency")
	amount_total_currency = fields.Float(string='Total (FC)', digits=0, required=True)

	amount_total = fields.Float(string='Total', digits=0, required=True)
	amount_paid = fields.Float(string='Paid', digits=0, required=True)


	def _is_pos_order_paid(self):
		if (abs(self.amount_total - self.amount_paid) < 0.02):
			self.write({'amount_total': self.amount_paid})
			return True
		else:
			return False

	@api.model
	def _payment_fields(self, order, ui_paymentline):
		payment_total = []
		company_id = self.env.user.company_id
		payment_date = ui_paymentline['name']
		payment_date = fields.Date.context_today(self, fields.Datetime.from_string(payment_date))
		price_unit_foreign_curr = 0.0

		price_unit_comp_curr = ui_paymentline['amount'] or 0.0
		currency_id = False

		if order.pricelist_id.currency_id.id != order.currency_id.id:
			# Convert
			price_unit_foreign_curr = ui_paymentline['amount']
			price_unit_comp_curr = order.pricelist_id.currency_id._convert(price_unit_foreign_curr, order.currency_id, order.company_id, payment_date)
			currency_id = order.pricelist_id.currency_id.id
			price_unit_comp_curr = price_unit_comp_curr

		return {
			'amount_currency': price_unit_foreign_curr,
			'currency': currency_id,
			'amount': price_unit_comp_curr or 0.0,
			'payment_date': payment_date,
			'payment_method_id': ui_paymentline['payment_method_id'],
			'card_type': ui_paymentline.get('card_type'),
			'transaction_id': ui_paymentline.get('transaction_id'),
			'pos_order_id': order.id,
		}

	def _prepare_invoice_line(self, order_line):
		vals = super(POSOrder,self)._prepare_invoice_line(order_line)
		_logger.info("_prepare_invoice_line")
		_logger.info(order_line.read())
		_logger.info(vals)
		if order_line.foreign_currency:
			vals.update({
				"price_unit":order_line.price_unit_currency,
			})
		return vals
        # return {
        #     'product_id': order_line.product_id.id,
        #     'quantity': order_line.qty if self.amount_total >= 0 else -order_line.qty,
        #     'discount': order_line.discount,
        #     'price_unit': order_line.price_unit,
        #     'name': order_line.product_id.display_name,
        #     'tax_ids': [(6, 0, order_line.tax_ids_after_fiscal_position.ids)],
        #     'product_uom_id': order_line.product_uom_id.id,
        # }

	# def _prepare_invoice_vals(self):
	# 	vals = super(POSOrder, self)._prepare_invoice_vals()
	# 	_logger.info("_prepare_invoice_vals")
	# 	_logger.info(vals)
	# 	return vals
	# {'product_id': 139, 'quantity': 1.0, 'discount': 0.0, 'price_unit': 100.51, 'name': '[664] Tinta Negra T664 120 Epson 664', 'tax_ids': [(6, 0, [2])], 'product_uom_id': 1}


	@api.model
	def _order_fields(self, ui_order):
		vals = super(POSOrder, self)._order_fields(ui_order)
		amount_total = []
		amount_total_currency = []
		amt_total = ui_order['amount_total']
		amt_paid = ui_order['amount_paid']
		pricelist_id = self.env['product.pricelist'].browse(ui_order.get('pricelist_id'))
		amt_total_currency = 0
		
		if ui_order['lines']:
			pos_session = self.env['pos.session'].browse(ui_order.get('pos_session_id'))
			pricelist_id = self.env['product.pricelist'].browse(ui_order.get('pricelist_id'))
			foreign_currency = pricelist_id.currency_id.id
			payment_date = fields.Date.today()
			if pos_session.currency_id.id != pricelist_id.currency_id.id:
				for line in ui_order['lines']:
					price_unit_foreign_curr = line[2].get('price_unit') or 0.0
					price_unit_comp_curr = pricelist_id.currency_id._convert(price_unit_foreign_curr, pos_session.currency_id, pos_session.company_id, payment_date)
					price_subtotal_foreign_curr = line[2].get('price_subtotal') or 0.0
					price_subtotal_comp_curr = pricelist_id.currency_id._convert(price_subtotal_foreign_curr, pos_session.currency_id, pos_session.company_id, payment_date)
					price_subtotal_incl_foreign_curr = line[2].get('price_subtotal_incl') or 0.0
					price_subtotal_incl_comp_curr = pricelist_id.currency_id._convert(price_subtotal_incl_foreign_curr, pos_session.currency_id, pos_session.company_id, payment_date)
					line[2].update({
							'price_unit':price_unit_comp_curr,
							'price_subtotal':price_subtotal_comp_curr,
							'price_subtotal_incl':price_subtotal_incl_comp_curr,
							'price_unit_currency':price_unit_foreign_curr,
							'price_subtotal_currency':price_subtotal_foreign_curr,
							'price_subtotal_incl_currency':price_subtotal_incl_foreign_curr,
							'foreign_currency':pricelist_id.currency_id.id
						})
					amount_total.append(price_subtotal_incl_comp_curr)
					amount_total_currency.append(price_subtotal_incl_foreign_curr)
				amount_total_foreign_curr = ui_order.get('amount_total')
				amount_total_comp_curr = pricelist_id.currency_id._convert(amount_total_foreign_curr, pos_session.currency_id, pos_session.company_id, payment_date)
				ui_order.update({'amount_total': sum(amount_total)})
				amt_total = sum(amount_total)
				amt_paid =  sum(amount_total)
				amt_total_currency = sum(amount_total_currency)
				
		process_line = partial(self.env['pos.order.line']._order_line_fields, session_id=ui_order['pos_session_id'])
		vals.update({
			'user_id':      ui_order['user_id'] or False,
			'session_id':   ui_order['pos_session_id'],
			'lines':        [process_line(l) for l in ui_order['lines']] if ui_order['lines'] else False,
			'pos_reference': ui_order['name'],
			'sequence_number': ui_order['sequence_number'],
			'partner_id':   ui_order['partner_id'] or False,
			'date_order':   ui_order['creation_date'].replace('T', ' ')[:19],
			'fiscal_position_id': ui_order['fiscal_position_id'],
			'pricelist_id': ui_order['pricelist_id'],
			'amount_paid':  amt_paid,
			'amount_total':  amt_total,
			'amount_total_currency': amt_total_currency,
			'foreign_currency': foreign_currency,
			'amount_tax':  ui_order['amount_tax'],
			'amount_return':  ui_order['amount_return'],
			'company_id': self.env['pos.session'].browse(ui_order['pos_session_id']).company_id.id,
			'to_invoice': ui_order['to_invoice'] if "to_invoice" in ui_order else False,
		})
		return vals

	def _process_payment_lines(self, pos_order, order, pos_session, draft):
		"""Create account.bank.statement.lines from the dictionary given to the parent function.

		If the payment_line is an updated version of an existing one, the existing payment_line will first be
		removed before making a new one.
		:param pos_order: dictionary representing the order.
		:type pos_order: dict.
		:param order: Order object the payment lines should belong to.
		:type order: pos.order
		:param pos_session: PoS session the order was created in.
		:type pos_session: pos.session
		:param draft: Indicate that the pos_order is not validated yet.
		:type draft: bool.
		"""
		prec_acc = order.pricelist_id.currency_id.decimal_places
		pricelist_id = self.env['product.pricelist'].browse(pos_order.get('pricelist_id'))
		order_bank_statement_lines= self.env['pos.payment'].search([('pos_order_id', '=', order.id)])
		order_bank_statement_lines.unlink()
		payment_date = fields.Date.today()
		for payments in pos_order['statement_ids']:
			if not float_is_zero(payments[2]['amount'], precision_digits=prec_acc):
				order.add_payment(self._payment_fields(order, payments[2]))

		order.amount_paid = sum(order.payment_ids.mapped('amount'))

		currency_id = False
		amt_currncy = 0.0
		price_subtotal_comp_curr = pos_order['amount_return']
		if pos_session.currency_id.id != pricelist_id.currency_id.id:
			price_subtotal_comp_curr = pricelist_id.currency_id._convert(pos_order['amount_return'], pos_session.currency_id, pos_session.company_id, payment_date)
			currency_id = order.pricelist_id.currency_id.id
			amt_currncy = -pos_order['amount_return']
		if not draft and not float_is_zero(pos_order['amount_return'], prec_acc):
			cash_payment_method = pos_session.payment_method_ids.filtered('is_cash_count')[:1]
			if not cash_payment_method:
				raise UserError(_("No cash statement found for this session. Unable to record returned cash."))
			return_payment_vals = {
				'name': _('return'),
				'pos_order_id': order.id,
				'amount_currency': amt_currncy,
				'currency': currency_id,
				'amount': -price_subtotal_comp_curr,
				'payment_date': fields.Date.context_today(self),
				'payment_method_id': cash_payment_method.id,
			}
			order.add_payment(return_payment_vals)


class POSConfig(models.Model):
	
	_inherit = 'pos.config'
		
	@api.constrains('pricelist_id', 'use_pricelist', 'available_pricelist_ids', 'journal_id', 'invoice_journal_id', 'payment_method_ids')
	def _check_currencies(self):
		for config in self:
			if config.use_pricelist and config.pricelist_id not in config.available_pricelist_ids:
				raise ValidationError(_("The default pricelist must be included in the available pricelists."))

		if self.invoice_journal_id.currency_id and self.invoice_journal_id.currency_id != self.currency_id:
			raise ValidationError(_("The invoice journal must be in the same currency as the Sales Journal or the company currency if that is not set."))

		if any(
			self.payment_method_ids\
				.filtered(lambda pm: pm.is_cash_count)\
				.mapped(lambda pm: self.currency_id not in (self.company_id.currency_id | pm.cash_journal_id.currency_id))
		):
			raise ValidationError(_("All payment methods must be in the same currency as the Sales Journal or the company currency if that is not set."))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: