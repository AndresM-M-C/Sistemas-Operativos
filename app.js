
import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import * as auth from './controllers/authController.js';
import * as prod from './controllers/productController.js';

const app = express();
const __dirname = path.dirname(fileURLToPath(import.meta.url));

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

app.post('/api/auth/register', auth.registrarUsuario);
app.post('/api/auth/login', auth.iniciarSesion);
app.post('/api/tarjetas', auth.agregarTarjeta);
app.get('/api/tarjetas/:idUsuario', auth.obtenerTarjetas);
app.delete('/api/tarjetas/:idTarjeta', auth.eliminarTarjeta);

app.get('/api/categorias', prod.obtenerCategorias);
app.post('/api/categorias', prod.crearCategoria);
app.delete('/api/categorias/:id', prod.eliminarCategoria);

app.get('/api/productos', prod.obtenerProductos);
app.post('/api/productos', prod.crearProducto);
app.put('/api/productos/:id', prod.actualizarProducto);
app.delete('/api/productos/:id', prod.eliminarProducto);

app.post('/api/comprar', prod.procesarCompra);
app.get('/api/compras/:idUsuario', prod.obtenerHistorialCompras);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 Servidor en http://localhost:${PORT}`));