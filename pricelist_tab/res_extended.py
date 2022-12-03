# -*- coding: utf-8 -*-


import logging

from odoo import api, fields, models
#from openerp.tools.translate import _


_logger = logging.getLogger(__name__) # Need for message in console.

# for store more option in res.extended. It for store in one place any options.
class res_extended(models.Model):

    _name = 'res.extended'

    name =fields.char('Name', size=128, required=False),
    type_opt =fields.char('Type', size=128, required=False),
    id_opt=fields.integer('Id Operation', required=False, help="Id Operation"),
    value_opt=fields.char('Value', size=128, required=False),

res_extended()

