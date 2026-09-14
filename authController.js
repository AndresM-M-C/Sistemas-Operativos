
import { pool } from '../config/db.js';

export const registrarUsuario = async (req, res) => {
    const { nombre, password, idRol } = req.body;
    try {
        const [result] = await pool.query(
            'INSERT INTO Usuario (nombre, password, idRol) VALUES (?, ?, ?)',
            [nombre, password, idRol]
        );
        res.status(201).json({ mensaje: 'Usuario registrado', idUsuario: result.insertId });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

export const iniciarSesion = async (req, res) => {
    const { nombre, password } = req.body;
    try {
        const [rows] = await pool.query('SELECT * FROM Usuario WHERE nombre = ? AND password = ?', [nombre, password]);
        if (rows.length > 0) {
            res.status(200).json({ mensaje: 'Login correcto', usuario: rows[0] });
        } else {
            res.status(401).json({ error: 'Credenciales incorrectas' });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

export const agregarTarjeta = async (req, res) => {
    const { noTarjeta, propietario, idUsuario } = req.body;
    try {
        const [result] = await pool.query(
            'INSERT INTO Tarjeta (NoTarjeta, Propietario, idUsuario) VALUES (?, ?, ?)',
            [noTarjeta, propietario, idUsuario]
        );
        res.status(201).json({ mensaje: 'Tarjeta agregada', idTarjeta: result.insertId });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

export const eliminarTarjeta = async (req, res) => {
    const { idTarjeta } = req.params;
    try {
        await pool.query('DELETE FROM Tarjeta WHERE idTarjeta = ?', [idTarjeta]);
        res.status(200).json({ mensaje: 'Tarjeta eliminada' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

export const obtenerTarjetas = async (req, res) => {
    const { idUsuario } = req.params;
    try {
        const [rows] = await pool.query('SELECT * FROM Tarjeta WHERE idUsuario = ?', [idUsuario]);
        res.status(200).json(rows);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};