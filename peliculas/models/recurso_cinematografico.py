# _*_ coding: utf-8  _*_


from odoo import fields, models, api

class RecuersoCinematografico(models.Model):
    _name = "recurso.cinematografico"

    name = fields.Char(string='Recurso')
    descripcion = fields.Char(string='Descripción')
    precio = fields.Float(string='Precio')
    contacto_id = fields.Many2one(
        comodel_name='res.partner',
        # para filtrar solo los marcados como indiviual y no como 
        # compañia "[('is_company', '=', False)]"
        domain ="[('is_company', '=', False)]"
    )
    imagen = fields.Binary(string='Imagen')