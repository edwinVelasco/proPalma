/**
 * Created by edwin on 1/06/15.
 */

function get_insumos(){
    texto = '<br/><p class="login-logo">Listado de Insumos</p><br/>'
    tabla = '<div id="lista_insumos" class="register-page"><table class="table table-hover">';
    thead = '<thead>    <tr>    <th>Nombre</th> <th>Tipo de Insumo</th> <th>Editar</th> </tr>    </thead>';
    tbody = '<tbody id="body_insumos"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    boton_agregar = '<div class="row"><div class="col-xs-6"></div><div class="col-xs-6"><button class="btn btn-success col-xs-3" onclick="new_insumo()" type="button">Nueva</button></div></div>'

    $("#cuerpo").html(texto+tabla+boton_agregar);

    $.ajax({
            type: "GET",
            url: "get_insumos",
            data: "",
            success: function (data) {
                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay Insumos Registradas',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{
                    for (i=0; i< data.length; i++)
                    {
                        nombre = '<td>'+data[i].fields.insumo+'</td>';

                        tipo = '<td>Coberturas</td>';
                        if (data[i].fields.tipo == '1')
                            tipo = '<td>Variedad de Palma</td>';

                        editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_insumo('+data[i].pk+')" type="button">Editar</button></td>';
                        fila = '<tr>'+nombre+tipo+editar+'</tr>';
                        $('#body_insumos').append(fila);
                    }
                }


            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;

}

function new_insumo(){
    $("#cuerpo").load( "../static/html/registro_insumo.html");
}

function editar_insumo(pk){
    hacienda_editar = pk;
    $("#cuerpo").load( "../static/html/editar_insumo.html");
}