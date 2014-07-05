{
    'name': 'ALTINKAYA',
    'version': '1.0',
    'author': 'Altinkaya Enclosures',
    'website': 'http://www.altinkaya.eu',
    'category': 'tools',
    'sequence': 1,
    'summary': 'Altinkaya Enclosures Customizations for V7',
    'images': [],
    'depends': ['crm','mail','account_voucher','account_accountant','sale','stock','mrp','purchase','hr','account',
    'account_cancel','analytic','base','base_action_rule','base_setup','base_status','board','contacts',
    'decimal_precision','delivery','document','edi','email_template','fetchmail','knowledge','mrp_operations',
    'process','procurement','product','product_visible_discount'],
    'description': """
Altinkaya Elektronik Cihaz Kutulari OpenERP V7 ozellestirmeleri
===============================================================

    Kullanilan modulleri yukler
    Gerekli goruntu degisikliklerini yapar.
    
    
    """,
    'data': [
    "view/altinkaya_view_sales.xml",
    "view/altinkaya_view_product.xml",
    "view/altinkaya_view_payment.xml",
    "view/altinkaya_view_partner.xml",
    "view/altinkaya_view_stock.xml",
    "view/altinkaya_view_manufacturing.xml",
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
