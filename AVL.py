class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 1

class ArbolAVL:
    # --- MÉTODOS DE IMPRESIÓN ---
    def imprimir_estructura(self, nodo, prefijo="", es_izq=None):
        """Imprime el árbol etiquetando explícitamente (I) Izquierda y (D) Derecha."""
        if nodo is not None:
            if es_izq is None:
                etiqueta = "(Raíz) "
            else:
                etiqueta = "├── (I) " if es_izq else "└── (D) "

            print(prefijo + etiqueta + f"[{nodo.valor}]")
            nuevo_prefijo = prefijo + ("│   " if es_izq else "    ")
            
            if nodo.izq or nodo.der:
                if nodo.izq:
                    self.imprimir_estructura(nodo.izq, nuevo_prefijo, True)
                else:
                    print(nuevo_prefijo + "├── (I) [Nulo]")

                if nodo.der:
                    self.imprimir_estructura(nodo.der, nuevo_prefijo, False)
                else:
                    print(nuevo_prefijo + "└── (D) [Nulo]")

    # --- PASO 1: BST NORMAL (SIN BALANCEAR) ---
    def insertar_bst(self, raiz, valor):
        """Inserta nodos en un árbol binario estándar sin realizar rotaciones."""
        if not raiz:
            return Nodo(valor)
        if valor < raiz.valor:
            raiz.izq = self.insertar_bst(raiz.izq, valor)
        elif valor > raiz.valor:
            raiz.der = self.insertar_bst(raiz.der, valor)
        return raiz

    # --- PASO 2: MÉTODOS Y BALANCEO AVL ---
    def obtener_altura(self, nodo):
        return nodo.altura if nodo else 0

    def obtener_balance(self, nodo):
        return self.obtener_altura(nodo.izq) - self.obtener_altura(nodo.der) if nodo else 0

    def rotacion_derecha(self, z):
        y = z.izq
        T3 = y.der
        y.der = z
        z.izq = T3
        z.altura = 1 + max(self.obtener_altura(z.izq), self.obtener_altura(z.der))
        y.altura = 1 + max(self.obtener_altura(y.izq), self.obtener_altura(y.der))
        return y

    def rotacion_izquierda(self, z):
        y = z.der
        T2 = y.izq
        y.izq = z
        z.der = T2
        z.altura = 1 + max(self.obtener_altura(z.izq), self.obtener_altura(z.der))
        y.altura = 1 + max(self.obtener_altura(y.izq), self.obtener_altura(y.der))
        return y

    def insertar_avl_paso_a_paso(self, raiz, valor):
        """Inserta e imprime las rotaciones necesarias al balancear."""
        if not raiz:
            return Nodo(valor)
        if valor < raiz.valor:
            raiz.izq = self.insertar_avl_paso_a_paso(raiz.izq, valor)
        elif valor > raiz.valor:
            raiz.der = self.insertar_avl_paso_a_paso(raiz.der, valor)
        else:
            return raiz

        raiz.altura = 1 + max(self.obtener_altura(raiz.izq), self.obtener_altura(raiz.der))
        balance = self.obtener_balance(raiz)

        # Rotaciones
        if balance > 1 and self.obtener_balance(raiz.izq) >= 0:
            print(f"\n  [!] DESBALANCE en nodo ({raiz.valor}) [Factor={balance}]. Rotación Simple Derecha (LL)...")
            return self.rotacion_derecha(raiz)

        if balance < -1 and self.obtener_balance(raiz.der) <= 0:
            print(f"\n  [!] DESBALANCE en nodo ({raiz.valor}) [Factor={balance}]. Rotación Simple Izquierda (RR)...")
            return self.rotacion_izquierda(raiz)

        if balance > 1 and self.obtener_balance(raiz.izq) < 0:
            print(f"\n  [!] DESBALANCE en nodo ({raiz.valor}) [Factor={balance}]. Rotación Doble Izquierda-Derecha (LR)...")
            raiz.izq = self.rotacion_izquierda(raiz.izq)
            return self.rotacion_derecha(raiz)

        if balance < -1 and self.obtener_balance(raiz.der) > 0:
            print(f"\n  [!] DESBALANCE en nodo ({raiz.valor}) [Factor={balance}]. Rotación Doble Derecha-Izquierda (RL)...")
            raiz.der = self.rotacion_derecha(raiz.der)
            return self.rotacion_izquierda(raiz)

        return raiz


# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    avl = ArbolAVL()

    print("=== CONSTRUCTOR Y BALANCEADOR DE ÁRBOLES BINARIOS ===")
    entrada = input("Ingresa los números separados por espacio o comas:\n> ")
    
    datos = entrada.replace(",", " ").split()
    numeros = [int(x) for x in datos]

    # 1. CONSTRUCCIÓN DEL ÁRBOLE ORIGINAL SIN BALANCEAR
    raiz_original = None
    for num in numeros:
        raiz_original = avl.insertar_bst(raiz_original, num)

    print("\n" + "="*55)
    print("1. ÁRBOL BINARIO ORIGINAL (SIN BALANCEAR)")
    print("="*55)
    avl.imprimir_estructura(raiz_original)

    # 2. PROCESO DE BALANCEO PASO A PASO
    print("\n" + "="*55)
    print("2. PASO A PASO DEL BALANCEO (RECONSTRUCCIÓN AVL)")
    print("="*55)
    
    raiz_balanceada = None
    for num in numeros:
        print(f"\n[+] Procesando elemento: {num}")
        raiz_balanceada = avl.insertar_avl_paso_a_paso(raiz_balanceada, num)
        print("Estructura en este paso:")
        avl.imprimir_estructura(raiz_balanceada)
        print("-" * 40)

    # 3. RESULTADO FINAL
    print("\n" + "="*55)
    print("3. ÁRBOL FINAL COMPLETAMENTE BALANCEADO")
    print("="*55)
    avl.imprimir_estructura(raiz_balanceada)