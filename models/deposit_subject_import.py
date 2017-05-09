# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import re
import const

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

def add_key_or_error (our_dictionary, new_key, new_value):
    if our_dictionary.has_key (new_key):
        our_dictionary[u'Ошибка'] += u" По меньшей мере дважды указано поле '{}': '{}' и '{}'".format (new_key, our_dictionary[new_key],new_value)
    else:
        our_dictionary[new_key] = new_value

def and_colon(original_string):
    return original_string+u": "

class deposit_subject_import(models.Model):
    _name = 'deposit_subject_import_wason'
    importing_leads = fields.Text (string=u'Введите сохраняемые лиды в формате: номер телефона,имя(необязательно),название лида', default=None, required=True, track_visibility='onchange')
    processed_leads = fields.Text (string="Так выглядят обработанные лиды:", compute="process_leads", store=True)
    const.LEAD_DICT_KEY_NAME = u"Имя"
    const.LEAD_DICT_KEY_PHONE = u"Телефон"
    const.LEAD_DICT_KEY_COMMENT = u"Комментарий"

    @api.onchange('importing_leads')
    @api.multi
    def process_leads(self):
        #_logger.debug (u'self.importing_leads {} имеет тип: {})'.format(self.importing_leads, type (type (self.importing_leads))) )
        self.process_leads=type(self.importing_leads)
        if type (self.importing_leads)==unicode :
            _logger.debug (u'self.importing_leads {} имеет тип: {})'.format(self.importing_leads, type (self.importing_leads)) )
            leads = re.split ('^[\-=_]+$',self.importing_leads,0,re.MULTILINE) # https://docs.python.org/2/library/re.html
            # первый параметр - регулярное выражение поиска: ищем в начале строки любой из символов в кв скобках, повторящиейся, 
            # https://habrahabr.ru/post/115825/ - вот здесь хорошо про регулярные выражения
            # второй - строка, где ищем, далее указываем, что все вхождения
            # ну и далее флаг многострочного режима
            self.processed_leads = "=================".join (leads)
            # формат ввода: сначала имя (или знак вопроса, лили может не быть имени), потом номер телефона в любом формате, потом текст
            leads_count = 0
            for next_lead in leads:   # это цикл по "лидам" - каждый лид несколько строк через разделители - специальный строки
                _logger.debug (u'leads_count {} next_lead: {}'.format(leads_count, next_lead) )
                next_lead_lines = filter(None, next_lead.split('\n')) # удаляем заодно пустые строки
                new_lead = {u'Ошибка':'', u'Введено':next_lead}
                for next_lead_line in next_lead_lines:   # это цикл по строкам внутри одного лида
                    next_lead_line = next_lead_line.strip()
                    if next_lead_line in (u"?", and_colon (const.LEAD_DICT_KEY_NAME)):
                        # значит имя отсутствует
                        add_key_or_error (new_lead,const.LEAD_DICT_KEY_NAME,"")
                    elif re.match ('^(\+7|[1-689\(]|Телефон: \+7|Телефон: [1-689\(])[\d\-\( )]{9,15}$', next_lead_line) == None:
                        _logger.debug (u'не номер телефона' )
                        # может быть или комментарий или имя
                        if next_lead_line[:5]==and_colon (const.LEAD_DICT_KEY_NAME):
                            add_key_or_error (new_lead,const.LEAD_DICT_KEY_NAME,next_lead_line [5:])
                        elif next_lead_line[:13]==and_colon (const.LEAD_DICT_KEY_COMMENT):
                            add_key_or_error (new_lead,const.LEAD_DICT_KEY_COMMENT,next_lead_line [13:])
                        elif new_lead.has_key (const.LEAD_DICT_KEY_NAME):
                            add_key_or_error (new_lead,const.LEAD_DICT_KEY_COMMENT,next_lead_line)
                        else:
                            add_key_or_error (new_lead,const.LEAD_DICT_KEY_NAME,next_lead_line)
                    else: # номер телефона
                        add_key_or_error (new_lead,const.LEAD_DICT_KEY_PHONE,next_lead_line)
                
                if not new_lead.has_key (const.LEAD_DICT_KEY_PHONE):
                    new_lead[u'Ошибка'] += u" Не найден номер телефона для связи!"
                leads [leads_count] = new_lead
                leads_count += 1
                _logger.debug (u'new_lead {}'.format(new_lead) )
                self.processed_leads += str (new_lead).encode ('utf8')
            #self.processed_leads = "---".join (d['Введено'] for d in leads)  # http://stackoverflow.com/questions/5253773/convert-list-of-dicts-to-string
