# _*_ coding: utf-8  _*_

from odoo import fields, models, api


class Genero(models.Model):
    
    _name = "genero"

    name = fields.Char(string='Género')