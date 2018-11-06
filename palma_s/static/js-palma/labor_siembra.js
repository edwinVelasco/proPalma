/**
 * Created by edwin on 7/06/15.
 */

function get_labores_siembra(){
    texto = '<br/><p class="login-logo">Listado de Costos de Labores de Siembra</p><br/>'
    tabla = '<div id="lista_labores_siembra" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Tipo de Labor</th> <th>Cantidad Por Hectarea</th> <th>Area</th> <th>Unidad</th> <th>Precio por Unidad</th> <th>Fecha</th> <th>subtotal</th> <th>Editar</th> <th>Borrar</th></tr>    </thead>';
    tbody = '<tbody id="body_labores_siembra"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_labor_siembra()" type="button">Nueva</button></div></div> </br></br>';


    tabla_resultados = '<div class="register-page"><table class="table table-hover">';
    thead_resultados = '<thead>    <tr>    <th>Descripción</th> <th>Valor</th> </tr> </thead>';
    tbody_resultados = '<tbody id="resultados_labores_siembra"></tbody>';
    tabla_resultados += thead_resultados + tbody_resultados + '</table> </div>';

    $("#cuerpo").html(texto+tabla+boton_agregar+tabla_resultados);

    pintar_tabla_resultados_labor_siembra();

    $.ajax({
            type: "GET",
            url: "get_labores_siembra",
            success: function (data) {
                console.log(data);

                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No Hay Labores de Siembra Registrados',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{
                    for (i=0; i< data.length; i++)
                    {
                        add_labor_data_labor_siembra(data[i]);
                    }
                }

            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function pintar_tabla_resultados_labor_siembra(){
    $.ajax({
            type: "GET",
            url: "get_total_labores_siembra",
            success: function (data) {
                subtotal = '<tr> <td>Total Labores de Siembra de Palma</td><td>'+data+'</td></tr>';
                $('#resultados_labores_siembra').append(subtotal);
            },
            error: function(data) {
                console.log(data)
            }
        });
}

function add_labor_data_labor_siembra(data){
    $.ajax({
            type: 'GET',
            url: 'get_labor',
            data: {'id' : data.fields.labor},
            success: function (res) {
                data.fields.labor = res;
                add_unidad_data_table_labor_siembra(data);
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function add_unidad_data_table_labor_siembra(data){
    $.ajax({
            type: 'GET',
            url: 'get_unidad',
            data: {'id' : data.fields.unidad},
            success: function (uni) {
                item = '<td>'+data.fields.labor+'</td>';
                cantidad = '<td>'+data.fields.cantidad_laboradas+'</td>';
                area = '<td>'+data.fields.area_labor+'</td>';
                unidad = '<td>'+uni+'</td>';
                precio_unidad = '<td>'+data.fields.precio_labor+'</td>';
                fecha = '<td>'+data.fields.fecha_labor+'</td>';
                subtotal = '<td>'+data.fields.subtotal+'</td>';

                editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_labor_siembra('+data.pk+')" type="button">Ir</button></td>';
                borrar = '<td><button class="btn btn-success col-xs-4" onclick="borrar_labor_siembra('+data.pk+')" type="button">Ir</button></td>';

                fila = '<tr>'+item+cantidad+area+unidad+precio_unidad+fecha+subtotal+editar+borrar+'</tr>';

                $('#body_labores_siembra').append(fila);
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function borrar_labor_siembra(id){
    $.ajax({
            type: 'GET',
            url: 'borrar_labor_siembra',
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
                        message : 'Labor de Siembra Borrado Exitosamente',
                        status  : 'success',
                        timeout : 3000,
                        pos:'top-center'
                    });
                    get_labores_siembra();
                }
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function new_labor_siembra(tipo){
    hacienda_editar = tipo;
    $("#cuerpo").load( "../static/html/registro_labor_siembra.html");
}

function editar_labor_siembra(id){
    hacienda_editar = id;
    $("#cuerpo").load( "../static/html/editar_labor_siembra.html");
}


