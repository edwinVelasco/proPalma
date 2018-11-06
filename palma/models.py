from django.db import models
import datetime

# Create your models here.

class Tipo_Documento(models.Model):
    tipo = models.CharField(max_length=20)
    def __unicode__(self):
        return '%s' %(self.id)


class Departamento(models.Model):
    nombre = models.CharField(max_length=45)
    def __unicode__(self):
        return '%s' %(self.id)

class Municipio(models.Model):
    nombre = models.CharField(max_length=45)
    departamento = models.ForeignKey('Departamento')

    def __unicode__(self):
        return '%s+%s' %(self.id, self.departamento)

class Palmicultor(models.Model):
    nombres = models.CharField(max_length=45)#
    cedula_palmera = models.CharField(max_length=15)#
    apellidos = models.CharField(max_length=45)#
    tipo_documento = models.ForeignKey('Tipo_Documento')#
    documento = models.CharField(max_length=15, unique=True)#
    municipio = models.ForeignKey('Municipio')#
    genero = models.CharField(max_length=1)#

    '''
        masculino --> 1
        femenino --> 2
    '''
    direccion = models.CharField(max_length=45)#
    telefono = models.CharField(max_length=45)
    email = models.EmailField(max_length=60)#
    zona_palmera = models.EmailField(max_length=20)#
    activo = models.CharField(max_length=1) #activo -->1 inactivo --> 2

    def __unicode__(self):
        return '%s, %s, %s, %s' %(self.nombres, self.apellidos, self.email, self.documento)

class Usuario(models.Model):
    documento = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=32)
    tipo = models.CharField(max_length=1)

    '''
        1 --> admin
        2 --> palmicultor
    '''
    activo = models.CharField(max_length=1) #activo -->1 inactivo --> 2
    def __unicode__(self):
        return '%s, %s' %(self.documento, self.tipo)

class Hacienda(models.Model):
    nombre = models.CharField(max_length=45, unique=True)
    direccion = models.CharField(max_length=45)
    cedula_catastral = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=45)
    area_total = models.IntegerField()
    descripcion  = models.TextField()
    nucleo_palmero = models.CharField(max_length=45)
    palmicultor = models.ForeignKey('Palmicultor')
    municipio = models.ForeignKey('Municipio')
    activo = models.CharField(max_length=1) #activo -->1 inactivo --> 0

    def __unicode__(self):
        return '%s, %s, %s, %s' %(self.nombre, self.direccion, self.telefono, self.palmicultor)

class Zona(models.Model):
    area = models.IntegerField()
    hacienda = models.ForeignKey('Hacienda')
    capacidad_palma = models.IntegerField()
    fecha_creacion = models.DateField(auto_now=True)
    fecha_plantacion = models.DateField(auto_now=False)
    codigo = models.CharField(max_length=45)
    activo = models.CharField(max_length=1, default='0')
    #activo --> 0 inactivo --> 1


class Enmienda(models.Model):
    enmienda = models.CharField(max_length=45, unique=True)
    fechaCreacion = models.DateTimeField(auto_now=True)
    usuarioCreador = models.ForeignKey('Usuario')
    def __unicode__(self):
        return '%s' %(self.id)

class Unidad(models.Model):
    tipo = models.CharField(max_length=1)
    unidad = models.CharField(max_length=40, unique=True)
    fechaCreacion = models.DateTimeField('Fecha de creacion')
    usuarioCreador = models.ForeignKey('Usuario')

    '''
    Peso --> p
    Tiempo --> t
    unidad --> u
    '''

    def __unicode__(self):
        return '%s' %(self.id)

class Correcion_Suelo(models.Model):
    area_aplicada = models.IntegerField()
    fechaRegistro = models.DateTimeField(auto_now=True)
    fecha_aplicada = models.DateField()
    cantidad = models.FloatField()
    precio_enmienda = models.FloatField()
    precio_aplicadaEnmienda = models.FloatField()
    subtotal = models.FloatField()
    enmienda = models.ForeignKey('Enmienda')
    unidad = models.ForeignKey('Unidad')
    lote = models.ForeignKey('Zona')

####

class Fertilizantes(models.Model):
    fertilizante = models.CharField(max_length=45, unique=True)
    fecha_registro = models.DateTimeField(auto_now=True)
    usuarioCreador = models.ForeignKey('Usuario')

    def __unicode__(self):
        return '%s' %(self.id)

class Nivelacion_Nutrientes(models.Model):
    area_lote = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now=True)
    fecha_aplicacion = models.DateField()
    cantidad = models.FloatField()
    precio_nutriente = models.FloatField()
    precio_aplicacion = models.FloatField()
    subtotal = models.FloatField()
    lote = models.ForeignKey('Zona')
    unidad = models.ForeignKey('Unidad')
    fertilizantes = models.ForeignKey('Fertilizantes')

class Insumos(models.Model):
    insumo = models.CharField(max_length=45, unique=True)
    fecha_registro = models.DateTimeField(auto_now=True)
    usuarioCreador = models.ForeignKey('Usuario')
    tipo = models.CharField(max_length=1)

    '''
        Insumo coberturas --> 0 costos de coberturas
        Insumo Variedad de Palma --> 1  palma para la siembra
    '''

    def __unicode__(self):
        return '%s' %(self.id)

class Siembra_Cobertura(models.Model):
    area_lote = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now=True)
    fecha_siembra = models.DateField()
    cantidad = models.FloatField()
    precio_unidad = models.FloatField()
    subtotal = models.FloatField()
    lote = models.ForeignKey('Zona')
    unidad = models.ForeignKey('Unidad')
    insumo = models.ForeignKey('Insumos')

class Labor(models.Model):
    labor = models.CharField(max_length=70, unique=True)
    tipo = models.CharField(max_length=1)
    '''
        tipo 0 --> metro lineal
        tipo 1 --> area
        tipo 2 --> siembra palma
        tipo 3 --> otros ce
    '''
    fecha_registro = models.DateTimeField(auto_now=True)
    usuarioCreador = models.ForeignKey('Usuario')

    def __unicode__(self):
        return '%s' %(self.id)

class Preparacion_Suelo(models.Model):
    fecha_registro = models.DateTimeField(auto_now=True)
    fecha_preparacion = models.DateField()
    lote = models.ForeignKey('Zona')
    labor = models.ForeignKey('Labor')
    tipoMedida = models.CharField(max_length=1)#
    '''
        area --> 1
        metro lineal --> 0
    '''

    area_lote = models.IntegerField()
    precio = models.FloatField()
    subtotal = models.FloatField()



class Palma_Siembra(models.Model):
    fecha_registro = models.DateTimeField(auto_now=True)
    fecha_siembra = models.DateField()
    cantidad_plantulas = models.IntegerField()
    precio = models.FloatField()
    area = models.FloatField()
    subtotal = models.FloatField()
    lote = models.ForeignKey('Zona')
    tipo = models.ForeignKey('Insumos')
    unidad = models.ForeignKey('Unidad')

class Item(models.Model):
    item = models.CharField(max_length=55, unique=True)
    fecha_registro = models.DateTimeField(auto_now=True)
    usuarioCreador = models.ForeignKey('Usuario')

    def __unicode__(self):
        return '%s' %(self.id)

class Labor_Siembra(models.Model):
    area_labor = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now=True)
    fecha_labor = models.DateField()
    cantidad_laboradas = models.FloatField() #depende de la unidad
    precio_labor = models.FloatField()
    subtotal = models.FloatField()
    lote = models.ForeignKey('Zona')
    labor = models.ForeignKey('Labor')
    unidad = models.ForeignKey('Unidad')

class Otro_ce(models.Model):
    fecha_registro = models.DateTimeField(auto_now=True)
    fecha_actividad = models.DateField()
    area = models.FloatField()
    cantidad = models.FloatField()
    precio = models.FloatField()
    subtotal = models.FloatField()
    lote = models.ForeignKey('Zona')
    unidad = models.ForeignKey('Unidad')
    labor = models.ForeignKey('Labor')