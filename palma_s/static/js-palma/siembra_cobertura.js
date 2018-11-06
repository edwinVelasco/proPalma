/**
 * Created by edwin on 31/03/15.
 */

/**
 * Created by edwin on 30/05/15.
 */
/**
 * Created by edwin on 15/05/15.
 */
function get_siembra_cobertura(){

    texto = '<br/><p class="login-logo">Listado de Siembras de Coberturas</p><br/>'
    tabla = '<div id="lista_siembra_cobertura" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Insumo</th> <th>Cantidad Por Hectarea</th> <th>Area</th> <th>Unidad</th> <th>Precio por Unidad</th> <th>Fecha</th> <th>subtotal</th> <th>Editar</th> <th>Borrar</th></tr>    </thead>';
    tbody = '<tbody id="body_siembra_cobertura"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_siembra_cobertura()" type="button">Nueva</button></div></div> </br></br>';


    tabla_resultados = '<div class="register-page"><table class="table table-hover">';
    thead_resultados = '<thead>    <tr>    <th>Descripción</th> <th>Valor</th> </tr> </thead>';
    tbody_resultados = '<tbody id="resultados_siembra_cobertura"></tbody>';
    tabla_resultados += thead_resultados + tbody_resultados + '</table> </div>';

    $("#cuerpo").html(texto+tabla+boton_agregar+tabla_resultados);

    pintar_tabla_resultados_siembra_cobertura();

    $.ajax({
            type: "GET",
            url: "get_siembra_cobertura",
            data: '',
            success: function (data) {
                console.log(data);

                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay Siembras de Cobertura Registradas',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{

                    for (i=0; i< data.length; i++)
                    {
                        add_insumo_data_siembra_conertura(data[i]);
                    }
                }

            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function pintar_tabla_resultados_siembra_cobertura(){
    $.ajax({
            type: "GET",
            url: "totales_siembra_cobertura",
            data: '',
            success: function (data) {
                subtotal = '<tr> <td>Total Siembra de Cobertura</td><td>'+data+'</td></tr>';
                $('#resultados_siembra_cobertura').append(subtotal);

            },
            error: function(data) {
                console.log(data)
            }
        });
}

function add_insumo_data_siembra_conertura(data){
    $.ajax({
            type: 'GET',
            url: 'get_insumo',
            data: {'id' : data.fields.insumo},
            success: function (labor) {
                data.fields.insumo = labor;
                add_unidad_data_table_siembra_cobertura(data);
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function add_unidad_data_table_siembra_cobertura(data){
    $.ajax({
            type: 'GET',
            url: 'get_unidad',
            data: {'id' : data.fields.unidad},
            success: function (uni) {
                console.log(data);

                insumo = '<td>'+data.fields.insumo+'</td>';
                cantidad = '<td>'+data.fields.cantidad+'</td>';
                area = '<td>'+data.fields.area_lote+'</td>';
                unidad = '<td>'+uni+'</td>';
                precio_unidad = '<td>'+data.fields.precio_unidad+'</td>';
                fecha = '<td>'+data.fields.fecha_siembra+'</td>';
                subtotal = '<td>'+data.fields.subtotal+'</td>';

                editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_siembra_cobertura('+data.pk+')" type="button">Ir</button></td>';
                borrar = '<td><button class="btn btn-success col-xs-4" onclick="borrar_siembra_cobertura('+data.pk+')" type="button">Ir</button></td>';

                fila = '<tr>'+insumo+cantidad+area+unidad+precio_unidad+fecha+subtotal+editar+borrar+'</tr>';

                $('#body_siembra_cobertura').append(fila);
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function borrar_siembra_cobertura(id){
    $.ajax({
            type: 'GET',
            url: 'borrar_siembra_cobertura',
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
                        message : 'Siembra de Cobertura Borrada Exitosamente',
                        status  : 'success',
                        timeout : 3000,
                        pos:'top-center'
                    });
                    get_siembra_cobertura();
                }
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}


function new_siembra_cobertura(tipo){
    hacienda_editar = tipo;
    $("#cuerpo").load( "../static/html/registro_siembra_cobertura.html");
}


function editar_siembra_cobertura(id){
    hacienda_editar = id;
    $("#cuerpo").load( "../static/html/editar_siembra_cobertura.html");
}


