# _*_ coding: utf-8  _*_

from odoo import fields, models, api

class Updatewizard(models.TransientModel):
    
    _name = "update.wizard"

    name = fields.Text(string='Nueva Descripcion')

    def update_vista_general(self):
        # self.env para saltar a presupuesto
        presupuesto_obj = self.env['presupuesto']
        #la busqueda de de lo que hace el selft lo hizo con el debug en pycharm
        #de alli sale _context
        presupuesto_id = presupuesto_obj.search([('id','=',self._context['active_id'])])
        #presupuesto_id= presupuesto_obj.browse(self._context['active_id'=])
        
        presupuesto_id.vista_general = self.name