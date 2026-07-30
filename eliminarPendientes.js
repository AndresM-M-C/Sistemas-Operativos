async function eliminar(id) {
    try {
        const respuesta = await fetch(URL + "/" + id, { //
            method: "DELETE",
            headers: { "Content-type": "application/json" }
        })
        if (respuesta.status == 200) {
            const resultado = await respuesta.json();
            Swal.fire({
                icon: "success",
                position: "bottom-end",
                text: resultado.message,
                showConfirmButton: false,
                timer: 1000
            });
            obtenerTareas();
        }
    } catch (error) {

    }
}