/**
 * Created by edwin on 30/05/15.
 */
/**
 * Created by edwin on 15/05/15.
 */
function get_preparaciones_fisicas(){

    texto = '<br/><p class="login-logo">Listado de Preparaciones fisicas de Suelo por Metro Lineal</p><br/>'
    tabla = '<div id="lista_cor_suelos" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>labor</th> <th>Area Adecuada</th> <th>fecha</th> <th>$ por Hectarea</th>  <th>subtotal</th> <th>Editar</th> <th>Borrar</th></tr>    </thead>';
    tbody = '<tbody id="body_preparacion_mtr"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_preparacion(0)" type="button">Nueva</button></div></div> </br></br>';

    texto_area = '<br/><p class="login-logo">Listado de Preparaciones fisicas de Suelo por Area</p><br/>'
    tabla_area = '<div id="lista_cor_suelos" class="register-page"><table class="table table-hover">';
    thead_area = '<thead>    <tr>    <th>labor</th> <th>Area Adecuada</th> <th>fecha</th> <th>$ por Hectarea</th>  <th>subtotal</th> <th>Editar</th> <th>Borrar</th></tr>    </thead>';
    tbody_area = '<tbody id="body_preparacion_area"></tbody>';
    tabla_area += thead_area + tbody_area + '</table> </div>';
    boton_agregar_area = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_preparacion(1)" type="button">Nueva</button></div></div> </br></br>';


    tabla_resultados = '<div class="register-page"><table class="table table-hover">';
    thead_resultados = '<thead>    <tr>    <th>Descripción</th> <th>Valor</th> </tr> </thead>';
    tbody_resultados = '<tbody id="resultados_preparacion_fisica"></tbody>';
    tabla_resultados += thead_resultados + tbody_resultados + '</table> </div>';

    $("#cuerpo").html(texto+tabla+boton_agregar+texto_area+tabla_area+boton_agregar_area+tabla_resultados);

    pintar_tabla_resultados_preparacion();

    $.ajax({
            type: "GET",
            url: "get_preparaciones_fisicas",
            data: '',
            success: function (data) {
                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay Prepareciones Fisicas de Suelo Registradas',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{

                    for (i=0; i< data.length; i++)
                    {
                        add_fila_preparacion(data[i]);
                    }
                }

            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function pintar_tabla_resultados_preparacion(){
    $.ajax({
            type: "GET",
            url: "totales_preparacion",
            data: '',
            success: function (data) {
                datos = data.split(',');
                subtotal = '<tr> <td>Subtotal Preparación Fisica de Suelos por Area</td><td>'+datos[0]+'</td></tr>';
                $('#resultados_preparacion_fisica').append(subtotal);
                aplicacion = '<tr> <td>Subtotal Preparación Fisica de Suelos por Metro Lineal</td><td>'+datos[1]+'</td></tr>';
                $('#resultados_preparacion_fisica').append(aplicacion);
                total = '<tr> <td>Total Preparación Fisica de Suelos</td><td>'+datos[2]+'</td></tr>';
                $('#resultados_preparacion_fisica').append(total);
            },
            error: function(data) {
                console.log(data)
            }
        });
}

function add_fila_preparacion(data){
    $.ajax({
            type: 'GET',
            url: 'get_labor',
            data: {'id' : data.fields.labor},
            success: function (labor) {

                    l = '<td>'+labor+'</td>';
                    area = '<td>'+data.fields.area_lote+'</td>';
                    fecha = '<td>'+data.fields.fecha_preparacion+'</td>';
                    precio_hectarea = '<td>'+data.fields.precio+'</td>';
                    subtotal = '<td>'+data.fields.subtotal+'</td>';

                    editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_preparacion('+data.pk+')" type="button">Ir</button></td>';
                    borrar = '<td><button class="btn btn-success col-xs-4" onclick="borrar_preparacion_fisica('+data.pk+')" type="button">Ir</button></td>';
                    fila = '<tr>'+l+area+fecha+precio_hectarea+subtotal+editar+borrar+'</tr>';

                if(data.fields.tipoMedida === '1')
                   $('#body_preparacion_area').append(fila);
                else
                    $('#body_preparacion_mtr').append(fila);



            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function borrar_preparacion_fisica(id){
    $.ajax({
            type: 'GET',
            url: 'borrar_preparacion_fisica',
            data: {'id':id},
            success: function (data) {

                if (data === 'error'){
                    UIkit.notify({
                        message : 'Upps! algo salio mal con el proceso',
                        status  : 'danger',
                        timeout : 3000,
                        pos:'top-center'
                    });
                }
                else{
                    UIkit.notify({
                        message : 'Preparación Fisica de Suelos Borrada Exitosamente',
                        status  : 'success',
                        timeout : 3000,
                        pos:'top-center'
                    });
                    get_preparaciones_fisicas(data);
                }
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}


function new_preparacion(tipo){
    hacienda_editar = tipo;
    $("#cuerpo").load( "../static/html/registro_preparacion.html");
}


function editar_preparacion(id){
    hacienda_editar = id;
    $("#cuerpo").load( "../static/html/editar_preparacion.html");
}

