const formulario = document.getElementById("formulario");
const input = document.getElementById("descripcion");

async function crearPendiente(evt) {
    evt.preventDefault();
    Swal.fire("prueba")
    const descripcion = input.value;

    try {
        const respuesta = await fetch(URL, {
            method: "POST",
            headers: { "Content-type": "application/json" },
            body: JSON.stringify({
                pendiente: descripcion
            })
        });
        if (respuesta.status == 200) {
            input.value = "";
            obtenerTareas();
            Swal.fire({
                position: "bottom-end",
                icon: "success",
                text: "Agregado correctamente",
                showConfirmButton: false,
                timer: 1000
            });
        } else {

        }

    } catch (error) {
        console.error(error);
        Swal.fire({
            position: "bottom-end",
            icon: "error",
            text: "Intenta de nuevo mas tarde",
            showConfirmButton: false,
            timer: 1000
        });
    }
}



formulario.addEventListener("submit", crearPendiente);