# _*_ coding:utf-8 _*_

{
    'name': 'Modulo de peliculas',
    'version': '1.0',
    'depends': [
        'contacts',
        'mail',
    ],
    'author': 'Dilcia Barrios',
    'category': 'Peliculas',
    'website': 'http://www.google.com',
    'summary': 'Modulo de Presupuestos de peliculas',
    'description': '''
    Modulo para hacer presupuestos de peliculas
    ''',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/secuencia.xml',
        'data/categoria.xml',
        'wizard/update_wizard_views.xml',
        'report/report_pelicula.xml',
        'views/presupuesto_views.xml',
        'views/menu.xml',
    ],
}