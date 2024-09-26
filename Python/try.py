import os
import tkinter as tk
from tkinter import filedialog
# No necesitamos importar nada específico para la funcionalidad básica de archivos

# Clase para representar una línea de ensamblador
class LineaEnsamblador:
    def __init__(self):
        self.etiqueta = None
        self.codop = None
        self.operando = None

    # Método para analizar una línea y extraer sus componentes
    def analizar_linea(self, linea):
        # Eliminar espacios en blanco al inicio y al final
        linea = linea.strip()

        # Verificar si la línea es un comentario
        if linea.startswith(";"):
            pass  # No hacemos nada con los comentarios
        else:
            # Dividir la línea en palabras
            palabras = linea.split()  # En Python, split() por defecto separa por espacios en blanco

            # Lógica para identificar etiqueta, codop y operando
            if len(palabras) == 1:
                self.codop = palabras[0]
            elif len(palabras) == 2:
                if palabras[0].endswith(":"):
                    self.etiqueta = palabras[0][:-1]  # Eliminar el ":" al final
                    self.codop = palabras[1]
                else:
                    self.codop = palabras[0]
                    self.operando = palabras[1]
            elif len(palabras) >= 3:
                indice_dos_puntos = -1
                for i, palabra in enumerate(palabras):
                    if palabra.endswith(":"):
                        indice_dos_puntos = i
                        break

                if indice_dos_puntos != -1:
                    self.etiqueta = palabras[indice_dos_puntos][:-1]
                    self.codop = palabras[indice_dos_puntos + 1]
                    self.operando = " ".join(palabras[indice_dos_puntos + 2:])

# Programa principal
if __name__ == "__main__":

    # Obtiene la ruta del directorio actual donde se encuentra el script
    ruta_actual = os.path.dirname(os.path.abspath(__file__))

    # Combina la ruta actual con la ruta relativa deseada (por ejemplo, "carpeta_documentos")
    ruta_inicial = os.path.join(ruta_actual, "carpeta_documentos")

    ruta_archivo = filedialog.askopenfilename(
        initialdir=ruta_inicial,  # Usa la ruta inicial calculada
        title="Seleccionar archivo",
        filetypes=(("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt"))
    )

    if ruta_archivo:
        print("Ruta del archivo seleccionado:", ruta_archivo)
        archivo = ruta_archivo


     

    try:
        with open(archivo, "r") as f:  # Manejo de archivos más sencillo en Python
            for linea in f:
                linea_ensamblador = LineaEnsamblador()
                linea_ensamblador.analizar_linea(linea)

                # Imprimir los componentes de la línea
                print("ETIQUETA=", linea_ensamblador.etiqueta or "null")
                print("CODOP=", linea_ensamblador.codop or "null")
                print("OPERANDO=", linea_ensamblador.operando or "null")

    except FileNotFoundError:  # Excepción más específica para archivos no encontrados
        print(f"Error: El archivo '{archivo}' no se encontró.")
    except IOError as e:
        print(f"Error al leer el archivo: {e}")