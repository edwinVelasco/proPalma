__author__ = 'edwin'

# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'palma.views.index'),
    url(r'^loguear$', 'palma.views.loguear'),
    url(r'^login$', 'palma.views.login'),
    url(r'^logout$', 'palma.views.logout'),
    url(r'^get_palmicultor$', 'palma.views.get_palmicultor_sesion'),
    url(r'^editar_password$', 'palma.views.editar_password'),
    url(r'^pedir_documento$', 'palma.views.pedir_documento'),
    url(r'^recuperar_password$', 'palma.views.recuperar_password'),

    #para el form de registro del palmicultor
    url(r'^get_departamentos$', 'palma.views.get_departamentos'),
    url(r'^get_tipos_documento$', 'palma.views.get_tipos_documento'),
    url(r'^get_municipios$', 'palma.views.get_municipios'),


    url(r'^get_municipios$', 'palma.views.get_municipios'),
    url(r'^add_palmicultor$', 'palma.views.add_palmicultor'),
    url(r'^editar_palmicultor$', 'palma.views.editar_palmicultor'),
    url(r'^activar_desactivar$', 'palma.views.activar_desactivar'),
    url(r'^get_palmicultores$', 'palma.views.get_palmicultores'),
    url(r'^revicion_pass$', 'palma.views.revicion_pass'),
    url(r'^get_palmicultores_filtro_admin$', 'palma.views.get_palmicultores_filtro_admin'),
    url(r'^desactivar_palmicultor$', 'palma.views.desactivar_palmicultor'),

    #--------------edirar palmicultor por el admin-----------------

    url(r'^get_palmicultor_admin$', 'palma.views.get_palmicultor_admin'),
    url(r'^reset_pass$', 'palma.views.reset_pass'),
    url(r'^editar_palmicultor_admin$', 'palma.views.editar_palmicultor_admin'),


    #-------hacienda--------------
    url(r'^get_haciendas$', 'palma.views.get_haciendas'),
    url(r'^add_hacienda$', 'palma.views.add_hacienda'),
    url(r'^get_hacienda$', 'palma.views.get_hacienda'),
    url(r'^editar_hacienda$', 'palma.views.editar_hacienda'),


    #----------Zonas-------
    url(r'^zona$', 'palma.views.zona'),
    url(r'^add_zona$', 'palma.views.add_zona'),
    url(r'^get_zonas$', 'palma.views.get_zonas'),
    url(r'^get_zona$', 'palma.views.get_zona'),
    url(r'^editar_zona$', 'palma.views.editar_zona'),
    url(r'^zona_session$', 'palma.views.zona_session'),


    #---------Enmiendas-----
    url(r'^add_enmienda$', 'palma.views.add_enmienda'),
    url(r'^get_enmiendas$', 'palma.views.get_enmiendas'),
    url(r'^get_enmienda$', 'palma.views.get_enmienda'),
    url(r'^editar_enmienda$', 'palma.views.editar_enmienda'),

    #--------Correcione de Suelos---------
    url(r'^get_correciones$', 'palma.views.get_correciones'),
    url(r'^add_correccion$', 'palma.views.add_correccion'),
    url(r'^borrar_correccion$', 'palma.views.borrar_correccion'),
    url(r'^get_correccion$', 'palma.views.get_correccion'),
    url(r'^editar_correccion$', 'palma.views.editar_correccion'),
    url(r'^totales_correccion_suelos$', 'palma.views.totales_correccion_suelos'),
    url(r'^get_area_zona$', 'palma.views.get_area_zona'),



    #--------Unidades----------
    url(r'^get_unidades$', 'palma.views.get_unidades'),
    url(r'^get_unidad$', 'palma.views.get_unidad'),



    #----------Fertilizantes------
    url(r'^get_fertilizantes$', 'palma.views.get_fertilizantes'),
    url(r'^add_fertilizante$', 'palma.views.add_fertilizante'),
    url(r'^get_fertilizante_editar$', 'palma.views.get_fertilizante_editar'),
    url(r'^editar_fertilizante$', 'palma.views.editar_fertilizante'),
    url(r'^get_fertilizante$', 'palma.views.get_fertilizante'),


    #----------Nivelacion de nutrientes------
    url(r'^get_nivelaciones$', 'palma.views.get_nivelaciones'),
    url(r'^add_nivelacion$', 'palma.views.add_nivelacion'),
    url(r'^totales_nivelacione_nutrientes$', 'palma.views.totales_nivelacione_nutrientes'),
    url(r'^borrar_nivelacion$', 'palma.views.borrar_nivelacion'),
    url(r'^get_nivelacion_editar$', 'palma.views.get_nivelacion_editar'),
    url(r'^editar_nivelacion$', 'palma.views.editar_nivelacion'),


    #---------------labores-----------------
    url(r'^add_labor$', 'palma.views.add_labor'),
    url(r'^get_labores$', 'palma.views.get_labores'),
    url(r'^editar_labor$', 'palma.views.editar_labor'),
    url(r'^get_labor_editar$', 'palma.views.get_labor_editar'),
    url(r'^get_labor_form$', 'palma.views.get_labor_form'),
    url(r'^get_labor$', 'palma.views.get_labor'),


    #-------------preparaciones fisicas -----------
    url(r'^get_preparaciones_fisicas$', 'palma.views.get_preparaciones_fisicas'),
    url(r'^totales_preparacion$', 'palma.views.totales_preparacion'),
    url(r'^add_preparacion_fisica$', 'palma.views.add_preparacion_fisica'),
    url(r'^editar_preparacion_fisica$', 'palma.views.editar_preparacion_fisica'),
    url(r'^get_preparacion_fisica_editar$', 'palma.views.get_preparacion_fisica_editar'),
    url(r'^borrar_preparacion_fisica$', 'palma.views.borrar_preparacion_fisica'),


    #---------------insumos-----------
    url(r'^get_insumos$', 'palma.views.get_insumos'),
    url(r'^add_insumo$', 'palma.views.add_insumo'),
    url(r'^get_insumo_editar$', 'palma.views.get_insumo_editar'),
    url(r'^editar_insumo$', 'palma.views.editar_insumo'),
    url(r'^get_insumo$', 'palma.views.get_insumo'),
    url(r'^get_insumos_form$', 'palma.views.get_insumos_form'),


    #---------------Siembras de Cobertura--------------
    url(r'^get_siembra_cobertura$', 'palma.views.get_siembra_cobertura'),
    url(r'^totales_siembra_cobertura$', 'palma.views.totales_siembra_cobertura'),
    url(r'^borrar_siembra_cobertura$', 'palma.views.borrar_siembra_cobertura'),
    url(r'^add_siembra_cobertura$', 'palma.views.add_siembra_cobertura'),
    url(r'^get_siembra_cobertura_editar$', 'palma.views.get_siembra_cobertura_editar'),
    url(r'^editar_siembra_cobertura$', 'palma.views.editar_siembra_cobertura'),



    #---------------siembra de palma----------
    url(r'^get_siembra_palma$', 'palma.views.get_siembra_palma'),
    url(r'^get_total_siembra_palma$', 'palma.views.get_total_siembra_palma'),
    url(r'^add_siembra_palma$', 'palma.views.add_siembra_palma'),
    url(r'^borrar_siembra_palma$', 'palma.views.borrar_siembra_palma'),
    url(r'^editar_siembra_palma$', 'palma.views.editar_siembra_palma'),
    url(r'^get_siembra_palma_editar$', 'palma.views.get_siembra_palma_editar'),



    #---------------------items---------------------------
    url(r'^get_items$', 'palma.views.get_items'),
    url(r'^get_item$', 'palma.views.get_item'),


    #---------------------Otros CE---------------
    url(r'^get_otros_costos_ce$', 'palma.views.get_otros_costos_ce'),
    url(r'^borrar_otro_ce$', 'palma.views.borrar_otro_ce'),
    url(r'^get_total_otros_ce$', 'palma.views.get_total_otros_ce'),
    url(r'^add_otro_ce$', 'palma.views.add_otro_ce'),
    url(r'^get_otro_ce_editar$', 'palma.views.get_otro_ce_editar'),
    url(r'^editar_otro_ce$', 'palma.views.editar_otro_ce'),

    #-------------------Labores de Siembra-----------------
    url(r'^get_labores_siembra$', 'palma.views.get_labores_siembra'),
    url(r'^get_total_labores_siembra$', 'palma.views.get_total_labores_siembra'),
    url(r'^borrar_labor_siembra$', 'palma.views.borrar_labor_siembra'),
    url(r'^add_labor_siembra$', 'palma.views.add_labor_siembra'),
    url(r'^get_labor_siembra_editar$', 'palma.views.get_labor_siembra_editar'),
    url(r'^editar_labor_siembra$', 'palma.views.editar_labor_siembra'),

    #---------------------Reporte de costos de establecimiento-------
    url(r'^reporte_ce$', 'palma.views.reporte_ce'),

    )
