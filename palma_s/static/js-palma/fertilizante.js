/**
 * Created by edwin on 25/05/15.
 */


function get_fertilizantes(){
    texto = '<br/><p class="login-logo">Listado de Fertilizantes</p><br/>'
    tabla = '<div id="lista_fertilizantes" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Nombre</th> <th>Editar</th> </tr>    </thead>';
    tbody = '<tbody id="body_fertilizantes"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_fertilizante()" type="button">Nuevo</button></div></div>'

    $("#cuerpo").html(texto+tabla+boton_agregar);

    $.ajax({
            type: "GET",
            url: "get_fertilizantes",
            data: "",
            success: function (data) {
                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay Fertilizantes Registrados',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{
                    for (i=0; i< data.length; i++)
                    {
                        nombre = '<td>'+data[i].fields.fertilizante+'</td>';
                        editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_fertilizante('+data[i].pk+')" type="button">Editar</button></td>';
                        fila = '<tr>'+nombre+editar+'</tr>';
                        $('#body_fertilizantes').append(fila);
                    }
                }


            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function new_fertilizante(){
    $("#cuerpo").load( "../static/html/registro_fertilizante.html");
}

function editar_fertilizante(pk){
    hacienda_editar = pk;
    $("#cuerpo").load( "../static/html/editar_fertilizante.html");
}