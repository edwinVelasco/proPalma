/**
 * Created by edwin on 5/06/15.
 */
/**
 * Created by edwin on 2/06/15.
 */
/**
 * Created by edwin on 31/03/15.
 */

/**
 * Created by edwin on 30/05/15.
 */
/**
 * Created by edwin on 15/05/15.
 */
function get_otros_ce(){

    texto = '<br/><p class="login-logo">Listado de Otros Costos de Establecimiento</p><br/>'
    tabla = '<div id="lista_otros_ce" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Otro Labor</th> <th>Cantidad Por Hectarea</th> <th>Area</th> <th>Unidad</th> <th>Precio por Unidad</th> <th>Fecha</th> <th>subtotal</th> <th>Editar</th> <th>Borrar</th></tr>    </thead>';
    tbody = '<tbody id="body_otros_ce"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_otro_ce()" type="button">Nueva</button></div></div> </br></br>';


    tabla_resultados = '<div class="register-page"><table class="table table-hover">';
    thead_resultados = '<thead>    <tr>    <th>Descripción</th> <th>Valor</th> </tr> </thead>';
    tbody_resultados = '<tbody id="resultados_otros_ce"></tbody>';
    tabla_resultados += thead_resultados + tbody_resultados + '</table> </div>';

    $("#cuerpo").html(texto+tabla+boton_agregar+tabla_resultados);

    pintar_tabla_resultados_otros_ce();

    $.ajax({
            type: "GET",
            url: "get_otros_costos_ce",
            data: '',
            success: function (data) {
                console.log(data);

                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No Hay Otros Costos de Establecimiento Registrados',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{

                    for (i=0; i< data.length; i++)
                    {
                        add_labor_data_otro_ce(data[i]);
                    }
                }

            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function pintar_tabla_resultados_otros_ce(){
    $.ajax({
            type: "GET",
            url: "get_total_otros_ce",
            data: '',
            success: function (data) {
                subtotal = '<tr> <td>Total Otros Costos de Establecimiento</td><td>'+data+'</td></tr>';
                $('#resultados_otros_ce').append(subtotal);

            },
            error: function(data) {
                console.log(data)
            }
        });
}

function add_labor_data_otro_ce(data){
    $.ajax({
            type: 'GET',
            url: 'get_labor',
            data: {'id' : data.fields.labor},
            success: function (res) {
                data.fields.labor = res;
                add_unidad_data_table_otro_ce(data);
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function add_unidad_data_table_otro_ce(data){

    $.ajax({
            type: 'GET',
            url: 'get_unidad',
            data: {'id' : data.fields.unidad},
            success: function (uni) {
                item = '<td>'+data.fields.labor+'</td>';
                cantidad = '<td>'+data.fields.cantidad+'</td>';
                area = '<td>'+data.fields.area+'</td>';
                unidad = '<td>'+uni+'</td>';
                precio_unidad = '<td>'+data.fields.precio+'</td>';
                fecha = '<td>'+data.fields.fecha_actividad+'</td>';
                subtotal = '<td>'+data.fields.subtotal+'</td>';

                editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_otro_ce('+data.pk+')" type="button">Ir</button></td>';
                borrar = '<td><button class="btn btn-success col-xs-4" onclick="borrar_otro_ce('+data.pk+')" type="button">Ir</button></td>';

                fila = '<tr>'+item+cantidad+area+unidad+precio_unidad+fecha+subtotal+editar+borrar+'</tr>';

                $('#body_otros_ce').append(fila);
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function borrar_otro_ce(id){
    $.ajax({
            type: 'GET',
            url: 'borrar_otro_ce',
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
                        message : 'Otro costo de Establecimiento Borrado Exitosamente',
                        status  : 'success',
                        timeout : 3000,
                        pos:'top-center'
                    });
                    get_otros_ce();
                }
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function new_otro_ce(tipo){
    hacienda_editar = tipo;
    $("#cuerpo").load( "../static/html/registro_otro_ce.html");
}

function editar_otro_ce(id){
    hacienda_editar = id;
    $("#cuerpo").load( "../static/html/editar_otro_ce.html");
}


