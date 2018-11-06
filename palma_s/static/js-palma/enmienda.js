/**
 * Created by edwin on 15/05/15.
 */

function get_enmiendas(){
    texto = '<br/><p class="login-logo">Listado de Enmiendas</p><br/>'
    tabla = '<div id="lista_haciendas" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Nombre</th> <th>Editar</th> </tr>    </thead>';
    tbody = '<tbody id="body_enmiendas"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_enmienda()" type="button">Nueva</button></div></div>'

    $("#cuerpo").html(texto+tabla+boton_agregar);

    $.ajax({
            type: "GET",
            url: "get_enmiendas",
            data: "",
            success: function (data) {
                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay Enmiendas Registradas',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{
                    for (i=0; i< data.length; i++)
                    {
                        nombre = '<td>'+data[i].fields.enmienda+'</td>';
                        editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_enmienda('+data[i].pk+')" type="button">Editar</button></td>';
                        fila = '<tr>'+nombre+editar+'</tr>';
                        $('#body_enmiendas').append(fila);
                    }
                }


            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}


function new_enmienda(){
    $("#cuerpo").load( "../static/html/registro_enmienda.html");
}

function editar_enmienda(pk){
    hacienda_editar = pk;
    $("#cuerpo").load( "../static/html/editar_enmienda.html");
}


