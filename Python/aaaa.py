import csv

# Clase para analizar y clasificar cada línea del archivo de ensamblaje
class LineaEnsamblador: 
    def __init__(self, linea): 
        # Constructor: inicializa la línea y prepara variables para almacenar sus componentes
        self.linea = linea.strip()  # Elimina espacios en blanco al inicio y final de la línea
        self.etiqueta = None 
        self.codop = None
        self.operando = None
        self.tipo = None

    def validacion_codop(self, codop):
        #Deb: Valida si el codop existe en la PRIMERA COLUMNA del archivo csv
        print(self.codop) #Deb: Imprime el codop actual para debug
        if self.codop == "ORG": #Deb: Si el codop es ORG, imprime "Origen"
            print("Origen")
        with open('/home/javszorin/Downloads/Salvation.Tabop - Table A-1.Instruction Set Summary.csv', 'r', newline='', encoding='utf-8') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            cadena_buscada = self.codop #Deb: Asigna el codop a buscar en el csv

            # Deb: Lee todas las filas del csv a una lista para poder iterar sobre ellas varias veces
            filas = list(lector_csv)

            codop_encontrado = False # Deb: Variable para indicar si se encontró el codop
            for fila in filas: 
                # Deb: Accede directamente a la primera columna (índice 0)
                primera_columna = fila[0] 
                if cadena_buscada.upper() in primera_columna.upper(): # Deb: Ignora mayúsculas/minúsculas
                    print(f'Cadena encontrada en la fila: {fila}')
                    codop_encontrado = True 
                    break  
            if not codop_encontrado:
                print(f'Codop no encontrado: {self.codop}') # Deb: Indica si el codop no se encontró

    def procesar_linea(self): 
        # Analiza la línea y clasifica su tipo, extrayendo etiqueta, codop y operando si corresponde
        if self.linea.startswith(";"): 
            self.tipo = "COMENTARIO" 
        else:
            partes = self.linea.split() 

            if len(partes) == 3: 
                self.etiqueta = partes[0].replace(":", "") 
                self.codop = partes[1] 
                self.operando = partes[2] 
                self.validacion_codop(self.codop) # Deb: Llama a la validación después de extraer el codop
            elif len(partes) == 2: 
                if ":" in partes[0]: 
                    self.etiqueta = partes[0].replace(":", "") 
                    self.codop = partes[1] 
                    self.validacion_codop(self.codop) # Deb: Llama a la validación después de extraer el codop
                else: 
                    self.codop = partes[0] 
                    self.operando = partes[1] 
                    self.validacion_codop(self.codop) # Deb: Llama a la validación después de extraer el codop
            elif len(partes) == 1: 
                self.codop = partes[0] 
                self.validacion_codop(self.codop) # Deb: Llama a la validación después de extraer el codop
            else:
                raise ValueError("Línea inválida.") 

    def imprimir(self): 
        # Imprime la clasificación de la línea y sus componentes de manera estructurada
        if self.tipo == "COMENTARIO": 
            print("COMENTARIO") 
        else: 
            etiqueta = self.etiqueta if self.etiqueta else "null"
            codop = self.codop if self.codop else "null" 
            operando = self.operando if self.operando else "null"
            print(f"ETIQUETA= {etiqueta}") 
            print(f"CODOP= {codop}")
            print(f"OPERANDO= {operando}")
            print("[--------------------------]"); 

# Clase para procesar el archivo de ensamblaje completo
class ProcesadorASM: 
    def __init__(self, archivo): 
        # Constructor: inicializa el archivo y la lista de líneas
        self.archivo = archivo 
        self.lineas = [] 

    def leer_archivo(self): 
        # Lee el archivo y almacena sus líneas en la lista 'self.lineas'
        try:
            with open(self.archivo, 'r') as f:
                self.lineas = f.readlines() 
        except FileNotFoundError:
            print(f"Error: el archivo {self.archivo} no se encontró.") 

    def procesar_lineas(self): 
        # Procesa cada línea del archivo, creando un objeto 'LineaEnsamblador' para analizarla e imprimir su resultado
        for linea in self.lineas: 
            linea_ensamblador = LineaEnsamblador(linea) 
            linea_ensamblador.procesar_linea() 
            linea_ensamblador.imprimir() 

# Programa principal: crea un objeto 'ProcesadorASM', lee el archivo y procesa sus líneas
procesador = ProcesadorASM("P1ASM.asm") 
procesador.leer_archivo() 
procesador.procesar_lineas()