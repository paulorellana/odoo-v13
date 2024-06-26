from odoo import http, _
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.http import request
from odoo.exceptions import AccessError, MissingError

class PortalEI(PortalAccount):

    @http.route(['/my/invoices/<int:invoice_id>/ei/xml'], type='http', auth="public", website=True)
    def portal_my_invoice_ei_xml(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        try:
            invoice_sudo = self._document_check_access('account.move', invoice_id, access_token)
            account_invoice_log = invoice_sudo.current_log_status_id
            if account_invoice_log.exists():
                xml_headers = [
                    ('Content-Type', 'application/xml'),
                    ('Content-Length', len(account_invoice_log.signed_xml_data_without_format)),
                    ('Content-Disposition', 'attachment; filename="%s.xml"' % (invoice_sudo.name)),
                ]
                return request.make_response(account_invoice_log.signed_xml_data_without_format, headers=xml_headers)

        except (AccessError, MissingError):
            return request.redirect('/my')

    @http.route(['/my/invoices/<int:invoice_id>/ei/cdr'], type='http', auth="public", website=True)
    def portal_my_invoice_ei_cdr(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        try:
            invoice_sudo = self._document_check_access('account.move', invoice_id, access_token)
            account_invoice_log = invoice_sudo.current_log_status_id
            if account_invoice_log.exists():
                xml_headers = [ 
                    ('Content-Type', 'application/xml'),
                    ('Content-Length', len(account_invoice_log.response_xml_without_format)),
                    ('Content-Disposition', 'attachment; filename="%s.xml"' % (account_invoice_log.name)),
                ]
                return request.make_response(account_invoice_log.response_xml_without_format, headers=xml_headers)

        except (AccessError, MissingError):
            return request.redirect('/my')
        
    @http.route(['/my/invoices/<int:invoice_id>/ei/cdr_content'], type='http', auth="public", website=True)
    def portal_my_invoice_ei_cdr_content(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        try:
            invoice_sudo = self._document_check_access('account.move', invoice_id, access_token)
            account_invoice_log = invoice_sudo.current_log_status_id
            if account_invoice_log.exists():
                xml_headers = [
                    ('Content-Type', 'application/xml'),
                    ('Content-Length', len(account_invoice_log.response_content_xml)),
                    ('Content-Disposition', 'attachment; filename="%s_content_cdr.xml"' % (invoice_sudo.name)),
                ]
                return request.make_response(account_invoice_log.response_content_xml, headers=xml_headers)

        except (AccessError, MissingError):
            return request.redirect('/my')