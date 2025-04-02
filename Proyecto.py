"""
Módulo para el análisis y derivación de polinomios con funciones trigonométricas y exponenciales
Utiliza programación orientada a objetos con los principios solicitados en el proyecto
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
import time
import functools

def cache_decorator(func):
    """Decorador para cachear resultados de funciones"""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

# Clase abstracta base para términos matemáticos
class TerminoMatematico(ABC):
    """Clase abstracta que define la interfaz para todos los términos matemáticos"""
    
    def __init__(self, coeficiente=1.0):
        self._coeficiente = coeficiente
    
    @property
    def coeficiente(self):
        """Getter para el coeficiente"""
        return self._coeficiente
    
    @coeficiente.setter
    def coeficiente(self, valor):
        """Setter para el coeficiente"""
        self._coeficiente = valor
    
    @abstractmethod
    def evaluar(self, x):
        """Evalúa el término para un valor dado de x"""
        pass
    
    @abstractmethod
    def derivar(self):
        """Deriva el término y devuelve un nuevo término"""
        pass
    
    @abstractmethod
    def __str__(self):
        """Representación en string del término"""
        pass

# Clases concretas para diferentes tipos de términos
class TerminoConstante(TerminoMatematico):
    """Término constante: coeficiente sin variable"""
    
    def evaluar(self, x):
        return self.coeficiente
    
    def derivar(self):
        return TerminoConstante(0)
    
    def __str__(self):
        return f"{self.coeficiente}"

class TerminoPolinomico(TerminoMatematico):
    """Término polinómico: coeficiente * x^exponente"""
    
    def __init__(self, coeficiente=1.0, exponente=1):
        super().__init__(coeficiente)
        self._exponente = exponente
    
    @property
    def exponente(self):
        """Getter para el exponente"""
        return self._exponente
    
    @exponente.setter
    def exponente(self, valor):
        """Setter para el exponente"""
        self._exponente = valor
    
    def evaluar(self, x):
        return self.coeficiente * (x ** self.exponente)
    
    def derivar(self):
        if self.exponente == 0:
            return TerminoConstante(0)
        nuevo_coef = self.coeficiente * self.exponente
        nuevo_exp = self.exponente - 1
        return TerminoPolinomico(nuevo_coef, nuevo_exp)
    
    def __str__(self):
        if self.exponente == 0:
            return f"{self.coeficiente}"
        elif self.exponente == 1:
            return f"{self.coeficiente}*x"
        else:
            return f"{self.coeficiente}*x^{self.exponente}"

class TerminoTrigonometrico(TerminoMatematico):
    """Término trigonométrico: coeficiente * func_trig(x)"""
    
    def __init__(self, coeficiente=1.0, func_trig="sin"):
        super().__init__(coeficiente)
        self._func_trig = func_trig
    
    @property
    def func_trig(self):
        """Getter para la función trigonométrica"""
        return self._func_trig
    
    @func_trig.setter
    def func_trig(self, valor):
        """Setter para la función trigonométrica"""
        if valor not in ["sin", "cos", "tan"]:
            raise ValueError("Función trigonométrica no válida")
        self._func_trig = valor
    
    def evaluar(self, x):
        if self.func_trig == "sin":
            return self.coeficiente * math.sin(x)
        elif self.func_trig == "cos":
            return self.coeficiente * math.cos(x)
        elif self.func_trig == "tan":
            return self.coeficiente * math.tan(x)
    
    def derivar(self):
        if self.func_trig == "sin":
            return TerminoTrigonometrico(self.coeficiente, "cos")
        elif self.func_trig == "cos":
            return TerminoTrigonometrico(-self.coeficiente, "sin")
        elif self.func_trig == "tan":
            return TerminoEspecial(self.coeficiente, "sec^2")
    
    def __str__(self):
        return f"{self.coeficiente}*{self.func_trig}(x)"

class TerminoExponencial(TerminoMatematico):
    """Término exponencial: coeficiente * exp(factor * x)"""
    
    def __init__(self, coeficiente=1.0, factor=1.0):
        super().__init__(coeficiente)
        self._factor = factor
    
    @property
    def factor(self):
        """Getter para el factor dentro de la exponencial"""
        return self._factor
    
    @factor.setter
    def factor(self, valor):
        """Setter para el factor dentro de la exponencial"""
        self._factor = valor
    
    def evaluar(self, x):
        return self.coeficiente * math.exp(self.factor * x)
    
    def derivar(self):
        return TerminoExponencial(self.coeficiente * self.factor, self.factor)
    
    def __str__(self):
        if self.factor == 1:
            return f"{self.coeficiente}*exp(x)"
        else:
            return f"{self.coeficiente}*exp({self.factor}*x)"

class TerminoEspecial(TerminoMatematico):
    """Término especial para casos particulares como sec^2"""
    
    def __init__(self, coeficiente=1.0, tipo="sec^2"):
        super().__init__(coeficiente)
        self._tipo = tipo
    
    @property
    def tipo(self):
        """Getter para el tipo de término especial"""
        return self._tipo
    
    @tipo.setter
    def tipo(self, valor):
        """Setter para el tipo de término especial"""
        self._tipo = valor
    
    def evaluar(self, x):
        if self.tipo == "sec^2":
            return self.coeficiente / (math.cos(x) ** 2)
        return 0
    
    def derivar(self):
        # La derivada de términos especiales podría requerir implementación adicional
        return TerminoConstante(0)
    
    def __str__(self):
        if self.tipo == "sec^2":
            return f"{self.coeficiente}/cos(x)^2"
        return str(self.coeficiente)

# Clase para el polinomio completo
class Polinomio:
    """
    Clase que representa un polinomio completo compuesto por varios términos
    """
    
    def __init__(self):
        self._terminos = []
    
    @property
    def terminos(self):
        """Getter para la lista de términos"""
        return self._terminos
    
    def agregar_termino(self, termino):
        """Agrega un término al polinomio"""
        if not isinstance(termino, TerminoMatematico):
            raise TypeError("El término debe ser una instancia de TerminoMatematico")
        self._terminos.append(termino)
    
    @cache_decorator
    def evaluar(self, x):
        """Evalúa el polinomio para un valor dado de x"""
        resultado = 0
        for termino in self.terminos:
            resultado += termino.evaluar(x)
        return resultado
    
    def derivar(self):
        """Deriva el polinomio y devuelve un nuevo polinomio"""
        polinomio_derivada = Polinomio()
        for termino in self.terminos:
            termino_derivado = termino.derivar()
            if not isinstance(termino_derivado, TerminoConstante) or termino_derivado.coeficiente != 0:
                polinomio_derivada.agregar_termino(termino_derivado)
        return polinomio_derivada
    
    def __str__(self):
        """Representación en string del polinomio"""
        if not self.terminos:
            return "0"
        
        resultado = str(self.terminos[0])
        for i in range(1, len(self.terminos)):
            termino_str = str(self.terminos[i])
            if termino_str.startswith("-"):
                resultado += f" - {termino_str[1:]}"
            else:
                resultado += f" + {termino_str}"
        
        return resultado

# Clase para el analizador de texto
class AnalizadorPolinomio:
    """
    Clase para analizar y convertir expresiones de texto en objetos Polinomio
    """
    
    @staticmethod
    def _extraer_coeficiente(texto):
        """Extrae el coeficiente de un texto"""
        texto = texto.strip()
        if not texto:
            return 1.0
        
        if texto == "-":
            return -1.0
        elif texto == "+":
            return 1.0
        
        try:
            return float(texto)
        except ValueError:
            return 1.0
    
    @staticmethod
    def _analizar_termino(termino):
        """Analiza un término individual del polinomio"""
        termino = termino.replace(" ", "")
        
        # Determinar el signo y extraer el coeficiente
        coef = 1.0
        if termino.startswith('-'):
            coef = -1.0
            termino = termino[1:]
        elif termino.startswith('+'):
            termino = termino[1:]
        
        # Extraer coeficiente numérico
        i = 0
        num_str = ""
        while i < len(termino) and (termino[i].isdigit() or termino[i] == '.'):
            num_str += termino[i]
            i += 1
        
        if num_str:
            coef *= float(num_str)
        
        # Verificar si hay operador de multiplicación
        if i < len(termino) and termino[i] == '*':
            i += 1
        
        # Verificar si es un término exponencial
        if i < len(termino) and termino[i:].startswith('exp'):
            i += 3  # Saltar 'exp'
            factor = 1.0
            
            # Extraer el argumento de la exponencial
            if i < len(termino) and termino[i] == '(':
                i += 1
                # Buscar por un posible factor
                factor_str = ""
                while i < len(termino) and termino[i] != '*' and termino[i] != ')':
                    factor_str += termino[i]
                    i += 1
                
                if factor_str.isdigit() or (factor_str.replace('.', '', 1).isdigit()):
                    factor = float(factor_str)
                
                # Si hay un operador de multiplicación, saltar
                if i < len(termino) and termino[i] == '*':
                    i += 1
                
                # Buscar la variable x
                if i < len(termino) and (termino[i] == 'x' or termino[i] == 'X'):
                    i += 1  # Saltar la x
                
                # Cerrar paréntesis
                if i < len(termino) and termino[i] == ')':
                    i += 1
            
            return TerminoExponencial(coef, factor)
        
        # Verificar si es un término trigonométrico
        for func in ['sin', 'cos', 'tan']:
            if i < len(termino) and termino[i:].startswith(func):
                return TerminoTrigonometrico(coef, func)
        
        # Buscar la variable x
        var_x = False
        if i < len(termino) and (termino[i] == 'x' or termino[i] == 'X'):
            var_x = True
            i += 1
        
        # Extraer exponente si existe
        exp = 1 if var_x else 0
        if i < len(termino) and termino[i] == '^':
            i += 1
            exp_str = ""
            while i < len(termino) and termino[i].isdigit():
                exp_str += termino[i]
                i += 1
            if exp_str:
                exp = int(exp_str)
        
        # Crear el término adecuado
        if var_x:
            return TerminoPolinomico(coef, exp)
        else:
            return TerminoConstante(coef)
    
    def analizar(self, texto_polinomio):
        """Analiza una cadena de texto y devuelve un objeto Polinomio"""
        polinomio = Polinomio()
        
        # Formatear el texto para facilitar el análisis
        if not texto_polinomio.startswith('+') and not texto_polinomio.startswith('-'):
            texto_polinomio = '+' + texto_polinomio
        
        # Dividir en términos
        i = 0
        start = 0
        terminos_texto = []
        
        while i < len(texto_polinomio):
            if i > 0 and (texto_polinomio[i] == '+' or texto_polinomio[i] == '-'):
                terminos_texto.append(texto_polinomio[start:i])
                start = i
            i += 1
        
        # Agregar el último término
        if start < len(texto_polinomio):
            terminos_texto.append(texto_polinomio[start:])
        
        # Analizar cada término y agregarlo al polinomio
        for termino_texto in terminos_texto:
            if termino_texto:
                termino = self._analizar_termino(termino_texto)
                polinomio.agregar_termino(termino)
        
        return polinomio

# Clase para visualización
class VisualizadorMatematico:
    """
    Clase para visualizar polinomios y sus derivadas usando matplotlib
    """
    
    def __init__(self, x_min=-10, x_max=10, num_puntos=1000):
        self._x_min = x_min
        self._x_max = x_max
        self._num_puntos = num_puntos
    
    @property
    def x_min(self):
        return self._x_min
    
    @x_min.setter
    def x_min(self, valor):
        self._x_min = valor
    
    @property
    def x_max(self):
        return self._x_max
    
    @x_max.setter
    def x_max(self, valor):
        self._x_max = valor
    
    @property
    def num_puntos(self):
        return self._num_puntos
    
    @num_puntos.setter
    def num_puntos(self, valor):
        if valor <= 0:
            raise ValueError("El número de puntos debe ser positivo")
        self._num_puntos = valor
    
    def _preparar_datos(self, polinomio):
        """Prepara los datos para la visualización"""
        x_vals = np.linspace(self.x_min, self.x_max, self.num_puntos)
        y_vals = []
        
        for x in x_vals:
            try:
                y = polinomio.evaluar(x)
                if not math.isnan(y) and not math.isinf(y):
                    y_vals.append(y)
                else:
                    y_vals.append(None)
            except:
                y_vals.append(None)
        
        return x_vals, y_vals
    
    def graficar_polinomio(self, polinomio, titulo=None):
        """Grafica un polinomio"""
        x_vals, y_vals = self._preparar_datos(polinomio)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, label=str(polinomio))
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True, linestyle='--', linewidth=0.5)
        
        if titulo:
            plt.title(titulo)
        plt.legend()
        plt.show()
    
    def comparar_polinomios(self, polinomio_original, polinomio_derivado):
        """Grafica un polinomio y su derivada juntos"""
        x_vals, y_original = self._preparar_datos(polinomio_original)
        _, y_derivada = self._preparar_datos(polinomio_derivado)
        
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 1, 1)
        plt.plot(x_vals, y_original, 'b-', label='Función Original')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.legend()
        plt.title('Función Original')
        
        plt.subplot(2, 1, 2)
        plt.plot(x_vals, y_derivada, 'r-', label='Derivada')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.legend()
        plt.title('Función Derivada')
        
        plt.tight_layout()
        plt.show()
    
    @timing_decorator
    def animar_polinomio(self, polinomio, frames=100):
        """Crea una animación mostrando cómo evoluciona la gráfica"""
        x_vals, y_vals = self._preparar_datos(polinomio)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        line, = ax.plot([], [], 'b-', lw=2)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True, linestyle='--', linewidth=0.5)
        
        ax.set_xlim(self.x_min, self.x_max)
        
        # Encontrar límites adecuados para el eje y
        valid_values = [y for y in y_vals if y is not None]
        if valid_values:
            y_min = min(valid_values)
            y_max = max(valid_values)
            margin = (y_max - y_min) * 0.1
            ax.set_ylim(y_min - margin, y_max + margin)
        else:
            ax.set_ylim(-10, 10)
        
        ax.set_title(f"Animación de {polinomio}")
        
        def init():
            line.set_data([], [])
            return line,
        
        def animate(i):
            x_subset = x_vals[:int((i + 1) * len(x_vals) / frames)]
            y_subset = y_vals[:int((i + 1) * len(y_vals) / frames)]
            line.set_data(x_subset, y_subset)
            return line,
        
        from matplotlib.animation import FuncAnimation
        ani = FuncAnimation(fig, animate, frames=frames, init_func=init, blit=True, interval=50)
        plt.close()  # Cierra la figura para prevenir doble visualización
        
        

# Clase principal de la aplicación
class AplicacionMatematica:
    """
    Clase principal que integra todas las funcionalidades del programa
    """
    
    def __init__(self):
        self.analizador = AnalizadorPolinomio()
        self.visualizador = VisualizadorMatematico()
    
    def ejecutar(self):
        """Método principal para ejecutar la aplicación"""
        try:
            # Solicitar entrada al usuario
            texto_polinomio = input("Ingrese el polinomio a derivar, use ^ para expontes (Ej: x^2): ")
            
            # Analizar el polinomio
            polinomio = self.analizador.analizar(texto_polinomio)
            print(f"Polinomio: {polinomio}")
            
            # Derivar el polinomio
            polinomio_derivado = polinomio.derivar()
            print(f"Derivada: {polinomio_derivado}")
            
            # Visualizar los resultados
            print("Graficando la función original y su derivada...")
            self.visualizador.comparar_polinomios(polinomio, polinomio_derivado) 
        except Exception as e:
            print(f"Error: {str(e)}")

# Punto de entrada del programa
def main():
    """Función principal para iniciar la aplicación"""
    app = AplicacionMatematica()
    app.ejecutar()

if __name__ == "__main__":
    main()
