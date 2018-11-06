/**
 * Created by edwin on 29/05/15.
 */
/**
 * Created by edwin on 25/05/15.
 */
function get_labores(){
    texto = '<br/><p class="login-logo">Listado de Labores</p><br/>'
    tabla = '<div id="lista_labores" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Nombre</th> <th>Tipo de Labor</th> <th>Editar</th> </tr>    </thead>';
    tbody = '<tbody id="body_labores"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_labor()" type="button">Nuevo</button></div></div>';

    $("#cuerpo").html(texto+tabla+boton_agregar);

    $.ajax({
            type: "GET",
            url: "get_labores",
            data: "",
            success: function (data) {
                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay Labores Registrados',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{
                    for (i=0; i< data.length; i++)
                    {
                        nombre = '<td>'+data[i].fields.labor+'</td>';
                        tipo = "Area";
                        if (data[i].fields.tipo === '0')
                        {
                            tipo = "Metro Lineal";
                        }
                        else if (data[i].fields.tipo === '2')
                        {
                            tipo = "Labores de Siembra";
                        }
                        else if (data[i].fields.tipo === '3')
                        {
                            tipo = "Otros Labores";
                        }
                        tipo = '<td>'+tipo+'</td>';
                        editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_labor('+data[i].pk+')" type="button">Ir</button></td>';
                        fila = '<tr>'+nombre+tipo+editar+'</tr>';
                        $('#body_labores').append(fila);
                    }
                }


            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}


function new_labor(){
    $("#cuerpo").load( "../static/html/registro_labor.html");
}

function editar_labor(pk){
    hacienda_editar = pk;
    $("#cuerpo").load( "../static/html/editar_labor.html");
}