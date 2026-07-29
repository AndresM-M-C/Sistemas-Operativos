const URL = "http://localhost:3000/pendientes";

async function obtenerTareas() {
    try {
        const respuestaServidor = await fetch(URL + "/leer");

        if (respuestaServidor.status === 200) {
            const datosFinales = await respuestaServidor.json();

            const tabla = document.getElementById("tabla");
            tabla.innerHTML = "";

            datosFinales.forEach(pendiente => {
                tabla.innerHTML += `
                <div class="fila">
                    <div class="columna">${pendiente.descripcion}</div>
                    <div class="columna">${pendiente.estado}</div>
                    <div class="columna">
                        <button onclick="actualizar('${pendiente._id}')" class="btn-completar">
                            ${pendiente.estado === "Pendiente" ? "Completar" : "Pendiente"}
                        </button>

                        <button onclick="eliminar('${pendiente._id}')" class="btn-eliminar">
                            Eliminar
                        </button>
                    </div>
                </div>
                `;
            });
        }

    } catch (error) {
        alert("Ocurrió un error al cargar los datos");
    }
}

obtenerTareas();