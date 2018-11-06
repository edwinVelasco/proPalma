# -*- coding: utf-8 -*-
from encodings.utf_8 import encode
from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse, Http404, HttpResponseRedirect
from models import Palmicultor, Tipo_Documento, Municipio, Departamento, Hacienda, Usuario, Zona, Enmienda, Correcion_Suelo, Unidad, Fertilizantes, Nivelacion_Nutrientes, Labor, Preparacion_Suelo, Insumos, Siembra_Cobertura, Item, Palma_Siembra, Otro_ce, Labor_Siembra
from django.db import IntegrityError
import hashlib
from django.core.mail import EmailMessage
import datetime
# Create your views here.

def index(request):
    return render(request, 'index.html')

def contacto(request):
    if request.method == 'POST':
        titulo = 'mensaje de prueba propalma'
        contenido = '\n mensaje enviado por: ProPalma'
        contenido += '\n nombre: Edwin velasco \n email: djsdjshd.gmail.com'
        correo = EmailMessage(titulo, contenido, to= ['edwinalbertovelasco8@outlook.com'])
        try:
            correo.send()
            #except gaiError:
            return HttpResponse(' mensaje enviado satisfactoriamente')
        except Exception, e:
            html = '<html><body>hay un error de typo %s con excepcion %s</body></html>'%(e, Exception)
            return HttpResponse(html)
    else:
        return HttpResponse(u'enviado satisfactoriamente')

def zona_session(request):
    if request.method == 'GET':
        if 'zona' in request.GET:
            request.session['zona'] = request.GET['zona']
            return HttpResponse('ok')

def zona(request):
    if 'usuario' in request.session and 'nombre' in request.session and 'tipo' in request.session and 'zona' in request.session:
        usuario = Usuario.objects.get(documento = request.session['usuario'])
        if usuario.tipo == '2':
            return render(request, 'zona.html', {'nombre':request.session['nombre']})
        else:
            return redirect('/login')
    else:
        return redirect('/')

#-----------------Crud palmicultor-----------------

def add_palmicultor(request):
    if request.method == 'POST':
        try:
            palmicultor = Palmicultor()
            palmicultor.nombres = request.POST['nombres']
            palmicultor.apellidos = request.POST['apellidos']
            palmicultor.email = request.POST['email']
            palmicultor.cedula_palmera = request.POST['cedula_palmera']
            palmicultor.zona_palmera = request.POST['zona']

            if request.POST['tipoDocumento'] == '0' or request.POST['tipoDocumento'] == 0:
                return HttpResponse('mal')
            tipo_documento = Tipo_Documento.objects.get(id=request.POST['tipoDocumento'])

            palmicultor.tipo_documento =tipo_documento

            palmicultor.documento = request.POST['numDocumento']

            if request.POST['genero'] == '0' or request.POST['genero'] == 0:
                return HttpResponse('mal')
            palmicultor.genero = request.POST['genero']

            palmicultor.direccion = request.POST['direccionResidencia']
            palmicultor.telefono = request.POST['telefono']

            municipio = Municipio.objects.get(id=request.POST['municipio'])
            palmicultor.activo = '1'
            palmicultor.municipio = municipio

            usuario = Usuario()
            usuario.documento = request.POST['numDocumento']
            usuario.password = pasar_md5(request.POST['numDocumento'])
            usuario.tipo = '2'
            usuario.activo= '1'

            palmicultor.save()
            usuario.save()
            return HttpResponse('ok')

        except Tipo_Documento.DoesNotExist:
            return HttpResponse('tipo_documento')#no hay un tipo_documento valido
        except Municipio.DoesNotExist:
            return HttpResponse('municipio')#no esta registrado el municipio
        except IntegrityError:
            return HttpResponse('documento')#significa que el documento ya fue registrado
    else:
        return Http404

def editar_palmicultor(request):
    if request.method == 'POST':
        try:
            palmicultor = Palmicultor.objects.get(documento=request.session['usuario'])
            palmicultor.email = request.POST['email']

            palmicultor.zona_palmera = request.POST['zona']
            palmicultor.cedula_palmera = request.POST['cedula_palmera']

            palmicultor.direccion = request.POST['direccionResidencia']
            palmicultor.telefono = request.POST['telefono']

            municipio = Municipio.objects.get(id=request.POST['municipio'])
            palmicultor.municipio = municipio

            palmicultor.save()
            return HttpResponse('ok')

        except Tipo_Documento.DoesNotExist:
            return HttpResponse('tipo_documento')#no hay un tipo_documento valido
        except Municipio.DoesNotExist:
            return HttpResponse('municipio')#no esta registrado el municipio
        except IntegrityError:
            return HttpResponse('documento')#significa que el documento ya fue registrado
    else:
        return Http404

def editar_palmicultor_admin(request):
    if request.method == 'POST':
        try:
            palmicultor = Palmicultor.objects.get(id=request.POST['id'])

            palmicultor.nombres = request.POST['nombres']
            palmicultor.apellidos = request.POST['apellidos']
            palmicultor.cedula_palmera = request.POST['cedula_palmera']
            tipo_documento = Tipo_Documento.objects.get(id=request.POST['tipoDocumento'])
            palmicultor.tipo_documento = tipo_documento
            usuario = Usuario.objects.get(documento=palmicultor.documento)
            palmicultor.documento = request.POST['numDocumento']
            usuario.documento = request.POST['numDocumento']
            usuario.save()
            palmicultor.save()
            return HttpResponse('ok')
        except Palmicultor.DoesNotExist:
            return HttpResponse('pal')
        except Tipo_Documento.DoesNotExist:
            return HttpResponse('tipo')
        except Usuario.DoesNotExist:
            return HttpResponse('usuario')
        except IntegrityError:
            return HttpResponse('documento')#significa que el documento ya fue registrado

def reset_pass(request):
    if request.method == 'GET':
        try:
            palmicultor = Palmicultor.objects.get(id=request.GET['id'])
            password = pasar_md5(palmicultor.documento)
            usuario = Usuario.objects.get(documento=palmicultor.documento)
            usuario.password = password
            usuario.save()
            return HttpResponse('ok')
        except Palmicultor.DoesNotExist:
            return HttpResponse('pal')
        except Usuario.DoesNotExist:
            return HttpResponse('usuario')

def get_palmicultor_admin(request):
    try:
        palmicultor = Palmicultor.objects.get(id=request.GET['id'])
        salida = '%s,%s,%s,%s,%s' %(palmicultor.nombres, palmicultor.apellidos, palmicultor.cedula_palmera, palmicultor.tipo_documento, palmicultor.documento)
        return HttpResponse(salida)
    except Palmicultor.DoesNotExist:
        return HttpResponse('no existe')

def get_palmicultor_sesion(request):
    try:
        palmicultor = Palmicultor.objects.get(documento=request.session['usuario'])
        salida = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %(palmicultor.nombres, palmicultor.apellidos, palmicultor.email, palmicultor.tipo_documento, palmicultor.documento, palmicultor.genero, palmicultor.municipio, palmicultor.direccion, palmicultor.telefono, palmicultor.cedula_palmera)
        return HttpResponse(salida)
    except Palmicultor.DoesNotExist:
        return HttpResponse('no existe')

def get_palmicultores(request):
    if request.method == 'GET':
        palmicultores = Palmicultor.objects.all().order_by('apellidos')
        data = serializers.serialize('json', palmicultores, fields=('apellidos', 'nombres', 'documento', 'email', 'telefono', 'activo', 'cedula_palmera'))
        return HttpResponse(data, mimetype='application/json')
    else:
        return Http404

def activar_desactivar(request):
    if request.method == 'GET':
        if 'id' in request.GET:
            palmucultor = Palmicultor.objects.get(id=request.GET['id'])
            usuario = Usuario.objects.get(documento=palmucultor.documento)
            salida = '2'
            if palmucultor.activo == '1':
                palmucultor.activo = '2'
                usuario.activo = '2'
            else:
                palmucultor.activo = '1'
                usuario.activo = '1'
                salida = '1'

            palmucultor.save()
            usuario.save()
            return HttpResponse(salida)
    else:
        return Http404

def desactivar_palmicultor(request):
    if request.method == 'GET':
        palmicultor = Palmicultor.objects.get(documento=request.session['usuario'])
        usuario = Usuario.objects.get(documento=palmicultor.documento)
        palmicultor.activo = '2'
        usuario.activo = '2'
        palmicultor.save()
        usuario.save()
        return HttpResponse('ok')
    else:
        return Http404

def revicion_pass(request):
    usuario = Usuario.objects.get(documento= request.session['usuario'])
    if usuario.password == pasar_md5(usuario.documento):
        return HttpResponse('=')
    else:
        return HttpResponse('ok')

def pedir_documento(request):
    if 'documento' in request.POST:
        try:
            palmicultor = Palmicultor.objects.get(documento=request.POST['documento'])
            if palmicultor.activo == '2':
                return HttpResponse('inactivo')
            titulo = 'PROPALMA, RECUPERACION DE CUENTA'
            dia = datetime.datetime.now()
            password = int(palmicultor.documento)/dia.day*dia.month*dia.hour
            contenido = '\n Su cuenta a sido recuperada con exito. \n Recuerde que ahora estos son sus datos de usuario'
            contenido += '\n User: %s \n Password: %s' %(palmicultor.documento, password)
            usuario = Usuario.objects.get(documento=palmicultor.documento)
            usuario.password = pasar_md5(str(password))
            usuario.save()

            correo = EmailMessage(titulo, contenido, to=[palmicultor.email])
            #correo = EmailMessage(titulo, contenido, to=['edwinalbertovelasco8@outlook.com'])
            try:
                correo.send()
                #except gaiError:
                return HttpResponse('ok')
            except Exception, e:
                html = '<html><body>hay un error de typo %s con excepcion %s</body></html>'%(e, Exception)
                return HttpResponse(html)
        except Palmicultor.DoesNotExist:
            return HttpResponse('not')

def recuperar_password(request):
    if request.method == 'POST':
        if 'new1' in request.POST and 'new2' in request.POST and 'id' in request.POST:
            if request.POST['new2'] == request.POST['new1']:
                usuario = Usuario.objects.get(documento=request.POST['id'])
                usuario.password = pasar_md5(request.POST['new1'])
                usuario.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('new')#no son iguales
        else:
            return HttpResponse('error')

def get_palmicultores_filtro_admin(request):
    if request.GET['nombre'] != '':
        #palmicultores = Palmicultor.objects.filter(nombres__contains=request.GET['nombre']) distingue mayusculas
        palmicultores = Palmicultor.objects.filter(nombres__icontains=request.GET['nombre']) #no distingue mayusculas

    elif request.GET['apellido'] != '':
        palmicultores = Palmicultor.objects.filter(apellidos__icontains=request.GET['apellido']) #no distingue mayusculas

    elif request.GET['documento'] != '':
        palmicultores = Palmicultor.objects.filter(documento__startswith=request.GET['documento']).order_by('apellidos')

    elif request.GET['hacienda'] != '':
        palmicultores = Palmicultor.objects.filter(hacienda__nombre__icontains=request.GET['hacienda']).order_by('apellidos')

    elif request.GET['departamento'] != '0':
        if request.GET['municipio'] != '0':
            palmicultores = Palmicultor.objects.filter(municipio=Municipio.objects.get(id=request.GET['municipio'])).order_by('apellidos')
        else:
            palmicultores = Palmicultor.objects.filter(municipio__departamento__exact=Departamento.objects.get(id=request.GET['departamento'])).order_by('apellidos')

    else:
        palmicultores = Palmicultor.objects.order_by('apellidos')


    data = serializers.serialize('json', palmicultores, fields=('apellidos', 'nombres', 'documento', 'email', 'telefono', 'activo', 'cedula_palmera'))
    return HttpResponse(data, mimetype='application/json')

#-----------------fin crud palmicultor------------

def get_departamentos(request):
    departamentos = Departamento.objects.all()
    data = serializers.serialize('json', departamentos, fields=('nombre'))
    return HttpResponse(data, mimetype='application/json')

def get_municipios(request):#busca los municipios de un departamento enviado en el request
    dep = Departamento.objects.get(id= request.GET['departamento'])

    municipio = Municipio.objects.filter(departamento=dep)
    data = serializers.serialize('json', municipio, fields=('nombre'))
    return HttpResponse(data, mimetype='application/json')

def get_tipos_documento(request):
    tipos = Tipo_Documento.objects.all()
    data = serializers.serialize('json', tipos, fields=('tipo'))
    return HttpResponse(data, mimetype='application/json')

def pasar_md5(cadena):
    m = hashlib.md5()
    m.update(cadena.encode('utf-8'))
    return m.hexdigest()
    #md5 es de 32 caracteres

def restaurar_pass(request):# restaura la contraseña de un usuario palmicultor
    if request.method == 'GET':
        try:
            usuario = Usuario.objects.get(id=request.GET['id'])
            usuario.password = pasar_md5(usuario.documento)
            usuario.save()
            return HttpResponse('ok') #todo bello, pass restaurada
        except Usuario.DoesNotExist:
            return HttpResponse('not') #usuario no encontrado

    else:
        return Http404

def login(request):
    if 'usuario' in request.session and 'nombre' in request.session and 'tipo' in request.session:
        if request.session['tipo'] == '2':
            return render(request, 'palmicultor.html', {'nombre':request.session['nombre']})
        else:
            return render(request, 'admin.html', {'nombre':request.session['nombre']})
    else:
        return Http404

def loguear(request):
    if request.method == 'POST':
        if 'password' in request.POST and 'documento' in request.POST:
            try:
                usuario = Usuario.objects.get(documento = request.POST['documento'])
                if pasar_md5(request.POST['password']) == usuario.password:
                    if usuario.activo == '1':
                        if usuario.tipo == '2': #palmicultor
                            request.session['usuario'] = request.POST['documento']
                            pal = Palmicultor.objects.get(documento=request.POST['documento'])
                            request.session['nombre'] = pal.nombres
                            request.session['tipo'] = '2'
                        else:#admin --> 1
                            request.session['usuario'] = request.POST['documento']
                            request.session['nombre'] = request.POST['documento']
                            request.session['tipo'] = '1'

                        return HttpResponse('ok')
                    else:
                        return HttpResponse('inactivo')#Usuario inactivo XD
                else:
                    return HttpResponse('password')#password incorrecta XD


            except Usuario.DoesNotExist:
                return HttpResponse('not user')
    else:
        return Http404

def logout(request):
    if 'usuario' in request.session and 'nombre' in request.session and 'tipo' in request.session:
        del request.session['usuario']
        del request.session['nombre']
        del request.session['tipo']
        return HttpResponse('ok')
    else:
        return Http404

def editar_password(request):
    if request.method == 'POST':
        if 'password' in request.POST and 'new1' in request.POST and 'new2' in request.POST:
            usuario = Usuario.objects.get(documento=request.session['usuario'])
            password = pasar_md5(request.POST['password'])
            if password == usuario.password:
                if request.POST['new1'] == request.POST['new2']:
                    usuario.password = pasar_md5(request.POST['new1'])
                    usuario.save()
                    return HttpResponse('ok')
                else:
                    return HttpResponse('new')
            else:
                return HttpResponse('password')
    else:
        return Http404
#--------- crud Haciendas-------------

#retorna en un json las haciendas del palmicultor que esta logueado
def get_haciendas(request):
    palmicultor = Palmicultor.objects.get(documento=request.session['usuario'])
    ha = Hacienda.objects.filter(palmicultor=palmicultor)
    data = serializers.serialize('json', ha, fields=('nombre', 'direccion', 'telefono', 'area_total', 'nucleo_palmero', 'activo'))
    return HttpResponse(data, mimetype='application/json')

def add_hacienda(request):
    if request.method == 'POST':
        try:
            palmicultor = Palmicultor.objects.get(documento=request.session['usuario'])
            hacienda = Hacienda()
            hacienda.palmicultor = palmicultor
            hacienda.nombre = request.POST['nombre']
            hacienda.cedula_catastral = request.POST['cedula']

            hacienda.municipio = Municipio.objects.get(id=request.POST['municipio'])

            hacienda.direccion = request.POST['direccion']
            hacienda.telefono = request.POST['telefono']
            hacienda.nucleo_palmero = request.POST['nucleo']
            hacienda.area_total = request.POST['area']
            hacienda.descripcion = request.POST['descripcion']
            hacienda.activo = '1'
            hacienda.save()

            return HttpResponse('ok')
        except Palmicultor.DoesNotExist:
            return HttpResponse('not')
        except Municipio.DoesNotExist:
            return HttpResponse('muni')
        except IntegrityError:
            return HttpResponse('error')
    else:
        return Http404

def editar_hacienda(request):
    if request.method == 'POST':
        try:
            hacienda = Hacienda.objects.get(id = request.POST['id'])
            hacienda.nombre = request.POST['nombre']
            hacienda.municipio = Municipio.objects.get(id=request.POST['municipio'])

            hacienda.direccion = request.POST['direccion']
            hacienda.telefono = request.POST['telefono']
            hacienda.nucleo_palmero = request.POST['nucleo']
            hacienda.area_total = request.POST['area']
            hacienda.descripcion = request.POST['descripcion']
            hacienda.cedula_catastral = request.POST['cedula']

            if 'activo' in request.POST:
                hacienda.activo = '1'
            else:
                hacienda.activo = '0'

            hacienda.save()

            return HttpResponse('ok')
        except Hacienda.DoesNotExist:
            pass
        except IntegrityError:
            return HttpResponse('ya')

    else:
        return Http404

def get_hacienda(request):
    if request.method == 'GET':
        hacienda = Hacienda.objects.get(id=request.GET['id'])
        salida = '%s,%s,%s,%s,%s,%s,%s,%s,%s' %(hacienda.nombre, hacienda.municipio, hacienda.direccion, hacienda.nucleo_palmero, hacienda.area_total, hacienda.descripcion, hacienda.activo, hacienda.cedula_catastral, hacienda.telefono)
        return HttpResponse(salida)
    else:
        return Http404

#--------- fin crud Haciendas-------------


#--------- crud Zonas/Lotes --------------
def add_zona(request):
    if request.method == 'POST':
        if 'area' in request.POST and 'capacidad' in request.POST and 'codigo' in request.POST and 'fecha' in request.POST and 'id' in request.POST:
            hacienda = Hacienda.objects.get(id = request.POST['id'])
            zonas = Zona.objects.filter(hacienda=hacienda)
            salida = False
            total_area = 0
            for zona in zonas:
                if zona.codigo == request.POST['codigo']:
                    return HttpResponse('ya,1')
                if zona.activo == '0':
                    total_area += zona.area

            area = int(request.POST['area'])
            print(total_area, 'antes')
            total_area += area
            if hacienda.area_total >= total_area:#bn
                try:
                    zona = Zona()
                    zona.hacienda = hacienda
                    zona.area = request.POST['area']
                    zona.capacidad_palma = request.POST['capacidad']
                    zona.codigo = request.POST['codigo']
                    zona.fecha_plantacion = request.POST['fecha']
                    zona.save()
                    salida = '%s,%s' %('ok', str(zona.hacienda.id))
                    return HttpResponse(salida)
                except IntegrityError:
                    return HttpResponse('error,1')
            else:
                total_area -= area
                salida = hacienda.area_total-total_area
                s = '%s,%s' %('otro', str(salida))
                return HttpResponse(s)
        else:
            return HttpResponseRedirect('logout')
    else:
        return Http404

#retorna todas las zonas de la hacienda seleccionada
def get_zonas(request):
    if 'id' in request.GET:
        hacienda = Hacienda.objects.get(id=request.GET['id'])
        zonas = Zona.objects.filter(hacienda=hacienda)
        data = serializers.serialize('json', zonas, fields=('codigo', 'area', 'capacidad_palma', 'fecha_plantacion', 'activo'))
        return HttpResponse(data, mimetype='application/json')
    else:
        return HttpResponse('error')

#retorna la hacienda deacuerdo al id para ser editada
def get_zona(request):
    if 'id' in request.GET:
        zona = Zona.objects.get(id=request.GET['id'])
        salida = '%s,%s,%s,%s,%s' %(zona.area, zona.capacidad_palma, zona.codigo, zona.fecha_plantacion, zona.activo)
        return HttpResponse(salida)

def editar_zona(request):
    #cambiar la forma en que se mira si el codigo ya fue guardado
    if request.method == 'POST':
        if 'area' in request.POST and 'capacidad' in request.POST and 'codigo' in request.POST and 'fecha' in request.POST and 'id' in request.POST:
            zona = Zona.objects.get(id=request.POST['id'])
            zonas = Zona.objects.filter(hacienda=zona.hacienda)
            total_area = 0
            for z in zonas:
                if z.codigo == request.POST['codigo']:
                    if z.id != zona.id:
                        return HttpResponse('ya,1')
                if z.activo == '0':
                    total_area += zona.area

            area = int(request.POST['area'])
            total_area -= zona.area
            total_area += area

            if zona.hacienda.area_total >= total_area:
                zona.area = request.POST['area']
                zona.capacidad_palma = request.POST['capacidad']
                zona.codigo = request.POST['codigo']
                zona.fecha_plantacion = request.POST['fecha']
                if 'activo' in request.POST:
                    zona.activo = '0'
                else:
                    zona.activo = '1'

                zona.save()
                salida = '%s,%s' %('ok', str(zona.hacienda.id))
                return HttpResponse(salida)
            else:
                total_area -= area
                #total_area += zona.area
                salida = zona.hacienda.area_total-total_area
                s = '%s,%s' %('otro', str(salida))
                return HttpResponse(s)
        else:
            return HttpResponseRedirect('logout')
    else:
        return Http404

#--------- fin crud Zonas/Lotes --------------



#--------- crud de enmiendas ----------------

def add_enmienda(request):
    if request.method == 'POST':
        if 'nombre' in request.POST:

            try:
                enmienda = Enmienda()
                enmienda.enmienda = request.POST['nombre']
                usuario = Usuario.objects.get(documento=request.session['usuario'])
                enmienda.usuarioCreador = usuario
                enmienda.save()
                return HttpResponse('ok')
            except Usuario.DoesNotExist:
                return HttpResponse('user')
            except IntegrityError:
                return HttpResponse('ya')
        else:
            return HttpResponse('nombre')

def get_enmiendas(request):
    enmiendas = Enmienda.objects.order_by('enmienda')
    data = serializers.serialize('json', enmiendas, fields=('enmienda'))
    return HttpResponse(data, mimetype='application/json')

def get_enmienda(request):
    if request.method == 'GET':
        enmienda = Enmienda.objects.get(id=request.GET['id'])
        salida = '%s' %(enmienda.enmienda)
        return HttpResponse(salida)

def editar_enmienda(request):
    if request.method == 'POST':
        if 'nombre' in request.POST and 'id' in request.POST:

            try:
                enmienda = Enmienda.objects.get(id = request.POST['id'])
                enmienda.enmienda = request.POST['nombre']
                enmienda.save()
                return HttpResponse('ok')
            except IntegrityError:
                return HttpResponse('ya')
        else:
            return HttpResponse('nombre')


#--------- fin del crud de enmienda----------

#------------ crud de correcion de suelos -----
def get_correciones(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        correciones = Correcion_Suelo.objects.filter(lote=zona)
        data = serializers.serialize('json', correciones, fields=('enmienda', 'cantidad', 'precio_enmienda', 'precio_aplicadaEnmienda', 'subtotal'))
        return HttpResponse(data, mimetype='application/json')

def add_correccion(request):
    if request.method == 'POST':
        if 'enmienda' in request.POST and 'cantidad' in request.POST and 'precio_en' in request.POST and 'precio_apli' in request.POST and 'unidad' in request.POST and 'area' in request.POST and 'fecha' in request.POST:

            if request.POST['enmienda'] == '0' or request.POST['enmienda'] == 0 or request.POST['unidad'] == '0' or request.POST['unidad'] == 0:
                return HttpResponse('error')
            try:

                zona = Zona.objects.get(id=request.session['zona'])
                correcion = Correcion_Suelo()
                correcion.enmienda = Enmienda.objects.get(id=request.POST['enmienda'])
                correcion.area_aplicada = request.POST['area']
                correcion.cantidad = request.POST['cantidad']
                correcion.fecha_aplicada = request.POST['fecha']
                correcion.unidad = Unidad.objects.get(id=request.POST['unidad'])
                correcion.lote = zona
                correcion.precio_aplicadaEnmienda = request.POST['precio_apli']
                correcion.precio_enmienda = request.POST['precio_en']
                correcion.subtotal = request.POST['subtotal']
                correcion.save()
                return HttpResponse('ok')
            except Enmienda.DoesNotExist:
                return HttpResponse('error')

            except Unidad.DoesNotExist:
                return HttpResponse('error')

            except Zona.DoesNotExist:
                return HttpResponse('zona')
        else:
            return HttpResponse('.l.')

def borrar_correccion(request):
    if 'id' in request.GET:
        correccion = Correcion_Suelo.objects.get(id=request.GET['id'])
        zona = correccion.lote
        correccion.delete()
        return HttpResponse(str(zona.id))
    else:
        return HttpResponse('error')

def get_correccion(request):
    if 'id' in request.GET:
        correccion = Correcion_Suelo.objects.get(id=request.GET['id'])
        salida = '%s,%s,%s,%s,%s,%s,%s,%s' %(correccion.enmienda, correccion.cantidad, correccion.precio_enmienda, correccion.precio_aplicadaEnmienda, correccion.unidad, correccion.area_aplicada, correccion.fecha_aplicada, correccion.subtotal)
        return HttpResponse(salida)

def editar_correccion(request):
    if request.method == 'POST':
        if 'id' in request.POST and 'enmienda' in request.POST and 'cantidad' in request.POST and 'precio_en' in request.POST and 'precio_apli' in request.POST and 'unidad' in request.POST and 'area' in request.POST and 'fecha' in request.POST:

            if request.POST['enmienda'] == '0' or request.POST['enmienda'] == 0 or request.POST['unidad'] == '0' or request.POST['unidad'] == 0:
                return HttpResponse('error')
            try:
                correcion = Correcion_Suelo.objects.get(id=request.POST['id'])
                if int(request.POST['area']) > correcion.lote.area:
                    return HttpResponse('area')

                correcion.enmienda = Enmienda.objects.get(id=request.POST['enmienda'])
                correcion.area_aplicada = request.POST['area']
                correcion.cantidad = request.POST['cantidad']
                correcion.fecha_aplicada = request.POST['fecha']
                correcion.unidad = Unidad.objects.get(id=request.POST['unidad'])
                correcion.precio_aplicadaEnmienda = request.POST['precio_apli']
                correcion.precio_enmienda = request.POST['precio_en']
                correcion.subtotal = request.POST['subtotal']
                correcion.save()
                return HttpResponse('ok')
            except Enmienda.DoesNotExist:
                return HttpResponse('error')

            except Unidad.DoesNotExist:
                return HttpResponse('error')
        else:
            return HttpResponse('.l.')

def totales_correccion_suelos(request):
    if request.method == 'GET':
        zona = Zona.objects.get(id=request.session['zona'])
        correciones = Correcion_Suelo.objects.filter(lote=zona)
        subtotal = 0
        aplicacion = 0
        for i in correciones:
            subtotal += i.subtotal
            aplicacion += i.precio_aplicadaEnmienda
        total = subtotal+aplicacion

        salida = ('%s,%s,%s') %(subtotal, aplicacion, total)

        return HttpResponse(str(salida))

def get_area_zona(request):
    if request.method == 'GET':
        zona = Zona.objects.get(id=request.session['zona'])
        return HttpResponse(str(zona.area))

#------------ fin crud de correcion de suelos -----



#--------------- Unidades-------------------

def get_unidades(request):
    unidades = Unidad.objects.filter(tipo=request.GET['tipo'])
    data = serializers.serialize('json', unidades, fields=('unidad'))
    return HttpResponse(data, mimetype='application/json')

def get_unidad(request):
    if request.method == 'GET' and 'id' in request.GET:
        unidad = Unidad.objects.get(id= request.GET['id'])
        return HttpResponse(str(unidad.unidad))

#--------------- fin Unidades---------------


#--------------- crud Fertilizantes ----------
def get_fertilizantes(request):
    fertilizantes = Fertilizantes.objects.order_by('fertilizante')
    data = serializers.serialize('json', fertilizantes, fields=('fertilizante'))
    return HttpResponse(data, mimetype='application/json')

def get_fertilizante(request):
    if request.method == 'GET':
        fertilizante = Fertilizantes.objects.get(id=request.GET['id'])
        return HttpResponse(str(fertilizante.fertilizante))

def add_fertilizante(request):
    if request.method == 'POST':
        if 'nombre' in request.POST:

            try:
                fertlizante = Fertilizantes()
                fertlizante.fertilizante = request.POST['nombre']
                usuario = Usuario.objects.get(documento=request.session['usuario'])
                fertlizante.usuarioCreador = usuario
                fertlizante.save()
                return HttpResponse('ok')
            except Usuario.DoesNotExist:
                return HttpResponse('user')
            except IntegrityError:
                return HttpResponse('ya')
        else:
            return HttpResponse('nombre')

def get_fertilizante_editar(request):
    if request.method == 'GET':
        fertilizante = Fertilizantes.objects.get(id=request.GET['id'])
        salida = '%s' %(fertilizante.fertilizante)
        return HttpResponse(salida)

def editar_fertilizante(request):
    if request.method == 'POST':
        if 'nombre' in request.POST and 'id' in request.POST:
            fertilizante = Fertilizantes.objects.get(id=request.POST['id'])
            try:
                fertilizante.fertilizante = request.POST['nombre']
                fertilizante.save()
                return HttpResponse('ok')
            except IntegrityError:
                return HttpResponse('ya')
        else:
            return HttpResponse('nombre')
    return Http404

#------------ fin crud fertilizante ----------

#---------------Crud Nivelacion nutrientes -----

def add_nivelacion(request):
    if request.method == 'POST':
        if 'fertilizante' in request.POST and 'cantidad' in request.POST and 'precio_fer' in request.POST and 'precio_apli' in request.POST and 'unidad' in request.POST and 'area' in request.POST and 'fecha' in request.POST:

            if request.POST['fertilizante'] == '0' or request.POST['fertilizante'] == 0 or request.POST['unidad'] == '0' or request.POST['unidad'] == 0:
                return HttpResponse('error')
            try:
                zona = Zona.objects.get(id=request.session['zona'])
                nivelacion = Nivelacion_Nutrientes()
                nivelacion.fertilizantes = Fertilizantes.objects.get(id=request.POST['fertilizante'])
                nivelacion.area_lote = zona.area
                nivelacion.cantidad = request.POST['cantidad']
                nivelacion.fecha_aplicacion = request.POST['fecha']
                nivelacion.unidad = Unidad.objects.get(id=request.POST['unidad'])
                nivelacion.lote = zona
                nivelacion.precio_aplicacion = request.POST['precio_apli']
                nivelacion.precio_nutriente = request.POST['precio_fer']
                nivelacion.subtotal = request.POST['subtotal']
                nivelacion.save()
                return HttpResponse('ok')
            except Fertilizantes.DoesNotExist:
                return HttpResponse('error')

            except Unidad.DoesNotExist:
                return HttpResponse('error')

            except Zona.DoesNotExist:
                return HttpResponse('zona')
        else:
            return HttpResponse('.l.')

def get_nivelaciones(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        nivelaciones = Nivelacion_Nutrientes.objects.filter(lote=zona)
        data = serializers.serialize('json', nivelaciones, fields=('fertilizantes', 'cantidad', 'precio_nutriente', 'precio_aplicacion', 'subtotal'))
        return HttpResponse(data, mimetype='application/json')

def totales_nivelacione_nutrientes(request):
    if request.method == 'GET':
        zona = Zona.objects.get(id=request.session['zona'])
        nivelaciones = Nivelacion_Nutrientes.objects.filter(lote=zona)
        subtotal = 0
        aplicacion = 0
        for i in nivelaciones:
            subtotal += i.subtotal
            aplicacion += i.precio_aplicacion
        total = subtotal+aplicacion

        salida = ('%s,%s,%s') %(subtotal, aplicacion, total)

        return HttpResponse(str(salida))

def borrar_nivelacion(request):
    if 'id' in request.GET:
        nivelacion = Nivelacion_Nutrientes.objects.get(id=request.GET['id'])
        zona = nivelacion.lote
        nivelacion.delete()
        return HttpResponse(str(zona.id))
    else:
        return HttpResponse('error')

def get_nivelacion_editar(request):
    if 'id' in request.GET:
        nivelacion = Nivelacion_Nutrientes.objects.get(id=request.GET['id'])
        salida = '%s,%s,%s,%s,%s,%s,%s,%s' %(nivelacion.unidad, nivelacion.area_lote, nivelacion.fertilizantes, nivelacion.cantidad, nivelacion.precio_nutriente, nivelacion.subtotal, nivelacion.precio_aplicacion, nivelacion.fecha_aplicacion)
        return HttpResponse(salida)

def editar_nivelacion(request):
    if request.method == 'POST':
        if 'id' in request.POST and 'fertilizante' in request.POST and 'cantidad' in request.POST and 'precio_fer' in request.POST and 'precio_apli' in request.POST and 'unidad' in request.POST and 'area' in request.POST and 'fecha' in request.POST:

            if request.POST['fertilizante'] == '0' or request.POST['fertilizante'] == 0 or request.POST['unidad'] == '0' or request.POST['unidad'] == 0:
                return HttpResponse('error')
            try:
                nivelacion = Nivelacion_Nutrientes.objects.get(id=request.POST['id'])
                nivelacion.fertilizantes = Fertilizantes.objects.get(id=request.POST['fertilizante'])
                nivelacion.cantidad = request.POST['cantidad']
                nivelacion.fecha_aplicacion = request.POST['fecha']
                nivelacion.unidad = Unidad.objects.get(id=request.POST['unidad'])
                nivelacion.precio_aplicacion = request.POST['precio_apli']
                nivelacion.precio_nutriente = request.POST['precio_fer']
                nivelacion.subtotal = request.POST['subtotal']
                nivelacion.save()
                return HttpResponse('ok')
            except Fertilizantes.DoesNotExist:
                return HttpResponse('error')

            except Unidad.DoesNotExist:
                return HttpResponse('error')

            except Zona.DoesNotExist:
                return HttpResponse('zona')
        else:
            return HttpResponse('.l.')


#--------------- fin Crud Nivelacion nutrientes -----


#------------------Crud labores----------------------
def add_labor(request):
    if request.method == 'POST':
        if 'nombre' in request.POST and 'tipo' in request.POST:

            try:
                labor = Labor()
                labor.labor = request.POST['nombre']
                labor.tipo = request.POST['tipo']
                usuario = Usuario.objects.get(documento=request.session['usuario'])
                labor.usuarioCreador = usuario
                labor.save()
                return HttpResponse('ok')
            except Usuario.DoesNotExist:
                return HttpResponse('user')
            except IntegrityError:
                return HttpResponse('ya')
        else:
            return HttpResponse('nombre')

def get_labores(request):
    labores = Labor.objects.order_by('tipo')
    data = serializers.serialize('json', labores, fields=('labor', 'tipo'))
    return HttpResponse(data, mimetype='application/json')

def get_labor_form(request):
    if 'tipo' in request.GET:
        labores = Labor.objects.filter(tipo=request.GET['tipo'])
        data = serializers.serialize('json', labores, fields=('labor'))
        return HttpResponse(data, mimetype='application/json')

def editar_labor(request):
    if request.method == 'POST':
        if 'nombre' in request.POST and 'tipo' in request.POST:
            labor = Labor.objects.get(id=request.POST['id'])
            labor.labor = request.POST['nombre']
            labor.tipo = request.POST['tipo']
            try:
                labor.save()
                return HttpResponse('ok')
            except IntegrityError:
                return HttpResponse('ya')
        else:
            return HttpResponse('nombre')

def get_labor_editar(request):
    if 'id' in request.GET:
        labor = Labor.objects.get(id=request.GET['id'])
        salida = '%s,%s' %(labor.labor, labor.tipo)
        return HttpResponse(salida)

def get_labor(request):
    if 'id' in request.GET:
        labor = Labor.objects.get(id=request.GET['id'])
        return HttpResponse(labor.labor)

#------------------fin Crud labores------------------

#-------------crud Preparacion Fisica--------------------

def get_preparaciones_fisicas(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        preparaciones = Preparacion_Suelo.objects.filter(lote=zona)
        data = serializers.serialize('json', preparaciones, fields=('labor', 'area_lote', 'fecha_preparacion', 'precio', 'subtotal', 'tipoMedida'))
        return HttpResponse(data, mimetype='application/json')

def totales_preparacion(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        preparaciones = Preparacion_Suelo.objects.filter(lote=zona)
        totalarea = 0
        totalmtr = 0

        for p in preparaciones:
            if p.tipoMedida == '1':
                totalarea += p.subtotal
            else:
                totalmtr += p.subtotal

        salida = '%s,%s,%s' %(totalarea, totalmtr, (totalarea+totalmtr))
        return HttpResponse(salida)

def add_preparacion_fisica(request):
    if request.method == 'POST':
        zona = Zona.objects.get(id=request.session['zona'])
        if request.POST['labor'] == '0':
            return HttpResponse('error')

        labor = Labor.objects.get(id=request.POST['labor'])
        pf = Preparacion_Suelo()
        pf.tipoMedida = request.POST['tipo']
        pf.lote = zona
        pf.fecha_preparacion = request.POST['fecha']
        pf.labor = labor
        pf.area_lote = request.POST['area']
        pf.precio = request.POST['precio']
        pf.subtotal = request.POST['subtotal']
        pf.save()
        return HttpResponse('ok')

def editar_preparacion_fisica(request):
    if request.method == 'POST':
        if request.POST['labor'] == '0':
            return HttpResponse('error')

        labor = Labor.objects.get(id=request.POST['labor'])
        pf = Preparacion_Suelo.objects.get(id=request.POST['id'])
        pf.fecha_preparacion = request.POST['fecha']
        pf.labor = labor
        pf.area_lote = request.POST['area']
        pf.precio = request.POST['precio']
        pf.subtotal = request.POST['subtotal']
        pf.save()
        return HttpResponse(str(pf.lote.id))

def get_preparacion_fisica_editar(request):
    if 'id' in request.GET:
        pf = Preparacion_Suelo.objects.get(id=request.GET['id'])
        salida = '%s,%s,%s,%s,%s,%s' %(pf.tipoMedida, pf.fecha_preparacion, pf.labor, pf.area_lote, pf.precio, pf.subtotal)
        return HttpResponse(salida)

def borrar_preparacion_fisica(requets):
    if 'id' in requets.GET:
        pf = Preparacion_Suelo.objects.get(id=requets.GET['id'])
        zona = pf.lote
        pf.delete()
        return HttpResponse(str(zona.id))

#-------------fin crud Preparacion Fisica--------------------


#-------------crud Insumos----------------
def get_insumos(request):
    insumos = Insumos.objects.order_by('tipo')
    data = serializers.serialize('json', insumos, fields=('insumo', 'tipo'))
    return HttpResponse(data, mimetype='application/json')

def get_insumos_form(request):
    insumos = Insumos.objects.filter(tipo=request.GET['tipo'])
    data = serializers.serialize('json', insumos, fields=('insumo', 'tipo'))
    return HttpResponse(data, mimetype='application/json')

def add_insumo(request):
    if request.method == 'POST' and 'nombre' in request.POST:
        try:
            insumo = Insumos()
            insumo.insumo = request.POST['nombre']
            insumo.tipo = request.POST['tipo']
            insumo.usuarioCreador = Usuario.objects.get(documento=request.session['usuario'])
            insumo.save()
            return HttpResponse('ok')
        except IntegrityError:
            return HttpResponse('ya')

def get_insumo_editar(request):
    if request.method == 'GET' and 'id' in request.GET:
        insumo = Insumos.objects.get(id=request.GET['id'])
        salida = '%s,%s' %(insumo.insumo, insumo.tipo)
        return HttpResponse(salida)

def editar_insumo(request):
    if request.method == 'POST' and 'nombre' in request.POST and 'id' in request.POST:
        try:
            insumo = Insumos.objects.get(id=request.POST['id'])
            insumo.insumo = request.POST['nombre']
            insumo.tipo = request.POST['tipo']
            insumo.save()

            return HttpResponse('ok')
        except Insumos.DoesNotExist:
            return HttpResponse('not')
        except IntegrityError:
            return HttpResponse('ya')

def get_insumo(request):
    if 'id' in request.GET:
        insumo = Insumos.objects.get(id= request.GET['id'])
        return HttpResponse(insumo.insumo)

#------------- fin crud Insumos----------------


#---------------Crud Siembra de Cobertura-----------
def get_siembra_cobertura(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        coberturas = Siembra_Cobertura.objects.filter(lote=zona)
        data = serializers.serialize('json', coberturas, fields=('area_lote', 'fecha_siembra', 'cantidad', 'precio_unidad', 'subtotal', 'unidad', 'insumo'))
        return HttpResponse(data, mimetype='application/json')

def add_siembra_cobertura(request):
    if 'zona' in request.session and request.method == 'POST':
        if request.POST['unidad'] == '0' or request.POST['unidad'] == 0 or request.POST['insumo'] == '0' or request.POST['insumo'] == 0:
            return HttpResponse('error')

        zona = Zona.objects.get(id=request.session['zona'])
        siembra = Siembra_Cobertura()
        siembra.area_lote = request.POST['area']
        siembra.fecha_siembra = request.POST['fecha']
        siembra.cantidad = request.POST['cantidad']
        siembra.precio_unidad = request.POST['precio_unidad']
        siembra.subtotal = request.POST['subtotal']
        siembra.lote = zona
        siembra.unidad = Unidad.objects.get(id=request.POST['unidad'])
        siembra.insumo = Insumos.objects.get(id=request.POST['insumo'])
        siembra.save()
        return HttpResponse('ok')

def totales_siembra_cobertura(request):
    zona = Zona.objects.get(id=request.session['zona'])
    coberturas = Siembra_Cobertura.objects.filter(lote=zona)
    total = 0
    for c in coberturas:
        total += c.subtotal
    return HttpResponse(str(total))

def borrar_siembra_cobertura(request):
    if request.method == 'GET' and 'id' in request.GET:
        try:
            siembra = Siembra_Cobertura.objects.get(id=request.GET['id'])
            siembra.delete()
            return HttpResponse('ok')
        except Siembra_Cobertura.DoesNotExist:
            return HttpResponse('not')

def get_siembra_cobertura_editar(request):
    if request.method == 'GET' and 'id' in request.GET:
        siembra = Siembra_Cobertura.objects.get(id=request.GET['id'])
        salida = '%s,%s,%s,%s,%s,%s,%s' %(siembra.unidad, siembra.area_lote, siembra.insumo, siembra.cantidad, siembra.precio_unidad, siembra.subtotal, siembra.fecha_siembra)
        return HttpResponse(salida)

def editar_siembra_cobertura(request):
    if 'zona' in request.session and request.method == 'POST':
        if request.POST['unidad'] == '0' or request.POST['unidad'] == 0 or request.POST['unidad'] == '0' or request.POST['unidad'] == 0:
            return HttpResponse('error')

        siembra = Siembra_Cobertura.objects.get(id=request.POST['id'])
        siembra.area_lote = request.POST['area']
        siembra.fecha_siembra = request.POST['fecha']
        siembra.cantidad = request.POST['cantidad']
        siembra.precio_unidad = request.POST['precio_unidad']
        siembra.subtotal = request.POST['subtotal']
        siembra.unidad = Unidad.objects.get(id=request.POST['unidad'])
        siembra.insumo = Insumos.objects.get(id=request.POST['insumo'])
        siembra.save()
        return HttpResponse('ok')

#---------------fin Crud Siembra de Cobertura-----------

def get_siembra_palma(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        palmas = Palma_Siembra.objects.filter(lote=zona)
        data = serializers.serialize('json', palmas, fields=('area', 'fecha_siembra', 'cantidad_plantulas', 'precio', 'subtotal', 'unidad', 'tipo'))
        return HttpResponse(data, mimetype='application/json')

def get_total_siembra_palma(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        palmas = Palma_Siembra.objects.filter(lote=zona)
        total = 0
        for p in palmas:
            total += p.subtotal

        return HttpResponse(str(total))

def add_siembra_palma(request):
    if 'zona' in request.session and request.method == 'POST':
        if request.POST['unidad'] == '0' or request.POST['unidad'] == 0 or request.POST['insumo'] == '0' or request.POST['insumo'] == 0:
            return HttpResponse('error')
        try:
            zona = Zona.objects.get(id=request.session['zona'])
            siembra = Palma_Siembra()
            siembra.area = request.POST['area']
            siembra.fecha_siembra = request.POST['fecha']
            siembra.cantidad_plantulas = request.POST['cantidad']
            siembra.precio = request.POST['precio_unidad']
            siembra.subtotal = request.POST['subtotal']
            siembra.lote = zona
            siembra.unidad = Unidad.objects.get(id=request.POST['unidad'])
            siembra.tipo = Insumos.objects.get(id=request.POST['insumo'])
            siembra.save()
            return HttpResponse('ok')
        except Zona.DoesNotExist:
            return HttpResponse('error')
        except Unidad.DoesNotExist:
            return HttpResponse('error')
        except Insumos.DoesNotExist:
            return HttpResponse('error')

def borrar_siembra_palma(request):
    if request.method == 'GET' and 'id' in request.GET:
        try:
            siembra = Palma_Siembra.objects.get(id=request.GET['id'])
            siembra.delete()
            return HttpResponse('ok')
        except Palma_Siembra.DoesNotExist:
            return HttpResponse('not')

def editar_siembra_palma(request):
    if 'zona' in request.session and request.method == 'POST':
        if request.POST['unidad'] == '0' or request.POST['unidad'] == 0 or request.POST['insumo'] == '0' or request.POST['insumo'] == 0:
            return HttpResponse('error')
        try:
            siembra = Palma_Siembra.objects.get(id=request.POST['id'])
            siembra.area = request.POST['area']
            siembra.fecha_siembra = request.POST['fecha']
            siembra.cantidad_plantulas = request.POST['cantidad']
            siembra.precio = request.POST['precio_unidad']
            siembra.subtotal = request.POST['subtotal']
            siembra.unidad = Unidad.objects.get(id=request.POST['unidad'])
            siembra.tipo = Insumos.objects.get(id=request.POST['insumo'])
            siembra.save()
            return HttpResponse('ok')
        except Zona.DoesNotExist:
            return HttpResponse('error')
        except Unidad.DoesNotExist:
            return HttpResponse('error')
        except Item.DoesNotExist:
            return HttpResponse('error')

def get_siembra_palma_editar(request):
    if request.method == 'GET' and 'id' in request.GET:
        siembra = Palma_Siembra.objects.get(id=request.GET['id'])
        salida = '%s,%s,%s,%s,%s,%s,%s' %(siembra.unidad, siembra.area, siembra.tipo, siembra.cantidad_plantulas, siembra.precio, siembra.subtotal, siembra.fecha_siembra)
        return HttpResponse(salida)

#---------------------Crud de Item-------------------------

def get_items(request):
    if request.method == 'GET':
        items = Item.objects.all()
        data = serializers.serialize('json', items, fields=('item'))
        return HttpResponse(data, mimetype='application/json')

def get_item(request):
    if 'id' in request.GET:
        item = Item.objects.get(id=request.GET['id'])
        return HttpResponse(item.item)


#---------------------fin Crud de Item-------------------------

#----------------Crud otros costos de establecimiento----------
def get_otros_costos_ce(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        otros = Otro_ce.objects.filter(lote=zona)
        data = serializers.serialize('json', otros, fields=('area', 'cantidad', 'fecha_actividad', 'precio', 'subtotal', 'unidad', 'labor'))
        return HttpResponse(data, mimetype='application/json')

def borrar_otro_ce(request):
    if request.method == 'GET' and 'id' in request.GET:
        try:
            otro_ce = Otro_ce.objects.get(id=request.GET['id'])
            otro_ce.delete()
            return HttpResponse('ok')
        except Otro_ce.DoesNotExist:
            return HttpResponse('error')

def get_total_otros_ce(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        otros_ce = Otro_ce.objects.filter(lote=zona)
        total = 0.0
        for o in otros_ce:
            total += o.subtotal

        return HttpResponse(str(total))

def add_otro_ce(request):
    if 'zona' in request.session and request.method == 'POST':
        if request.POST['unidad'] == '0' or request.POST['unidad'] == 0 or request.POST['labor'] == '0' or request.POST['labor'] == 0:
            return HttpResponse('error')
        try:
            zona = Zona.objects.get(id=request.session['zona'])
            otro = Otro_ce()
            otro.area = request.POST['area']
            otro.fecha_actividad = request.POST['fecha']
            otro.cantidad = request.POST['cantidad']
            otro.precio = request.POST['precio_unidad']
            otro.subtotal = request.POST['subtotal']
            otro.lote = zona
            otro.unidad = Unidad.objects.get(id=request.POST['unidad'])
            otro.labor = Labor.objects.get(id=request.POST['labor'])
            otro.save()
            return HttpResponse('ok')
        except Zona.DoesNotExist:
            return HttpResponse('error')
        except Unidad.DoesNotExist:
            return HttpResponse('error')
        except Labor.DoesNotExist:
            return HttpResponse('error')

def get_otro_ce_editar(request):
    if request.method == 'GET' and 'id' in request.GET:
        otro_ce = Otro_ce.objects.get(id=request.GET['id'])
        salida = '%s,%s,%s,%s,%s,%s,%s' %(otro_ce.unidad, otro_ce.area, otro_ce.labor, otro_ce.cantidad, otro_ce.precio, otro_ce.subtotal, otro_ce.fecha_actividad)
        return HttpResponse(salida)

def editar_otro_ce(request):
    if 'id' in request.POST and request.method == 'POST':
        if request.POST['unidad'] == '0' or request.POST['unidad'] == 0 or request.POST['labor'] == '0' or request.POST['labor'] == 0:
            return HttpResponse('error')
        try:
            otro = Otro_ce.objects.get(id=request.POST['id'])
            otro.area = request.POST['area']
            otro.fecha_actividad = request.POST['fecha']
            otro.cantidad = request.POST['cantidad']
            otro.precio = request.POST['precio_unidad']
            otro.subtotal = request.POST['subtotal']
            otro.unidad = Unidad.objects.get(id=request.POST['unidad'])
            otro.labor = Labor.objects.get(id=request.POST['labor'])
            otro.save()
            return HttpResponse('ok')
        except Zona.DoesNotExist:
            return HttpResponse('error')
        except Unidad.DoesNotExist:
            return HttpResponse('error')
        except Labor.DoesNotExist:
            return HttpResponse('error')


#----------------fin  Crud otros costos de establecimiento----------


#--------------- Crud de labores de siembra------------------------

def get_labores_siembra(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        labor_siembra = Labor_Siembra.objects.filter(lote=zona)
        data = serializers.serialize('json', labor_siembra, fields=('area_labor', 'cantidad_laboradas', 'fecha_labor', 'precio_labor', 'subtotal', 'unidad', 'labor'))
        return HttpResponse(data, mimetype='application/json')

def get_total_labores_siembra(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])
        labor_siembra = Labor_Siembra.objects.filter(lote=zona)
        salida = 0.0
        for l in labor_siembra:
            salida += l.subtotal

        return HttpResponse(str(salida))

def borrar_labor_siembra(request):
    if request.method == 'GET' and 'id' in request.GET:
        try:
            labor_siembra = Labor_Siembra.objects.get(id=request.GET['id'])
            labor_siembra.delete()
            return HttpResponse('ok')
        except Otro_ce.DoesNotExist:
            return HttpResponse('error')

def add_labor_siembra(request):
    if 'zona' in request.session and request.method == 'POST':
        if request.POST['unidad'] == '0' or request.POST['unidad'] == 0 or request.POST['labor'] == '0' or request.POST['labor'] == 0:
            return HttpResponse('error')
        try:
            zona = Zona.objects.get(id=request.session['zona'])
            labor_siembra = Labor_Siembra()
            labor_siembra.area_labor = request.POST['area']
            labor_siembra.fecha_labor = request.POST['fecha']
            labor_siembra.cantidad_laboradas = request.POST['cantidad']
            labor_siembra.precio_labor = request.POST['precio_unidad']
            labor_siembra.subtotal = request.POST['subtotal']
            labor_siembra.lote = zona
            labor_siembra.unidad = Unidad.objects.get(id=request.POST['unidad'])
            labor_siembra.labor = Labor.objects.get(id=request.POST['labor'])
            labor_siembra.save()
            return HttpResponse('ok')
        except Zona.DoesNotExist:
            return HttpResponse('error')
        except Unidad.DoesNotExist:
            return HttpResponse('error')
        except Labor.DoesNotExist:
            return HttpResponse('error')

def get_labor_siembra_editar(request):
    if request.method == 'GET' and 'id' in request.GET:
        labor_siembra = Labor_Siembra.objects.get(id=request.GET['id'])
        salida = '%s,%s,%s,%s,%s,%s,%s' %(labor_siembra.unidad, labor_siembra.area_labor, labor_siembra.labor, labor_siembra.cantidad_laboradas, labor_siembra.precio_labor, labor_siembra.subtotal, labor_siembra.fecha_labor)
        return HttpResponse(salida)

def editar_labor_siembra(request):
    if 'zona' in request.session and request.method == 'POST':
        if request.POST['unidad'] == '0' or request.POST['unidad'] == 0 or request.POST['labor'] == '0' or request.POST['labor'] == 0:
            return HttpResponse('error')
        try:
            labor_siembra = Labor_Siembra.objects.get(id=request.POST['id'])
            labor_siembra.area_labor = request.POST['area']
            labor_siembra.fecha_labor = request.POST['fecha']
            labor_siembra.cantidad_laboradas = request.POST['cantidad']
            labor_siembra.precio_labor = request.POST['precio_unidad']
            labor_siembra.subtotal = request.POST['subtotal']
            labor_siembra.unidad = Unidad.objects.get(id=request.POST['unidad'])
            labor_siembra.labor = Labor.objects.get(id=request.POST['labor'])
            labor_siembra.save()
            return HttpResponse('ok')
        except Zona.DoesNotExist:
            return HttpResponse('error')
        except Unidad.DoesNotExist:
            return HttpResponse('error')
        except Labor.DoesNotExist:
            return HttpResponse('error')

#--------------- fin Crud de labores de siembra------------------------

#--------------- fin Crud reporte costos establecimiento------------------------
def reporte_ce(request):
    if 'zona' in request.session:
        zona = Zona.objects.get(id=request.session['zona'])

        correcciones =Correcion_Suelo.objects.filter(lote=zona)
        nivelaciones = Nivelacion_Nutrientes.objects.filter(lote=zona)
        preparacion_fisica = Preparacion_Suelo.objects.filter(lote=zona)
        siembra_cobertura = Siembra_Cobertura.objects.filter(lote=zona)
        palmas_siembra = Palma_Siembra.objects.filter(lote=zona)
        labores_siembra = Labor_Siembra.objects.filter(lote=zona)
        otros_costos = Otro_ce.objects.filter(lote=zona)

        total_correcciones = 0
        total_nivelaciones = 0
        total_preparacion_fisica = 0
        total_siembra_cobertura = 0
        total_palmas_siembra = 0
        total_labores_siembra = 0
        total_otros_costos = 0

        for c in correcciones:
            total_correcciones += c.subtotal+c.precio_aplicadaEnmienda

        for n in nivelaciones:
            total_nivelaciones += n.subtotal +n.precio_aplicacion

        for pr in preparacion_fisica:
            total_preparacion_fisica += pr.subtotal

        for s in siembra_cobertura:
            total_siembra_cobertura += s.subtotal

        for ps in palmas_siembra:
            total_palmas_siembra += ps.subtotal

        for ls in labores_siembra:
            total_labores_siembra += ls.subtotal

        for o in otros_costos:
            total_otros_costos += o.subtotal

        total_costos = total_correcciones+total_nivelaciones+total_preparacion_fisica+total_siembra_cobertura+total_palmas_siembra+total_labores_siembra+total_otros_costos

        return render(request, 'pdf.html', {'correccion':total_correcciones, 'nivelacion':total_nivelaciones, 'prepa_fisica':total_preparacion_fisica, 'siembra_cobertura':total_siembra_cobertura, 'Palmas_siembra':total_palmas_siembra, 'siembra_palma':total_labores_siembra, 'otro':total_otros_costos, 'total':total_costos})
