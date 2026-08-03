/**
 * crear el pendiente
 * leer el pendiente 
 * actualizar el estado
 * eliminar el pendiente completado
 */

import { TODO } from "./TODO";

export async function crear(pendiente: string) {
    const nuevoPendiente = await TODO.create({
        descripcion: pendiente
    })
    return nuevoPendiente;
}

export async function leer() {
    const todosLosPendientes = await TODO.find({});
    return todosLosPendientes;
}

export async function actualizar(_id: string) {
    const tareaGuardada = await TODO.findOne({ _id })
    if (!tareaGuardada) {
        return { message: "TAREA NO ENCONTRADA" }
    }

    const datoModficado = await TODO.updateOne({ _id }, {
        estado: tareaGuardada.estado == "Pendiente" ?
            "Completado" : "Pendiente"
    })
    return datoModficado
}
export async function eliminar(_id: string) {
    const pendienteAEliminar = await TODO.findByIdAndDelete(_id)
    if (pendienteAEliminar) return { message: "Eliminado" }
    else return { message: "No encontrado" }
}
