# _*_ coding: utf-8  _*_

from odoo import fields, models, api


class Presupuesto(models.Model):
    
    _name = "presupuesto"
    _inherit= ['image.mixin']

    name = fields.Char(string='Pelicula')
    clasificacion = fields.Selection(selection=[
        ('G', 'G'), # Público General
        ('PG','PG'), # Se recomienda en compañia de un adulto
        ('PG-13', 'PG-13'), # Mayores de 13
        ('R', 'R'), # En compañia de un adulto obligatorio
        ('NC-17', 'NC-17'), # Mayores de 18
    ], string='Clasificación')

    fch_estreno = fields.Date(string='Fecha de Estreno')
    puntuacion = fields.Integer(string='Puntuación')
    active = fields.Boolean(string='Activo', default=True)
    director_id = fields.Many2one(
        comodel_name = 'res.partner',
        string='Director'
    )
    
    genero_ids = fields.Many2many(
        comodel_name = 'genero',
        string='Generos'
    )
    vista_general = fields.Text(string='Descripción')
    link_trailer = fields.Char(string='Trailer')
    es_libro=fields.Boolean(string='Verisión libro')
    libro= fields.Binary(string='Libro')
