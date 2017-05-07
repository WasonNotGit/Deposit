# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
#from procal import ProdCal


import logging
_logger = logging.getLogger (__name__)

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
    owner = 1
    relative = 2
    representative = 3
    broker = 4
    middleman = 5

    values = {
        owner: u'Собственник',
        relative: u'Родственник собственника',
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
    privatization = 2
    legacy = 3
    share_participating = 4
    gift = 5
    change = 6
    building = 7
    declaration = 8
    courth_decision = 9
    auction = 10
    other = 100

    values = {
        purchase: u'договор купли-продажи',
        privatization: u'приватизация',
        legacy: u'Наследство',
        share_participating: u'договор долевого участия',
        gift: u'договор дарения',
        change: u'договор мены',
        building: u'договор строительного подряда',
        declaration: u'декларация на дом',
        courth_decision: u'Решение суда',
        auction: u'реализация с торгов',
        other: u'прочее',
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

class WaterSupply():
    not_avail = 0
    chink = 1
    well = 2
    central = 3
    other = 10

    values = {
        not_avail: u'отсутствует',
        chink: u'скважина',
        well: u'Колодец',
        central: u'Центральное',
        other: u'Другое',
    }

    @classmethod
    def get_values(cls):
        return [(x, cls.values[x]) for x in cls.values]


def is_working_day (checking_date):
    #if checking_date.
    oficial_holidays = { date (2017, 5, 1), date (2017, 5, 8), date (2017, 5, 9), date (2017, 6, 12), date (2017, 11, 6), date (2018, 1, 1),
        date (2018, 1, 2), date (2018, 1, 3), date (2018, 1, 4), date (2018, 1, 5), date (2018, 1, 8), date (2018, 1, 9),
        date (2018, 2, 23), date (2018, 3, 8), date (2018, 5, 1), date (2018, 5, 9), date (2018, 11, 5)
     }
    _logger.debug (u'checking_date {}, type: {}'.format(checking_date , type(checking_date)) )
    if (checking_date in oficial_holidays):
        return False
    isoweekday = checking_date.weekday()
    _logger.debug (u'checking_date.isoweekday() {}'.format(checking_date.isoweekday() ))
    return checking_date.isoweekday()<6

def closest_working_day (starting_date, step):
    #prod_cal = ProdCal()
    _logger.debug (u'starting_date {} step {}'.format(starting_date, step))
    final_date=starting_date
    while not is_working_day(final_date):
        final_date += timedelta(days=step) 
    return final_date

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

class deposit_subject(models.Model):
    _name = 'deposit_subject_wason'
  #  _order = "crm_lead, floor, "
    _inherit = ['mail.thread']

    @api.constrains('square_meters')   
    def _check_string(self):
        for data in self:
            if data.square_meters < 3:
                 raise exceptions.ValidationError("Please enter the marks !")
        return True

    @api.onchange('square_meters')   
    def _check_string1(self):
        for data in self:
            if data.square_meters < 3:
                 raise exceptions.ValidationError("Onchange enter the marks !")
        return True


    _sql_constraints = [
    ('crm_lead_id', 'unique("crm_lead_id")', 'Field crm_lead_id must be unique.'),

  ]

    # Основные поля
    crm_lead_id = fields.Many2one('crm.lead', string='Lead',
                               required=True)
    stage_id = fields.Many2one(related='crm_lead_id.stage_id',
                                                 readonly=True)
    lead_email = fields.Char(related='crm_lead_id.email_from',readonly=False)

    contact_name = fields.Char(related='crm_lead_id.contact_name', string=u'Подскажите, как Вас зовут?',readonly=False)
    lead_phone = fields.Char(related='crm_lead_id.phone', readonly=False)
    # Поля займа

    deposit_type = fields.Selection(DepositType.get_values(), string=u'Что у Вас за объект?', index=True, default=None, track_visibility='onchange')
    loan_period_selection = fields.Selection ([(1,"1 месяц"),(2,"2 месяца"),(3,"3 месяца"),(4,"4 месяца"),(5,"5 месяцев"),(6,"6 месяцев"),(10,"10 месяцев"),
        (12,"1 год"),(18,"полтора года"),(24,"2 года"),(36,"3 года"),(48,"4 года"),(60,"5 лет"),(120,"10 лет"),(1000,"другой срок")], string=u'На какой срок Вы хотите взять займ?', default=None, track_visibility='onchange')
    loan_period_months = fields.Integer(string=u"На какой срок Вы хотите взять займ? (в месяцах)", default=0, track_visibility='onchange')
    share = fields.Selection ([(1,"Целиком"),(2,"Доля")], string=u'Объект закладываете целиком или долю', default=None, track_visibility='onchange')
    number_rooms = fields.Integer(string=u"Сколько комнат", track_visibility='onchange')
    square_meters = fields.Integer(string=u"Метраж?", track_visibility='onchange')
    square_acrs = fields.Integer(string=u"Сколько соток участок?", track_visibility='onchange')
    floor = fields.Integer(string=u"Этаж", track_visibility='onchange')
    land_status = fields.Selection(LandStatus.get_values(), string=u'По целевому назначению участка это земли: ', default=None, track_visibility='onchange')
    deposit_object_address = fields.Char (string=u'Адрес объекта', track_visibility='onchange')
    current_contact_to_owner = fields.Selection(CurrentContactRelationToOwner.get_values(), string=u'Вы собственник объекта?', index=False, default=None, track_visibility='onchange')
    consanguinity = fields.Char (string=u'Укажите родство', default=None, track_visibility='onchange')
    how_many_owners = fields.Selection(OneOrMany.get_values(), string=u'Сколько собственников у объекта: ', default=None, track_visibility='onchange')
    other_owners_agree = fields.Selection (NullableBoolean.get_values(), string=u'Все остальные собственники тоже будут закладывать?', default=None, track_visibility='onchange')
    minors_owners = fields.Selection (NullableBoolean.get_values(), string=u'Есть ли среди собственников несовершеннолетние?', default=None, track_visibility='onchange')
    arested = fields.Selection (NullableBoolean.get_values(), string=u'Есть ли обременения на объекте (аресты, ипотека)?', default=None, track_visibility='onchange')
    in_marriage = fields.Selection (NullableBoolean.get_values(), string=u'Объект приобретался в браке?', default=None, track_visibility='onchange')
    spose_agree = fields.Selection (NullableBoolean.get_values(), string=u'Будет ли нотариальное согласие супруга(и) на сделку?', required=False, default=None, track_visibility='onchange')
    marriage_contract = fields.Selection (NullableBoolean.get_values(), string=u'Имеется ли брачный договор?', required=False, default=None, track_visibility='onchange')
    reason_of_ownership = fields.Selection (ReasonOfOwnership.get_values(), string=u'Укажите, основание собственности: ', required=False, default=None, track_visibility='onchange')
    # Согласие супруги не требуется, т.к. объект приобретался по Договору дарения, приватизации или в наследство.
    how_many_regestered = fields.Integer(string=u"Сколько человек зарегистрировано на объекте", default=-1, track_visibility='onchange')
    minors_regestered = fields.Selection (NullableBoolean.get_values(), string=u'Есть ли среди зарегистрированных несовершеннолетние?', default=None, track_visibility='onchange')
    deposit_ownership_date = fields.Date(string=u'Дата возникновения права собственности', track_visibility='onchange')
    required_loan_amount = fields.Integer(string=u"Какая сумма Вам нужна?", track_visibility='onchange')
    loan_deadline = fields.Date(string=u"Не позднее какой даты Вам нужны деньги?", track_visibility='onchange')
    email_documents = fields.Selection (NullableBoolean.get_values(), string=u'Смогу отправить по электронной почте', required=False, default=None)
    deliver_documents = fields.Selection (NullableBoolean.get_values(), string=u'Смогу приехать в офис с документами', required=False, default=None)
    electricity_power = fields.Float(string=u"Сколько КВт электричества?", default=-1, track_visibility='onchange')
    gas_available = fields.Selection (NullableBoolean.get_values(), string=u'Есть ли газ?', default=None, track_visibility='onchange')
    water_supply = fields.Selection(WaterSupply.get_values(), string=u'Водоснабжение: ', default=None, track_visibility='onchange')
    sewerage = fields.Selection([(0,"Отсутствует"),(1,"Септик"),(2,"Центральная"),(10,"Прочее")], string=u'Канализация: ', default=None, track_visibility='onchange')
    heating = fields.Selection([(0,"Отсутствует"),(1,"Центральное"),(10,"Прочее")], string=u'Отопление: ', default=None, track_visibility='onchange')
    house_materials = fields.Selection([(0,"Дерево"),(1,"Брус"),(2,"Газобетон"),(3,"Кирпич"),(4,"Каркасный (в том числе СИП-панели)"),(10,"Прочее")], string=u'Из каких материалов построен дом: ', default=None, track_visibility='onchange')
    basement_materials = fields.Selection([(0,"Бетонный"),(1,"Свайный"),(10,"Прочее")], string=u'Какой фундамент: ', default=None, track_visibility='onchange')

    message = fields.Text(string="Message", compute="write_message")


    @api.onchange('loan_period_selection')
    @api.multi
    def change_loan_period(self):
        _logger.debug (u'self.loan_period_months {} имеет тип: {})'.format(self.loan_period_months, type (self.loan_period_months)) )
        if self.loan_period_selection==1000 :
            self.loan_period_months = 0
        else:
            self.loan_period_months = self.loan_period_selection
        #return True

    @api.onchange('required_loan_amount', 'loan_deadline', 'electricity_power', 'loan_period_months')
    @api.multi
    def write_message(self):
        if self.electricity_power>0 :
            total_amount = 0
            month_payment=self.required_loan_amount * self.electricity_power /100
            start_loan_date = datetime.datetime.strptime(self.loan_deadline, '%Y-%m-%d').date()
            first_payment_date = closest_working_day(start_loan_date + timedelta (days=1),1) 
            #_logger.debug (u'Уплата первой доли займа в сумме {} должна быть произведена не позднее {} (тип: {})'.format(month_payment,start_loan_date, type (start_loan_date)) )
            self.message=u'Уплата первой доли займа в сумме {1} должна быть произведена не позднее {0:%d.%m.%Y}.'.format(first_payment_date, month_payment)
            total_amount += month_payment
            for i in xrange(1,self.loan_period_months):
                next_payment_date = closest_working_day(last_day_of_month (start_loan_date + relativedelta (months=i)),-1)
                self.message += u' Не позднее {:%d.%m.%Y} в сумме {}.'.format(next_payment_date, month_payment)
                total_amount += month_payment
            last_payment_date = closest_working_day(start_loan_date + relativedelta (months=self.loan_period_months),1)
            self.message += u' Не позднее {:%d.%m.%Y} в сумме {}.'.format(last_payment_date, self.required_loan_amount)
            total_amount += self.required_loan_amount
            self.message = u'Займодавец предоставляет заёмщику денежную сумму в размере {}. '.format(total_amount) + self.message
            self.message += u' Таким образом, суммарно за {} месяцев получается {}'.format (self.loan_period_months, 
                (total_amount-self.required_loan_amount))
        else:
            self.message=u' '
    # mydomain = fields.Boolean(string=u"Видимость", compute= 'it_is_share')

    # @api.depends('share', 'other_owners_agree', 'how_many_owners')
    # @api.multi
    # def it_is_share (self):
    #     if self.share==0 or self.other_owners_agree==2 or self.how_many_owners==2:
    #         return True
    #     return False
    # @api.onchange('share', 'deposit_type')
    # @api.multi
    # def write_message(self):
    #     self.stage_id=crm.stage_id
    #     if self.share==1 : # and self.other_owners_agree==2 and self.how_many_owners==2
    #         self.message=u'Внимание! На самом деле человек хочет заложить только долю! Исправьте ниже ответ на вопрос: Закладывается доля'
    #     else:
    #         self.message=u' '

    @api.one
    def do_send_email(self):
        return  True


