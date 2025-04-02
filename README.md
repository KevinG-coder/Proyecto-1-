# Calculadora de Polinomios y Derivadas

## Descripción
Esta aplicación permite analizar, evaluar y derivar expresiones matemáticas complejas que incluyen términos polinómicos, trigonométricos y exponenciales. Implementada con programación orientada a objetos en Python, la aplicación puede interpretar expresiones ingresadas por el usuario, calcular sus derivadas y visualizar gráficamente tanto la función original como su derivada.

## Características
- Análisis de expresiones matemáticas desde texto
- Soporte para términos:
  - Polinómicos (constantes, lineales, cuadráticos, etc.)
  - Trigonométricos (seno, coseno, tangente)
  - Exponenciales
- Cálculo de derivadas
- Visualización gráfica de funciones y sus derivadas
- Animación de gráficas
- Implementación de patrones de diseño y principios OOP
- Optimizaciones con decoradores de caché y medición de rendimiento

## Requisitos
- Python 3.x
- NumPy
- Matplotlib

## Instalación
```bash
# Clonar el repositorio (si aplica)
git clone [URL_del_repositorio]

# Instalar dependencias
pip install numpy matplotlib
```

## Uso
Ejecute el archivo principal para iniciar la aplicación:
```bash
python prueba2.py
```

La aplicación le pedirá que ingrese una expresión matemática. Por ejemplo:
```
Ingrese el polinomio a derivar: 2*x^3 + 3*sin(x) - 5*exp(2*x) + 1
```

### Ejemplos de expresiones válidas:
- `x^2 + 3*x - 5`
- `sin(x) + cos(x)`
- `2*exp(x) - x^3`
- `5*tan(x) + 2*x`

## Estructura del proyecto
El código está organizado siguiendo principios de programación orientada a objetos:

### Clases principales
1. **TerminoMatematico** (Abstracta): Clase base para todos los términos matemáticos
2. **TerminoConstante**: Representa una constante numérica
3. **TerminoPolinomico**: Representa términos de la forma a*x^n
4. **TerminoTrigonometrico**: Representa términos trigonométricos (sin, cos, tan)
5. **TerminoExponencial**: Representa términos exponenciales
6. **TerminoEspecial**: Para casos particulares como sec²
7. **Polinomio**: Compone múltiples términos en una expresión completa
8. **AnalizadorPolinomio**: Convierte texto en objetos Polinomio
9. **VisualizadorMatematico**: Visualiza gráficamente los resultados
10. **AplicacionMatematica**: Integra todas las funcionalidades

### Decoradores
- **timing_decorator**: Mide el tiempo de ejecución de funciones
- **cache_decorator**: Implementa caché para optimizar funciones repetitivas

## Principios de diseño implementados
- **Abstracción**: Uso de clases abstractas para definir interfaces comunes
- **Encapsulamiento**: Atributos privados con getters y setters
- **Herencia**: Jerarquía de clases basada en TerminoMatematico
- **Polimorfismo**: Comportamiento específico para cada tipo de término
- **Composición**: Un Polinomio está compuesto por múltiples TerminoMatematico
- **Principio de responsabilidad única**: Cada clase tiene una responsabilidad bien definida

## Diagrama de clases simplificado
```
TerminoMatematico (ABC)
  ├── TerminoConstante
  ├── TerminoPolinomico
  ├── TerminoTrigonometrico
  ├── TerminoExponencial
  └── TerminoEspecial

Polinomio
  └── contiene: TerminoMatematico (*)

AnalizadorPolinomio
VisualizadorMatematico
AplicacionMatematica
  ├── tiene: AnalizadorPolinomio
  └── tiene: VisualizadorMatematico
```

## Limitaciones conocidas
- Las expresiones deben seguir el formato específico descrito en los ejemplos
- No se soportan funciones trigonométricas inversas
- La visualización puede mostrar comportamientos inesperados cerca de asíntotas

## Contribuciones
Las contribuciones son bienvenidas. Por favor, asegúrese de seguir los siguientes pasos:
1. Bifurque el repositorio
2. Cree una rama para su característica (`git checkout -b feature/nueva-caracteristica`)
3. Confirme sus cambios (`git commit -m 'Añade nueva característica'`)
4. Envíe a la rama (`git push origin feature/nueva-caracteristica`)
5. Abra una solicitud de extracción

## Autor
[Kevin Santiago Gomez Cardenas]
