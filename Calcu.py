import streamlit as st
import numpy as np
import sympy as sp

# Configuración adaptada a móviles (pantalla ajustada)
st.set_page_config(page_title="Calculadora Numérica", layout="centered")

st.title("🧮 Métodos Numéricos")
st.write("Selecciona un método e ingresa los datos de tu problema.")

# -----------------------------------------------------------------------------
# FUNCIONES DE MÉTODOS NUMÉRICOS
# -----------------------------------------------------------------------------

def evaluar_funcion(expr_str, valor):
    x = sp.symbols('x')
    expr = sp.sympify(expr_str)
    return float(expr.subs(x, valor))

def metodo_trapecio(f_str, a, b, n):
    h = (b - a) / n
    suma = evaluar_funcion(f_str, a) + evaluar_funcion(f_str, b)
    for i in range(1, n):
        suma += 2 * evaluar_funcion(f_str, a + i * h)
    return (h / 2) * suma

def metodo_simpson_13(f_str, a, b, n):
    if n % 2 != 0:
        raise ValueError("El número de subintervalos (n) debe ser PAR.")
    h = (b - a) / n
    suma = evaluar_funcion(f_str, a) + evaluar_funcion(f_str, b)
    for i in range(1, n):
        if i % 2 == 0:
            suma += 2 * evaluar_funcion(f_str, a + i * h)
        else:
            suma += 4 * evaluar_funcion(f_str, a + i * h)
    return (h / 3) * suma

def metodo_simpson_38(f_str, a, b, n):
    if n % 3 != 0:
        raise ValueError("El número de subintervalos (n) debe ser múltiplo de 3.")
    h = (b - a) / n
    suma = evaluar_funcion(f_str, a) + evaluar_funcion(f_str, b)
    for i in range(1, n):
        if i % 3 == 0:
            suma += 2 * evaluar_funcion(f_str, a + i * h)
        else:
            suma += 3 * evaluar_funcion(f_str, a + i * h)
    return (3 * h / 8) * suma

def diferenciacion_numerica(f_str, x0, h, tipo):
    if tipo == "Hacia adelante (Forward)":
        return (evaluar_funcion(f_str, x0 + h) - evaluar_funcion(f_str, x0)) / h
    elif tipo == "Hacia atrás (Backward)":
        return (evaluar_funcion(f_str, x0) - evaluar_funcion(f_str, x0 - h)) / h
    elif tipo == "Central":
        return (evaluar_funcion(f_str, x0 + h) - evaluar_funcion(f_str, x0 - h)) / (2 * h)

def interpolacion_lagrange(X, Y, x_interp):
    n = len(X)
    resultado = 0.0
    for i in range(n):
        termino = Y[i]
        for j in range(n):
            if i != j:
                termino *= (x_interp - X[j]) / (X[i] - X[j])
        resultado += termino
    return resultado

# -----------------------------------------------------------------------------
# INTERFAZ OPTIMIZADA PARA MÓVIL (Menús desplegables superiores)
# -----------------------------------------------------------------------------

# Menú principal en la pantalla principal (no en el sidebar)
categoria = st.selectbox(
    "Categoría del problema:",
    ["Integración Numérica", "Diferenciación Numérica", "Interpolación Numérica"]
)

st.write("---")

if categoria == "Integración Numérica":
    st.subheader("📌 Integración Numérica")
    
    metodo = st.selectbox("Método de Integración:", ["Trapecio", "Simpson 1/3", "Simpson 3/8"])
    f_str = st.text_input("Función f(x):", "x**2 + 2*x + 1")
    
    # Inputs organizados en columnas más pequeñas para pantalla móvil
    c1, c2, c3 = st.columns(3)
    with c1:
        a = st.number_input("Lim inf (a):", value=0.0)
    with c2:
        b = st.number_input("Lim sup (b):", value=2.0)
    with c3:
        n = st.number_input("Intervalos (n):", value=6, step=1)
    
    if st.button("Calcular Integral", use_container_width=True):
        try:
            if metodo == "Trapecio":
                res = metodo_trapecio(f_str, a, b, n)
            elif metodo == "Simpson 1/3":
                res = metodo_simpson_13(f_str, a, b, n)
            elif metodo == "Simpson 3/8":
                res = metodo_simpson_38(f_str, a, b, n)
            
            st.success(f"Resultado ({metodo}):\n\n### {res:.6f}")
        except Exception as e:
            st.error(f"Error: {e}")

elif categoria == "Diferenciación Numérica":
    st.subheader("📌 Diferenciación Numérica")
    
    tipo_dif = st.selectbox("Tipo de diferencia:", ["Central", "Hacia adelante (Forward)", "Hacia atrás (Backward)"])
    f_str = st.text_input("Función f(x):", "sin(x) + cos(x)")
    
    c1, c2 = st.columns(2)
    with c1:
        x0 = st.number_input("Punto (x0):", value=1.0)
    with c2:
        h = st.number_input("Paso (h):", value=0.01, format="%.4f")
    
    if st.button("Calcular Derivada", use_container_width=True):
        try:
            res = diferenciacion_numerica(f_str, x0, h, tipo_dif)
            st.success(f"Derivada aproximada:\n\n### {res:.6f}")
        except Exception as e:
            st.error(f"Error: {e}")

elif categoria == "Interpolación Numérica":
    st.subheader("📌 Interpolación de Lagrange")
    
    x_input = st.text_input("Valores de X (separados por comas):", "1, 2, 3, 4")
    y_input = st.text_input("Valores de Y (separados por comas):", "1, 4, 9, 16")
    x_interp = st.number_input("Valor X a interpolar:", value=2.5)
    
    if st.button("Calcular Interpolación", use_container_width=True):
        try:
            X = [float(i.strip()) for i in x_input.split(",")]
            Y = [float(i.strip()) for i in y_input.split(",")]
            
            if len(X) != len(Y):
                st.error("X e Y deben tener la misma cantidad de datos.")
            else:
                res = interpolacion_lagrange(X, Y, x_interp)
                st.success(f"Resultado interpolado:\n\n### Y = {res:.6f}")
        except Exception as e:
            st.error(f"Error en los datos: {e}")