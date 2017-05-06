# -*- coding: utf-8 -*-
from odoo import http

# class DepositSubjectWason(http.Controller):
#     @http.route('/deposit_subject_wason/deposit_subject_wason/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/deposit_subject_wason/deposit_subject_wason/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('deposit_subject_wason.listing', {
#             'root': '/deposit_subject_wason/deposit_subject_wason',
#             'objects': http.request.env['deposit_subject_wason.deposit_subject_wason'].search([]),
#         })

#     @http.route('/deposit_subject_wason/deposit_subject_wason/objects/<model("deposit_subject_wason.deposit_subject_wason"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('deposit_subject_wason.object', {
#             'object': obj
#         })