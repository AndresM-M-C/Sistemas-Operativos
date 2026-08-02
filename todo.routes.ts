import { Request, Response, } from 'express';
import { Router } from 'express';
import { leer, crear, actualizar, eliminar } from './todo.controller';
import { todo } from 'node:test';

const todoRoutes = Router();

todoRoutes.get("/leer", async function (req: Request, res: Response) {
    const resultado = await leer()
    res.json(resultado)
})         //http://localhost:3000/pendientes/leer

todoRoutes.post("/", async function (req: Request, res: Response) {
    const pendiente = req.body.pendiente;
    const respuesta = await crear(pendiente);
    res.json(respuesta);

})     //http://localhost:3000/pendientes/

todoRoutes.put("/:id", async function (req: Request, res: Response) {
    const id = req.params.id;
    const respuesta = await actualizar(id + "");
    res.json(respuesta);

})      //http://localhost:3000/pendientes/1

todoRoutes.delete("/:id", async function (req: Request, res: Response) {
    const { id } = req.params;
    const respuesta = await eliminar(id as string);
    res.json(respuesta);
})      //http://localhost:3000/pendientes/1


export default todoRoutes