# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import logging
_logger = logging.getLogger (__name__)

class wason_lead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'
   # _inherits = {'deposit_subject_wason': 'id_deposit'}
    _sql_constraints = [
    ('id_deposit', 'unique("id_deposit")', 'Field id_deposit must be unique.'),
  ]

    id_deposit = fields.Many2one('deposit_subject_wason', string='Deposit', ondelete='cascade')

    # -- Create
    @api.model
    def create(self, vals):
        res = super(wason_lead, self).create(vals)
        deposit_id = self.env['deposit_subject_wason'].create({
                     'crm_lead_id': res.id,
                     'id' : 1529,
                     'deposit_object_address' : 'adress 01',
                    # 'name': res.name,
                    # 'user_id': self._uid,  
                    # 'order_id': res.id,
                    # 'source_ref': "sale.order,"+str(res.id),
                    # 'dod_est': datetime.today(),
                    # 'partner_shipping_id': vals['partner_shipping_id'],
                    # 'state': '0', ,,,
                    })
        #new_lead = self.env['crm.lead'].search(['id','=',res.id])
        new_lead = self.env['crm.lead'].browse(res.id)
        new_lead.id_deposit = deposit_id
        #new_lead.stage_id = 10
        return res

class deposit_subject_import(models.Model):
    _name = 'deposit_subject_import_wason'
    importing_leads = fields.Text (string=u'Введите сохраняемые лиды в формате: номер телефона,имя(необязательно),название лида', default=None, required=True, track_visibility='onchange')
    processed_leads = fields.Text (string="Так выглядят обработанные лиды:", compute="process_leads", store=True)


    @api.onchange('importing_leads')
    @api.multi
    def process_leads(self):
        #_logger.debug (u'self.importing_leads {} имеет тип: {})'.format(self.importing_leads, type (type (self.importing_leads))) )
        self.process_leads=type(self.importing_leads)
        if type (self.importing_leads)==unicode :
            _logger.debug (u'self.importing_leads {} имеет тип: {})'.format(self.importing_leads, type (self.importing_leads)) )
            self.process_leads=u'Ehfsdfg'
