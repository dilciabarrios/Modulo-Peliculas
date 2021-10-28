# _*_ coding: utf-8  _*_

from io import StringIO
import logging

from odoo import fields, models, api

#UserError para poder manejar mensajes de errores a traves de ventanas emergentes
from odoo.exceptions import UserError 

logger = logging.getLogger(__name__)

class Presupuesto(models.Model):
    
    _name = "presupuesto"
    _inherit= ['mail.thread','mail.activity.mixin','image.mixin']
    
    @api.depends('detalles_ids') #con esto le estamos diciendo que la funcion compute depende de ese campo
    # se va a ejecutar cada vez que se renderice la vista o cada vez que se modifique elementos de detalles_ids 
    def _compute_total(self):
    #ciclo for record para que procese varios registros a la vez y no 
    #salte un mensaje de error, porque sino le pongo el ciclo for
    #self tiene que leer los registros uno a uno y como va a recibir varios
    #dara mensaje de error
        for record in self:
            sub_total= 0
            for linea in record.detalles_ids:
                sub_total += linea.importe
            record.base = sub_total
            record.impuestos = sub_total * 0.16
            record.total = sub_total * 1.16
            

    name = fields.Char(string='Pelicula')
    clasificacion = fields.Selection(selection=[
        ('G', 'G'), # Público General
        ('PG','PG'), # Se recomienda en compañia de un adulto
        ('PG-13', 'PG-13'), # Mayores de 13
        ('R', 'R'), # En compañia de un adulto obligatorio
        ('NC-17', 'NC-17'), # Mayores de 18
    ], string='Clasificación')

    dsc_clasificacion = fields.Char(string= 'Descripcion Clasificacion')

    fch_estreno = fields.Date(string='Fecha de Estreno')
    puntuacion = fields.Integer(string='Puntuación', related="puntuacion2")
    puntuacion2 = fields.Integer(string='Puntuación2')
    active = fields.Boolean(string='Activo', default=True)
    director_id = fields.Many2one(
        comodel_name = 'res.partner',
        string='Director'
    )
    
    categoria_director_id = fields.Many2one(
        comodel_name = 'res.partner.category',
        string = 'Categoria de Director',
    
        # segunda version
        # de esta forma apunto a la categoria por su id y no por nombre
        # ya que si apunto al nombre si alguien modifica el registro  el nombre de la categoria no
        # se ve afectado la tabla 
        # peliculas.category_director (se le llama external id ), env.ref para poder apuntar a la categoria que deseo
        # defult lambda self (cuando voy a utilizar un función corta)
        default=lambda self: self.env.ref('peliculas.category_director')

        # primera version
        # default=lambda self: self.env['res.partner.category'].search([('name', '=','Director')])
    )
    # genero_ids:permite elegir muchos registros de una sola vez en lugar de agregarlos de uno.
    genero_ids = fields.Many2many(
        comodel_name = 'genero',
        string='Generos'
    )
    vista_general = fields.Text(string='Descripción')
    link_trailer = fields.Char(string='Trailer')
    es_libro=fields.Boolean(string='Verisión libro')
    libro= fields.Binary(string='Libro')
    libro_filename = fields.Char(string="Nombre del libro")

    # copy=False para que cuando duplique un registro no se duplique el estado de un registro
    # y por defecto pongo que el estado es borrador siempre 
    state= fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado'),
    ], default='borrador', sring='Estados', copy=False)

    #para que me arroje fecha y hora en en sistema
    fch_aprobado = fields.Datetime(string='Fecha Aprobado', copy=False)
    num_presupuesto = fields.Char(string='Número presupuesto', copy=False)
    fch_creacion = fields.Datetime(string='Fecha Creación', copy=False, default=lambda self: fields.Datetime.now())
    #varias actores pueden estar asociados a diferentes presupuestos
    actor_ids = fields.Many2many(
        comodel_name = 'res.partner',
        string='Actores'
    )
    # categoria_actor_id: permite elegir un componente perteneciente al modelo relacionado
    categoria_actor_id = fields.Many2one(
        comodel_name = 'res.partner.category',
        string = 'Categoria Actor',
        default=lambda self: self.env.ref('peliculas.category_actor')
    )
    
    opinion = fields.Html (string='Opinion')

    # de esta forma relaciona detalles presupuesto con presupuesto
    detalles_ids = fields.One2many(
        comodel_name='presupuesto.detalle',
        # inverse_name esta esperando el nombre de la varible que se relaciona con la cabecera 
        # cabecera es presupuesto
        inverse_name='presupuesto_id',
        string='Detalles'
    )
    campos_ocultos=fields.Boolean(string='Campos Ocultos')


    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        # leer el valor que tiene configurada la compañia (le estoy asignando el id que tiene configurado en currency_id de la compañia)
        # especifico nombre de la tabla
        default=lambda self: self.env.company.currency_id.id
    )

    #compute es una funcion: ningun calculo de estos se guarda en base en datos
    #si por alguna razon necesito guardarlo base de datos coloco "store=True"
    #cada vez que odoo renderiza una vista se inicia la funcion y hace el calculo en 
    #en ese momento

    terminos= fields.Text(string='Términos')
    base= fields.Monetary(string='Base Imponible', compute='_compute_total')
    impuestos=  fields.Monetary(string='Impuestos',compute='_compute_total')
    total= fields.Monetary(string='Total', compute='_compute_total')

    def aprobar_presupuesto(self):
        logger.info('***Entro a la función Aprobar Presupuesto')
        #colocando el self. estoy apuntando a la variable state de 
        #lo contrario no estaria apuntando a esa varible
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()
        #ejemplos
        #logger.info('Hola mundo')
        #logger.warning('Hola mundo')
        #logger.error('Hola mundo')
    
    def cancelar_presupuesto(self):
        self.state = 'cancelado'

    #funcion para eliminar o suprimir, hacemos llamado a la funcion original de odoo por eso usamos "super"
    #primer parametro (nombre de la class), segundo parametro self
    def unlink(self):
        for record in self:
            if record.state != 'cancelado':
                raise UserError ('No se encuentra en el estado cancelado por la tanto no se puede eliminar')
            #el UserError me funciona como un break todo lo que se encuentre debajo de el no se 
            #va a ejecutar
            super(Presupuesto, record).unlink()
            
        
    # decorador siempre debe ir definda con la funcion create
    @api.model 
    # en variables le paso nombre de la data como por ejemplo nombre de la pelicula,
    # la clasificacion entre otros
    # nuestra funcion lee absolutamente todas las variables 
    # los campos vacios se guardan como False
    def create(self, variables):
        logger.info('variables'.format(variables))
        # self.env['ir.sequence'] para hacer salto de nuestro modulo presupuesto a secuencia
        sequence_obj= self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.presupuesto.pelicula')
        variables['num_presupuesto']= correlativo
        return super (Presupuesto,self).create(variables)


    # funcion cuando edito un registro que se dispara es write
    # el write solo le llegan las variables que se editan no como el create
    def write(self,variables):
        logger.info('variables'.format(variables))
        if 'clasificacion' in variables:
            raise UserError('La clasificacion no se puede editar')
        return super (Presupuesto,self).write(variables)

    # funcion que duplica un registro
    # siempre va a ser defaul=None
    
    def copy(self, default=None):
        # definimos que sea un diccionario sino le llega nada que sea un diccionario vacio
        default = dict(default or {})
        # puedo definir tantas variables como deseo editar
                         # se va agregar nombre + palabra copia
        default['name']= self.name + '(Copia)'
        # para que cambia el valor de la puntacion a 1
        default['puntuacion2']= 1

        return super(Presupuesto, self).copy(default)

    # funcion onchange atributo dispara el momento en que se cambia el valor del elemento.
    @api.onchange('clasificacion')
    # def _onchange_clasificacion(no es obligatorio colocar ese nombre es simplemente es un estandar
    def _onchange_clasificacion(self):
        #  if self.clasificacion: si es que existe clasificacion entonces evalua
        if self.clasificacion:
            if self.clasificacion == 'G':
                self.dsc_clasificacion = 'Público General'
            if self.clasificacion == 'PG':
                self.dsc_clasificacion = 'Se recomienda en compañia de un adulto'
            if self.clasificacion == 'PG-13':
                self.dsc_clasificacion = 'Mayores de 13'
            if self.clasificacion == 'R':
                self.dsc_clasificacion = 'En compañia de un adulto obligatorio'
            if self.clasificacion == 'NC-17':
                self.dsc_clasificacion = 'Mayores de 18'
        else:
            self.dsc_clasificacion = False
            

class PresupuestoDetalle(models.Model):

    _name = "presupuesto.detalle"

    # Many2one: muchos detalles pertenecen a una sola cabecera (presupuesto)
    # Many2one: presupuestos detalles van a pertenecer a un solo presupuesto

    presupuesto_id = fields.Many2one(
        comodel_name='presupuesto',
        string='Presupuesto',
    )

    name = fields.Many2one(
        comodel_name='recurso.cinematografico', 
        string='Recurso',
    )
    descripcion= fields.Char(string='Descripción', related='name.descripcion')
    contacto_id= fields.Many2one(
        comodel_name='res.partner',
        string='Contacto',
        related='name.contacto_id'
    ) 
    imagen= fields.Binary(string='Imagen', related='name.imagen')
    cantidad= fields.Float(string='Cantidad', default='1.0', digits=(16, 4))
    precio= fields.Float(string='Precio', digits='Product Price')
    importe= fields.Monetary(string='Importe')
    # para asignarle a un valor de tipo decimal el simbolo de la moneda es cambiarle el tipo de cambio
    # en el que esta definido por eso colocamos Monetary

    # currency_id (asi se debe llamar no se puede cambiar el nombre)lee el tipo de moneda seleccionado y colocarle el simbolo que tiene registrado en sistema
    
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string = 'Moneda',
        # related='presupuesto_id.currency_id' para que me seleccione por defecto la moneda
        # seleccionada en la cabecera presupuesto
        related='presupuesto_id.currency_id'
    )

    @api.onchange('name')
    def _onchange_name(self):
        #cuando un campo esta vacio odoo lo trata como si fuera un booleano
        if self.name:
            # para hacer salto de presupuesto a recurso cinematografico ya que la variable precio se encuentra alli
            self.precio = self.name.precio
  
    @api.onchange('cantidad', 'precio')
    def _onchange_importe(self):
        self.importe = self.cantidad * self.precio