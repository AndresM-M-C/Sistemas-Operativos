
import { pool } from '../config/db.js';

export const obtenerCategorias = async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM Categoria');
        res.status(200).json(rows);
    } catch (error) { res.status(500).json({ error: error.message }); }
};

export const crearCategoria = async (req, res) => {
    const { nombre } = req.body;
    try {
        const [resul] = await pool.query('INSERT INTO Categoria (Nombre) VALUES (?)', [nombre]);
        res.status(201).json({ idCategoria: resul.insertId, nombre });
    } catch (error) { res.status(500).json({ error: error.message }); }
};

export const eliminarCategoria = async (req, res) => {
    try {
        await pool.query('DELETE FROM Categoria WHERE idCategoria = ?', [req.params.id]);
        res.json({ mensaje: 'Categoría eliminada' });
    } catch (error) { res.status(500).json({ error: error.message }); }
};

export const obtenerProductos = async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM Productos');
        res.status(200).json(rows);
    } catch (error) { res.status(500).json({ error: error.message }); }
};

export const crearProducto = async (req, res) => {
    const { nombre, precio, stock, idCategoria, descripcion } = req.body;
    if (stock < 0) return res.status(400).json({ error: 'El stock debe ser 0 o más' });

    try {
        const [result] = await pool.query(
            'INSERT INTO Productos (Nombre, Precio, Stock, idCategoria, descripcion) VALUES (?, ?, ?, ?, ?)',
            [nombre, precio, stock, idCategoria, descripcion]
        );
        res.status(201).json({ mensaje: 'Producto creado', idProductos: result.insertId });
    } catch (error) { res.status(500).json({ error: error.message }); }
};

export const actualizarProducto = async (req, res) => {
    const { id } = req.params;
    const { nombre, precio, stock, idCategoria, descripcion } = req.body;
    if (stock < 0) return res.status(400).json({ error: 'El stock debe ser 0 o más' });

    try {
        await pool.query(
            'UPDATE Productos SET Nombre=?, Precio=?, Stock=?, idCategoria=?, descripcion=? WHERE idProductos=?',
            [nombre, precio, stock, idCategoria, descripcion, id]
        );
        res.json({ mensaje: 'Producto actualizado' });
    } catch (error) { res.status(500).json({ error: error.message }); }
};

export const eliminarProducto = async (req, res) => {
    try {
        await pool.query('DELETE FROM Productos WHERE idProductos = ?', [req.params.id]);
        res.json({ mensaje: 'Producto eliminado' });
    } catch (error) { res.status(500).json({ error: error.message }); }
};

export const procesarCompra = async (req, res) => {
    const { idUsuario, idTarjeta, items } = req.body;
    try {
        let totalVenta = 0;

        const [pedidoRes] = await pool.query('INSERT INTO Pedido (Estado, idUsuario) VALUES (?, ?)', [1, idUsuario]);
        const idPedido = pedidoRes.insertId;

        for (let item of items) {
            const [prodRows] = await pool.query('SELECT * FROM Productos WHERE idProductos = ?', [item.idProducto]);
            const prod = prodRows[0];

            if (prod.Stock < item.cantidad) throw new Error(`Stock insuficiente para ${prod.Nombre}`);

            const subtotal = prod.Precio * item.cantidad;
            totalVenta += subtotal;

            await pool.query('INSERT INTO DetalleCompra (idPedido, idProducto, cantidad, subtotal) VALUES (?, ?, ?, ?)',
                [idPedido, item.idProducto, item.cantidad, subtotal]);

            await pool.query('UPDATE Productos SET Stock = Stock - ? WHERE idProductos = ?', [item.cantidad, item.idProducto]);
        }

        await pool.query('INSERT INTO TicketCompra (idPedido, idTarjeta, Total) VALUES (?, ?, ?)', [idPedido, idTarjeta, totalVenta]);

        res.status(201).json({ mensaje: 'Compra realizada con éxito', idPedido, total: totalVenta });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

export const obtenerHistorialCompras = async (req, res) => {
    const { idUsuario } = req.params;
    try {
        const [rows] = await pool.query(
            `SELECT p.idPedido, p.Estado, t.Total FROM Pedido p 
       JOIN TicketCompra t ON p.idPedido = t.idPedido WHERE p.idUsuario = ?`, [idUsuario]
        );
        res.status(200).json(rows);
    } catch (error) { res.status(500).json({ error: error.message }); }
};