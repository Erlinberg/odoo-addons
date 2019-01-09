# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012-Present (<http://www.acespritech.com/>) Acespritech Solutions Pvt.Ltd
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name' : 'altinkaya_customV7',
    'version' : '1.0',
    'category': 'General',
    'depends' : ['base', 'sale', 'stock', 'sale_stock', 'delivery'],
    'author' : 'Acespritech Solutions Pvt. Ltd.',
    'description': """
    Sales Order Customization
        * Provides Invoice Address
        * Provides Delivery Address
        * History of Invoices and Picking
        * Delivery Method
        * Add Button In delivery order for reference to Sale order.
    """,
    'website': 'http://www.acespritech.com',
    'data': [
             'sale/sales_order_view.xml',
             'stock/stock_view.xml'
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: