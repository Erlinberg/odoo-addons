# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def _get_partner_currency(self):
        if self.property_account_receivable_id.currency_id and self.property_account_payable_id.currency_id:
            self.partner_currency_id = self.property_account_receivable_id.currency_id
        else:
            self.partner_currency_id = self.sudo().company_id.currency_id

    @api.multi
    def _compute_balances(self):
        AccountMoveLine = self.env['account.move.line']
        domain = [('partner_id', 'in', self.ids), ('account_id.internal_type', 'in', ['receivable', 'payable']),
                  ('date', '>=', "%s-01-01" % fields.Date.today().year)]

        result = dict((item['partner_id'][0], [item['debit'] - item['credit'], item['amount_currency']])
                      for item in
                      AccountMoveLine.read_group(domain, ['partner_id', 'credit', 'debit', 'amount_currency'],
                                                 ['partner_id'], orderby='id'))
        for partner in self:
            partner.balance = result[partner.id][0]
            partner.currency_balance = result[partner.id][1]

    partner_currency_id = fields.Many2one('res.currency', string='Partner Currency', readonly=True, store=True,
                                          compute='_get_partner_currency')

    balance = fields.Monetary(string='TRY Balance', compute='_compute_balances')
    currency_balance = fields.Monetary(string='Partner Currency Balance', compute='_compute_balances',
                                       currency_field='partner_currency_id')

    @api.one
    def change_accounts_to_usd(self):
        """ Change partners receivable and payable account to USD and update move lines accordingly """
        receivable_usd = self.env['account.account'].search([('code', '=', '120.USD')], limit=1)
        payable_usd = self.env['account.account'].search([('code', '=', '320.USD')], limit=1)
        old_receivable = self.property_account_receivable_id
        old_payable = self.property_account_payable_id
        company_currency = self.env.user.company_id.currency_id
        if not (receivable_usd and payable_usd):
            raise UserError(_('Error in accounts definition'))

        cr = self.env.cr
        cr.execute(
            """update account_move_line set account_id = {0} where partner_id = {1} and account_id = {2}""".format(
                receivable_usd.id, self.id, old_receivable.id))
        cr.execute(
            """update account_move_line set account_id = {0} where partner_id = {1} and account_id = {2}""".format(
                payable_usd.id, self.id, old_payable.id))

        self.write({'property_account_receivable_id': receivable_usd.id,
                    'property_account_payable_id': payable_usd.id})

        currency_id = receivable_usd.currency_id
        partner_amls = self.env['account.move.line'].search(["&", "&", "|", ("currency_id", "not in", [currency_id.id]),
                                                             ("amount_currency", "=", 0),
                                                             ("partner_id", "=", self.id),
                                                             ("account_id", "in", [payable_usd.id, receivable_usd.id])])
        for aml in partner_amls:
            amount_currency = company_currency._convert(aml.debit - aml.credit,
                                                        currency_id,
                                                        self.env.user.company_id, aml.date)

            amount_residual_currency = company_currency._convert(aml.amount_residual,
                                                                 currency_id,
                                                                 self.env.user.company_id, aml.date)
            cr.execute(
                """ update account_move_line
                 SET
                  amount_currency = {0},
                  currency_id = {1},
                  amount_residual_currency = {2}
                where id = {3}""".format(amount_currency,
                                         currency_id.id,
                                         amount_residual_currency,
                                         aml.id))

    @api.one
    def change_accounts_to_eur(self):
        """ Change partners receivable and payable account to eur and update move lines accordingly """
        receivable_eur = self.env['account.account'].search([('code', '=', '120.EUR')], limit=1)
        payable_eur = self.env['account.account'].search([('code', '=', '320.EUR')], limit=1)
        old_receivable = self.property_account_receivable_id
        old_payable = self.property_account_payable_id
        company_currency = self.env.user.company_id.currency_id
        if not (receivable_eur and payable_eur):
            raise UserError(_('Error in accounts definition'))

        cr = self.env.cr

        cr.execute(
            """update account_move_line set account_id = {0} where partner_id = {1} and account_id = {2}""".format(
                receivable_eur.id, self.id, old_receivable.id))
        cr.execute(
            """update account_move_line set account_id = {0} where partner_id = {1} and account_id = {2}""".format(
                payable_eur.id, self.id, old_payable.id))

        self.write({'property_account_receivable_id': receivable_eur.id,
                    'property_account_payable_id': payable_eur.id})

        currency_id = receivable_eur.currency_id
        partner_amls = self.env['account.move.line'].search(["|", ("currency_id", "not in", [currency_id.id]),
                                                             ("amount_currency", "=", 0),
                                                             ("partner_id", "=", self.id),
                                                             ("account_id", "in", [payable_eur.id, receivable_eur.id])])
        for aml in partner_amls:
            amount_currency = company_currency._convert(aml.debit - aml.credit,
                                                        currency_id,
                                                        self.env.user.company_id, aml.date)

            amount_residual_currency = company_currency._convert(aml.amount_residual,
                                                                 currency_id,
                                                                 self.env.user.company_id, aml.date)
            cr.execute(
                """ update account_move_line
                 SET
                  amount_currency = {0},
                  currency_id = {1},
                  amount_residual_currency = {2}
                where id = {3}""".format(amount_currency,
                                         currency_id.id,
                                         amount_residual_currency,
                                         aml.id))

    @api.one
    def change_accounts_to_try(self):
        """ Change partners receivable and payable account to company currency and donot update move lines """
        receivable_try = self.env['account.account'].search([('code', '=', '120')], limit=1)
        payable_try = self.env['account.account'].search([('code', '=', '320')], limit=1)
        old_receivable = self.property_account_receivable_id
        old_payable = self.property_account_payable_id

        if not (receivable_try and payable_try):
            raise UserError(_('Error in accounts definition'))

        cr = self.env.cr
        cr.execute(
            """update account_move_line set account_id = {0} where partner_id = {1} and account_id = {2}""".format(
                receivable_try.id, self.id, old_receivable.id))
        cr.execute(
            """update account_move_line set account_id = {0} where partner_id = {1} and account_id = {2}""".format(
                payable_try.id, self.id, old_payable.id))
        self.write({'property_account_receivable_id': receivable_try.id,
                    'property_account_payable_id': payable_try.id})