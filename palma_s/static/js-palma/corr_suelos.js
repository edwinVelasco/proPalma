/**
 * Created by edwin on 15/05/15.
 */
function get_correcciones_suelo(){

    texto = '<br/><p class="login-logo">Listado de Correcciones de Suelo</p><br/>'
    tabla = '<div id="lista_cor_suelos" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Enmienda</th> <th>Cantidad</th> <th>$ de Enmienda</th> <th>Subtotal</th> <th>$ de Aplicación</th> <th>Editar</th> <th>Borrar</th></tr>    </thead>';
    tbody = '<tbody id="body_correccion"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_correccion()" type="button">Nueva</button></div></div> </br></br>'

    tabla_resultados = '<div id="lista_cor_suelos" class="register-page"><table class="table table-hover">';
    thead_resultados = '<thead>    <tr>    <th>Descripción</th> <th>Valor</th> </tr> </thead>';
    tbody_resultados = '<tbody id="resultados_correcciones"></tbody>';
    tabla_resultados += thead_resultados + tbody_resultados + '</table> </div>';

    $("#cuerpo").html(texto+tabla+boton_agregar+tabla_resultados);

    pintar_tabla_resultados();

    $.ajax({
            type: "GET",
            url: "get_correciones",
            data: '',
            success: function (data) {
                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay Correcciones registradas',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{

                    for (i=0; i< data.length; i++)
                    {
                        add_fila_correccion(data[i]);
                    }
                }


            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function pintar_tabla_resultados(){
    $.ajax({
            type: "GET",
            url: "totales_correccion_suelos",
            data: '',
            success: function (data) {
                datos = data.split(',');
                subtotal = '<tr> <td>Subtotal Corrección de Suelos</td><td>'+datos[0]+'</td></tr>';
                $('#resultados_correcciones').append(subtotal);
                aplicacion = '<tr> <td>Subtotal Costos Aplicación</td><td>'+datos[1]+'</td></tr>';
                $('#resultados_correcciones').append(aplicacion);
                total = '<tr> <td>Total Corrección de Suelos</td><td>'+datos[2]+'</td></tr>';
                $('#resultados_correcciones').append(total);

            },
            error: function(data) {
                console.log(data)
            }
        });
}

function add_fila_correccion(data){
    $.ajax({
            type: 'GET',
            url: 'get_enmienda',
            data: {'id' : data.fields.enmienda},
            success: function (enmienda) {

                en = '<td>'+enmienda+'</td>';
                cantidad = '<td>'+data.fields.cantidad+'</td>';
                precio_en = '<td>'+data.fields.precio_enmienda+'</td>';
                subtotal = '<td>'+data.fields.subtotal+'</td>';
                precio_apli = '<td>'+data.fields.precio_aplicadaEnmienda+'</td>';
                editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_correccion('+data.pk+')" type="button">Ir</button></td>';
                borrar = '<td><button class="btn btn-success col-xs-4" onclick="borrar_correccion('+data.pk+')" type="button">Ir</button></td>';
                fila = '<tr>'+en+cantidad+precio_en+subtotal+precio_apli+editar+borrar+'</tr>';
                $('#body_correccion').append(fila);
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function new_correccion(){
    $("#cuerpo").load( "../static/html/registro_correccion_suelo.html");
}

function borrar_correccion(id){
    $.ajax({
            type: 'GET',
            url: 'borrar_correccion',
            data: {'id':id},
            success: function (data) {

                if (data === 'error'){
                    UIkit.notify({
                        message : 'Upps! algo salio mal con el proceso',
                        status  : 'danger',
                        timeout : 5000,
                        pos:'top-center'
                    });
                }
                else{
                    UIkit.notify({
                        message : 'Correccion de Suelo Borrada Exitosamente',
                        status  : 'success',
                        timeout : 5000,
                        pos:'top-center'
                    });
                    get_correcciones_suelo(data);
                }
            },
            error: function(data) {
                alert(data);
                console.log(data)
            }
        });
        return false;
}

function editar_correccion(id){
    hacienda_editar = id;
    $("#cuerpo").load( "../static/html/editar_correccion_suelo.html");
}