# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DepositType():
    flat = 1
    room = 2
    house = 3
    auto = 4
    land = 5
    premise = 6

    values = {
        flat: u'Квартира',
        room: u'Комната',
        house: u'Дом с земельным участком',
        auto: u'Автомобиль',
        land: u'Земельный участок',
        premise: u'Нежилое коммерческое помещение',
    }

    @classmethod
    def get_values(cls):
        return [(x, cls.values[x]) for x in cls.values]

class LandStatus():
    agriculture = 1
    village = 2
    industrial = 3
    guard = 4
    forest = 5
    water = 6
    reserve = 7
    another = 100

    values = {
        agriculture: u'сельскохозяйственного назначения',
        village: u'населенных пунктов',
        industrial: u'промышленности, энергетики, транспорта, связи,..',
        guard: u'особо охраняемых территорий и объектов',
        forest: u'лесного фонда',
        water: u'водного фонда',
        reserve: u'запаса',
        another: u'Прочее',
    }

    @classmethod
    def get_values(cls):
        return [(x, cls.values[x]) for x in cls.values]


class CurrentContactRelationToOwner():
    owner1 = 1
    relative1 = 2
    representative = 3
    broker = 4
    middleman = 5

    values = {
        owner1: u'Собственник',
        relative1: u'Родственник собственника',
        representative: u'Представитель собственника',
        broker: u'Брокер',
        middleman: u'Посредник',
    }

    @classmethod
    def get_values(cls):
        return [(x, cls.values[x]) for x in cls.values]


class NullableBoolean():
    yes = 1
    no = 2

    values = {
        yes: u'Да',
        no: u'Нет',
    }

    @classmethod
    def get_values(cls):
        return [(x, cls.values[x]) for x in cls.values]


class ReasonOfOwnership():
    purchase = 1
    legacy = 2
    courth_decision = 3

    values = {
        purchase: u'Купля-продажа',
        legacy: u'Наследство',
        courth_decision: u'Решение суда',
    }

    @classmethod
    def get_values(cls):
        return [(x, cls.values[x]) for x in cls.values]

class OneOrMany():
    one = 1
    many = 2

    values = {
        one: u'Один',
        many: u'Два или более',
    }

    @classmethod
    def get_values(cls):
        return [(x, cls.values[x]) for x in cls.values]


class deposit_subject(models.Model):
    _name = 'deposit_subject_wason'
  #  _order = "crm_lead, floor, "
    _inherit = ['mail.thread']

    _sql_constraints = [
    ('crm_lead_id', 'unique("crm_lead_id")', 'Field crm_lead_id must be unique.'),
  ]

    # Основные поля
    crm_lead_id = fields.Many2one('crm.lead', string='Lead',
                               required=True)
    stage_id = fields.Many2one(related='crm_lead_id.stage_id',
                                                 readonly=True)
    lead_email = fields.Char(related='crm_lead_id.email_from',readonly=False)

    contact_name = fields.Char(related='crm_lead_id.contact_name', string=u'Как к Вам обращаться?',readonly=False)
    #lambda self: self.env.context.get('default_crm_lead', False)
    # Поля займа

    deposit_type = fields.Selection(DepositType.get_values(), string=u'Что у Вас за объект?', index=True, default=None, track_visibility='onchange')
    share = fields.Selection ([(0,"Целиком"),(1,"Доля")], string=u'Объект закладываете целиком или долю', default=None, track_visibility='onchange')
    number_rooms = fields.Integer(string=u"Сколько комнат", track_visibility='onchange')
    square_meters = fields.Integer(string=u"Сколько квадратных метров?", track_visibility='onchange')
    square_acrs = fields.Integer(string=u"Сколько соток участок?", track_visibility='onchange')
    floor = fields.Integer(string=u"Этаж", track_visibility='onchange')
    land_status = fields.Selection(LandStatus.get_values(), string=u'По целевому назначению участка это земли: ', default=None, track_visibility='onchange')
    deposit_object_address = fields.Char (string=u'Адрес объекта', default=None, track_visibility='onchange')
    current_contact_to_owner = fields.Selection(CurrentContactRelationToOwner.get_values(), string=u'Вы являетесь собственником объекта?', index=False, default=None, track_visibility='onchange')
    consanguinity = fields.Char (string=u'Укажите родство', default=None, track_visibility='onchange')
    how_many_owners = fields.Selection(OneOrMany.get_values(), string=u'Сколько собственников у объекта: ', default=None, track_visibility='onchange')
    other_owners_agree = fields.Selection (NullableBoolean.get_values(), string=u'Все остальные собственники тоже будут закладывать?', default=None, track_visibility='onchange')
    minors_owners = fields.Selection (NullableBoolean.get_values(), string=u'Есть ли среди собственников несовершеннолетние?', default=None, track_visibility='onchange')
    arested = fields.Selection (NullableBoolean.get_values(), string=u'Есть ли обременения на объекте (аресты, ипотека)?', default=None, track_visibility='onchange')
    in_marriage = fields.Selection (NullableBoolean.get_values(), string=u'Объект приобретался в браке?', default=None, track_visibility='onchange')
    spose_agree = fields.Selection (NullableBoolean.get_values(), string=u'Будет ли нотариальное согласие супруга(и) на сделку?', required=False, default=None, track_visibility='onchange')
    marriage_contract = fields.Selection (NullableBoolean.get_values(), string=u'Имеется ли брачный договор?', required=False, default=None, track_visibility='onchange')
    reason_of_ownership = fields.Selection (ReasonOfOwnership.get_values(), string=u'Укажите, основание для возникновения собственности: ', required=False, default=None, track_visibility='onchange')
    # Согласие супруги не требуется, т.к. объект приобретался по Договору дарения, приватизации или в наследство.
    how_many_regestered = fields.Integer(string=u"Сколько человек зарегистрировано на объекте", track_visibility='onchange')
    minors_regestered = fields.Selection (NullableBoolean.get_values(), string=u'Есть ли среди зарегистрированных несовершеннолетние?', default=None, track_visibility='onchange')
    deposit_ownership_date = fields.Date(string=u'Дата возникновения права собственности', track_visibility='onchange')
    required_loan_amount = fields.Integer(string=u"Какая сумма Вам нужна?", track_visibility='onchange')
    loan_deadline = fields.Date(string=u"Примерно к какой дате Вам нужны деньги?", track_visibility='onchange')
    email_documents = fields.Selection (NullableBoolean.get_values(), string=u'Смогу отправить по электронной почте', required=False, default=None)
    deliver_documents = fields.Selection (NullableBoolean.get_values(), string=u'Смогу приехать в офис с документами', required=False, default=None)
    message = fields.Text(string="Message", compute="write_message")

    @api.onchange('share', 'other_owners_agree', 'how_many_owners')
    @api.multi
    def write_message(self):
        if self.share==1 : # and self.other_owners_agree==2 and self.how_many_owners==2
            self.message=u'Внимание! На самом деле человек хочет заложить только долю! Исправьте ниже ответ на вопрос: Закладывается доля'
        else:
            self.message=u' '
    # mydomain = fields.Boolean(string=u"Видимость", compute= 'it_is_share')

    # @api.depends('share', 'other_owners_agree', 'how_many_owners')
    # @api.multi
    # def it_is_share (self):
    #     if self.share==0 or self.other_owners_agree==2 or self.how_many_owners==2:
    #         return True
    #     return False

    @api.one
    def do_send_email(self):
        return  True

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
                    # 'id' : 537,
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
        return res
