import mongoose = require("mongoose");

const PendientesSchema = new mongoose.Schema({
    descripcion: { type: String, required: true },
    estado: {
        type: String, required: true,
        enum: ["Pendiente", "Completado"],
        default: "Pendiente"
    }
})

export const TODO = mongoose.model("Pendientes", PendientesSchema);
