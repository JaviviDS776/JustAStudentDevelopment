import flet as ft
import csv

class InstruccionInfo:
    def __init__(self, codop, operandos, addr_mode, source_form, bytes_por_calcular, total_bytes):
        self.codop = codop
        self.operandos = operandos
        self.addr_mode = addr_mode
        self.source_form = source_form
        self.bytes_por_calcular = bytes_por_calcular
        self.total_bytes = total_bytes

class CSVHandler:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.instrucciones = {}

    def leer_csv(self):
        with open(self.csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                codop, operandos, addr_mode, source_form, bytes_por_calcular, total_bytes = row
                if codop not in self.instrucciones:
                    self.instrucciones[codop] = []
                self.instrucciones[codop].append(InstruccionInfo(codop, operandos, addr_mode, source_form, int(bytes_por_calcular), int(total_bytes)))

    def obtener_modo_direccionamiento(self, codop, operando):
        if codop in self.instrucciones:
            for instruccion in self.instrucciones[codop]:
                if self.coincide_operando(operando, instruccion.operandos):
                    return instruccion.addr_mode
        if codop == "ORG":
            return "Inicio"
        return "desconocido"

    def coincide_operando(self, operando, patron):
        if patron == '-' and operando is None:
            return True
        if patron.startswith('#') and operando and operando.startswith('#'):
            return True
        if patron == 'opr8a' and operando and len(operando) == 2:
            return True
        if patron == 'opr16a' and operando and len(operando) == 4:
            return True
        if 'xysp' in patron and operando and ',' in operando:
            return True
        return False

class LineaEnsamblador:
    def __init__(self, linea, csv_handler):
        self.linea = linea.strip()
        self.etiqueta = None
        self.codop = None
        self.operando = None
        self.tipo = None
        self.modo_direccionamiento = None
        self.csv_handler = csv_handler

    def procesar_linea(self):
        if self.linea.startswith(";"):
            self.tipo = "COMENTARIO"
        else:
            partes = self.linea.split()
            
            if len(partes) == 3:
                self.etiqueta = partes[0].replace(":", "")
                self.codop = partes[1]
                self.operando = partes[2]
            elif len(partes) == 2:
                if ":" in partes[0]:
                    self.etiqueta = partes[0].replace(":", "")
                    self.codop = partes[1]
                else:
                    self.codop = partes[0]
                    self.operando = partes[1]
            elif len(partes) == 1:
                self.codop = partes[0]
            else:
                raise ValueError("Línea inválida.")
        
        self.determinar_modo_direccionamiento()

    def determinar_modo_direccionamiento(self):
        if self.codop:
            self.modo_direccionamiento = self.csv_handler.obtener_modo_direccionamiento(self.codop, self.operando)

    def get_row_data(self):
        if self.tipo == "COMENTARIO":
            return ["COMENTARIO", "", "", "", ""]
        else:
            return [
                self.etiqueta if self.etiqueta else "null",
                self.codop if self.codop else "null",
                self.operando if self.operando else "null",
                self.modo_direccionamiento if self.modo_direccionamiento else "desconocido",
                self.linea
            ]

class ProcesadorASM:
    def __init__(self, archivo, csv_handler):
        self.archivo = archivo
        self.lineas = []
        self.csv_handler = csv_handler
    
    def leer_archivo(self):
        try:
            with open(self.archivo, 'r') as f:
                self.lineas = f.readlines()
        except FileNotFoundError:
            print(f"Error: el archivo {self.archivo} no se encontró.")
    
    def procesar_lineas(self):
        resultados = []
        for linea in self.lineas:
            linea_ensamblador = LineaEnsamblador(linea, self.csv_handler)
            linea_ensamblador.procesar_linea()
            resultados.append(linea_ensamblador.get_row_data())
        return resultados

def main(page: ft.Page):
    page.title = "Procesador ASM"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Etiqueta")),
            ft.DataColumn(ft.Text("CODOP")),
            ft.DataColumn(ft.Text("Operando")),
            ft.DataColumn(ft.Text("Modo Direccionamiento")),
            ft.DataColumn(ft.Text("Línea Original")),
        ],
        rows=[]
    )

    def process_file(file_path):
        csv_handler = CSVHandler("try/addressing.csv")
        csv_handler.leer_csv()
        procesador = ProcesadorASM(file_path, csv_handler)
        procesador.leer_archivo()
        resultados = procesador.procesar_lineas()

        table.rows.clear()
        for resultado in resultados:
            table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in resultado]))
        page.update()

    def openASM(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            process_file(file_path)

    file_picker = ft.FilePicker(on_result=openASM)
    page.overlay.append(file_picker)

    open_file_button = ft.ElevatedButton(
        text="Seleccionar archivo ASM",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(file_type=['.asm', '.ASM', '.s', '.S'])
    )

    page.add(ft.Column([
        open_file_button,
        ft.Container(height=20),
        table
    ]))

ft.app(target=main)