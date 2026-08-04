console.log("prueba")
import mongoose from "mongoose";
import express from "express";
import cors from "cors";
import todoRoutes from "./todo.routes";

const app = express();
app.use(cors());
app.use(express.json())
app.use("/pendientes", todoRoutes)



mongoose.connect("mongodb://localhost:27017/")
    .then(() => {
        app.listen(3000, () =>
            console.log("Conectado y corriendo en el puerto http://localhost:3000"));
    }).catch(error => console.log("error: " + error))



