/**
 * Created by edwin on 25/05/15.
 */

function get_nivelacion_nutrientes(){
    texto = '<br/><p class="login-logo">Listado de Nivelación de Nitrientes</p><br/>'
    tabla = '<div id="lista_niv_nitri" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Fertilizante</th> <th>Cantidad</th> <th>$ del Fertilizante</th> <th>Subtotal</th> <th>$ de Aplicación</th> <th>Editar</th> <th>Borrar</th></tr>    </thead>';
    tbody = '<tbody id="body_nivelacion_nutrientes"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_nivelacion()" type="button">Nueva</button></div></div> </br></br>'

    tabla_resultados = '<div id="lista_cor_suelos" class="register-page"><table class="table table-hover">';
    thead_resultados = '<thead>    <tr>    <th>Descripción</th> <th>Valor</th> </tr> </thead>';
    tbody_resultados = '<tbody id="resultados_nivelaciones"></tbody>';
    tabla_resultados += thead_resultados + tbody_resultados + '</table> </div>';

    $("#cuerpo").html(texto+tabla+boton_agregar+tabla_resultados);

    pintar_tabla_resultados_nivelacion();

    $.ajax({
            type: "GET",
            url: "get_nivelaciones",
            data: '',
            success: function (data) {
                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay Nivelación de Nutrientes Registradas',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{

                    for (i=0; i< data.length; i++)
                    {
                        add_fila_nivelacion(data[i]);
                    }
                }

            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function pintar_tabla_resultados_nivelacion(){
    $.ajax({
            type: "GET",
            url: "totales_nivelacione_nutrientes",
            data: '',
            success: function (data) {
                datos = data.split(',');
                subtotal = '<tr> <td>Subtotal Nivelación Nutrientes</td><td>'+datos[0]+'</td></tr>';
                $('#resultados_nivelaciones').append(subtotal);
                aplicacion = '<tr> <td>Subtotal Costos Aplicación</td><td>'+datos[1]+'</td></tr>';
                $('#resultados_nivelaciones').append(aplicacion);
                total = '<tr> <td>Total Nivelación Nutrientes</td><td>'+datos[2]+'</td></tr>';
                $('#resultados_nivelaciones').append(total);

            },
            error: function(data) {
                console.log(data)
            }
        });
}

function add_fila_nivelacion(data){
    $.ajax({
            type: 'GET',
            url: 'get_fertilizante',
            data: {'id' : data.fields.fertilizantes},
            success: function (fertilizante) {

                fer = '<td>'+fertilizante+'</td>';
                cantidad = '<td>'+data.fields.cantidad+'</td>';
                precio_nut = '<td>'+data.fields.precio_nutriente+'</td>';
                subtotal = '<td>'+data.fields.subtotal+'</td>';
                precio_apli = '<td>'+data.fields.precio_aplicacion+'</td>';

                editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_nivelacion('+data.pk+')" type="button">Ir</button></td>';
                borrar = '<td><button class="btn btn-success col-xs-4" onclick="borrar_nivelacion('+data.pk+')" type="button">Ir</button></td>';
                fila = '<tr>'+fer+cantidad+precio_nut+subtotal+precio_apli+editar+borrar+'</tr>';
                $('#body_nivelacion_nutrientes').append(fila);
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function new_nivelacion(){
    $("#cuerpo").load( "../static/html/registro_nivelacion.html");
}

function borrar_nivelacion(id){
    $.ajax({
            type: 'GET',
            url: 'borrar_nivelacion',
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
                        message : 'Nivelación de Nutrientes Borrada Exitosamente',
                        status  : 'success',
                        timeout : 3000,
                        pos:'top-center'
                    });
                    get_nivelacion_nutrientes();
                }
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function editar_nivelacion(id){
    hacienda_editar = id;
    $("#cuerpo").load( "../static/html/editar_nivelacion.html");
}