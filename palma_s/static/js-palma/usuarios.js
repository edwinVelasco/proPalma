/**
 * Created by diseraca on 8/04/15.
 */

function get_usuario(){
    texto = '<br/><p class="login-logo">Listado de los palmicultores</p><br/>'
    tabla = '<div id="lista_palmicultores" class="register-page"><table class="table table-hover">';
    thead = '<thead>      <th>Apellidos</th> <th>Nombres</th> <th>N° Documento</th> <th>Email</th> <th>Telefonos</th> <th>Usuario</th>  <th>Editar</th> <th>Contraseña</th> </thead>';
    tbody = '<tbody id="body_palmicultores"></tbody>';
    tabla += thead + tbody + '</table> </div>';
    $("#cuerpo").html(texto+tabla);

    $.ajax({
            type: "GET",
            url: "get_palmicultores",
            data: "",
            success: function (data) {
                console.log(data);
                if (data.length == 0)
                {
                    UIkit.notify({
                        message : 'No hay palmicultores registradas',
                        status  : 'warning',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else{
                    html = '';
                    for (i=0; i< data.length; i++)
                    {

                        apellidos = '<td>'+data[i].fields.apellidos+'</td>';
                        nombres = '<td>'+data[i].fields.nombres+'</td>';
                        documento = '<td>'+data[i].fields.documento+'</td>';
                        email = '<td>'+data[i].fields.email+'</td>';
                        telefonos = '<td>'+data[i].fields.telefono+'</td>';

                        if (data[i].fields.activo == '1')
                            desactivar = '<td><button class="btn btn-success col-xs-6" onclick="desactivar_palmicultor('+data[i].pk+')" type="button">Desactivar</button></td>';
                        else
                            desactivar = '<td><button class="btn btn-success col-xs-4" onclick="desactivar_palmicultor('+data[i].pk+')" type="button">Activar</button></td>';

                        editar = '<td><button class="btn btn-success col-xs-4" onclick="editar_palmicultor_admin('+data[i].pk+')" type="button">Ir</button></td>';
                        contrasena = '<td><button class="btn btn-success col-xs-6" onclick="resetear_pass('+data[i].pk+')" type="button">Restaurar</button></td>';
                        fila = '<tr>'+apellidos+nombres+documento+email+telefonos+desactivar+editar+contrasena+'</tr>';
                        console.log(fila);
                        $('#body_palmicultores').append(fila);
                    }


                }


            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function desactivar_palmicultor(id){
    $.ajax({
            type: "GET",
            url: "activar_desactivar",
            data: {'id':id},
            success: function (data) {
                if(data === '1')
                {
                    UIkit.notify({
                        message : 'Activado con exito',
                        status  : 'success',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                if(data === '2')
                {
                    UIkit.notify({
                        message : 'Desactivado con exito',
                        status  : 'success',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                get_filtro_palmicultores();

            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function editar_palmicultor_admin(id){
    hacienda_editar = id;
    $("#cuerpo").load( "../static/html/editar_palmicultor_admin.html");
}

function resetear_pass(id){
    $.ajax({
            type: "GET",
            url: "reset_pass",
            data: {'id':id},
            success: function (data) {
                if(data === 'ok')
                {
                    UIkit.notify({
                        message : 'Contraseña Restaurada con Exito, Recuerde que es el Mismo Número de Documento',
                        status  : 'success',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                else
                {
                    UIkit.notify({
                        message : 'Desactivado con exito',
                        status  : 'success',
                        timeout : 4000,
                        pos:'top-center'
                    });
                }
                get_filtro_palmicultores();

            },
            error: function(data) {
                console.log(data)
            }
        });
        return false;
}

function get_filtro_palmicultores(){
    $("#cuerpo").load( "../static/html/filtro_admin.html");
}