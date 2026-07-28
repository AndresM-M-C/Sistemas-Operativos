async function actualizar(id) {
    try {
        const respuesta = await fetch(URL + "/" + id, {
            method: "PUT",
            headers: { "Content-Type": "application/json" }
        })

        if (respuesta.status == 200) {
            obtenerTareas();
            Swal.fire({
                icon: "success",
                position: "top-center",
                text: "actualizado",
                showConfirmButton: false,
                timer: 1000
            });
        }
    } catch (error) {

    }
}