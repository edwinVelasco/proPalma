/**
 * Created by edwin on 5/04/15.
 */

function haciendas(){
    texto = '<br/><p class="login-logo">Listado de Haciendas</p><br/>'
    tabla = '<div id="lista_haciendas" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Nombre</th> <th>Dirección</th> <th>Núcleo Palmero</th> <th>Área Total</th> <th>Estado</th> <th>Información</th> <th>Editar</th> <th>Lotes/Zonas</th></tr>    </thead>';
    tbody = '<tbody id="body_haciendas"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_hacienda()" type="button">Nueva Hacienda</button></div></div>'

    $("#cuerpo").html(texto+tabla+boton_agregar);

    $.ajax({
            type: "GET",
            url: "get_haciendas",
            data: "",
            success: function (data) {
                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay haciendas registradas',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{
                    html = '';
                    for (i=0; i< data.length; i++)
                    {
                        nombre = '<tr><td>'+data[i].fields.nombre+'</td>';
                        direccion = '<td>'+data[i].fields.direccion+'</td>';
                        nucleo = '<td>'+data[i].fields.nucleo_palmero+'</td>';
                        telefono = '<td>'+data[i].fields.telefono+'</td>';
                        area = '<td>'+data[i].fields.area_total+'</td>';
                        estado = '<td>Activo</td>';
                        if (data[i].fields.activo === '0')
                            estado = '<td>Inactivo</td>';

                        ver = '<td><button class="btn btn-success col-xs-4" onclick="ver_hacienda('+data[i].pk+')" type="button">Ver</button></td>';
                        editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_hacienda('+data[i].pk+')" type="button">Ir</button></td>';
                        reg_lote = '<td><button class="btn btn-success col-xs-4" onclick="zonas_hacienda('+data[i].pk+')" type="button">Ver</button></td></tr>';
                        html += nombre+direccion+nucleo+area+estado+ver+editar+reg_lote;
                    }
                    $('#body_haciendas').html(html);

                }


            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function new_hacienda(){
    $("#cuerpo").load( "../static/html/registro_hacienda.html");
}
function ver_hacienda(pk){
    hacienda_editar = pk;
    $("#cuerpo").load( "../static/html/ver_hacienda.html");
}

function editar_hacienda(pk){
    hacienda_editar = pk;
    $("#cuerpo").load( "../static/html/editar_hacienda.html");
}

function zonas_hacienda(id){
    texto = '<br/><p id="listado-lote" class="login-logo">Listado de Lotes/Zonas</p><br/>'
    tabla = '<div id="lista_lotes" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Código</th> <th>Área</th> <th>Capacidad</th> <th>Fecha de Plantación</th> <th>Estado</th> <th>Ver</th>  <th>Editar</th> <th>Costos</th> </thead>';
    tbody = '<tbody id="body_zonas"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_zona('+id+')" type="button">Nueva Zona/Lote</button></div></div>'

    $("#cuerpo").html(texto+tabla+boton_agregar);

    $.ajax({
            type: "GET",
            url: "get_zonas",
            data: {'id':id},
            success: function (data) {

                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay Zonas Registradas',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{
                    html = '';
                    for (i=0; i< data.length; i++)
                    {
                        codigo = '<td>'+data[i].fields.codigo+'</td>';
                        area = '<td>'+data[i].fields.area+'</td>';
                        capacidad = '<td>'+data[i].fields.capacidad_palma+'</td>';
                        fecha = '<td>'+data[i].fields.fecha_plantacion+'</td>';
                        ver = '<td><button class="btn btn-success col-xs-4" onclick="ver_zona('+data[i].pk+')" type="button">Ver</button></td>';
                        estado = '<td>Activo</td>';
                        if (data[i].fields.activo =='1')
                            estado = '<td>Inactivo</td>';
                        editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_zona('+data[i].pk+')" type="button">Ir</button></td>';
                        registros = '<td><button class="btn btn-success col-xs-4" onclick="redireccionar_zona('+data[i].pk+')" type="button">Ir</button></td>';

                        html += '<tr>'+codigo+area+capacidad+fecha+estado+ver+editar+registros+'</tr>';

                    }
                    $('#body_zonas').html(html);

                }


            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function new_zona(id){
    hacienda_editar = id;
    $("#cuerpo").load( "../static/html/registro_zona.html");
}

function editar_zona(id){
    hacienda_editar = id;
    $("#cuerpo").load( "../static/html/editar_zona.html");
}
function ver_zona(id)
{
    hacienda_editar = id;
    $("#cuerpo").load( "../static/html/ver_zona.html");
}

function redireccionar_zona(zona){
    $.ajax({
            type: "GET",
            url: "zona_session",
            data: {'zona':zona},
            success: function (data) {
                window.location = '/zona'
            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}
