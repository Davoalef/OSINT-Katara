import re
import shutil
from pathlib import Path
import pdfplumber
import time

def AnalizarArchivo(ruta_archivo):
    contenido_texto = ""
    try:
        if ruta_archivo.suffix.lower() == ".pdf":
            with pdfplumber.open(str(ruta_archivo)) as pdf:  # Asegurar que se cierra correctamente
                for pagina in pdf.pages:
                    contenido_texto += pagina.extract_text() or ""  # Evitar errores si la página no tiene texto
        elif ruta_archivo.suffix.lower() == ".txt":
            with open(ruta_archivo, "r", encoding="utf-8") as archivo_txt:
                contenido_texto = archivo_txt.read()
        else:
            return "🚫No funciona"

        # Buscar palabras clave
        if re.search(
            r"\b(algorithm|sequential|conditional|cyclic|calculate|print|convert|process|digitize|design|algoritmo|secuencial|condicional|ciclico|calcular|imprimir|convertir|procesar|digitalizar|diseñar)\b",
            contenido_texto,
            re.I,
        ):
            if "ejercicio" in contenido_texto.lower():
                return "👍🏋️‍♀️Funciona/ejercicios"
            else:
                return "👍🧩Funciona/algoritmos"
        else:
            return "🚫No funciona"

    except Exception as e:
        print(f"Error al analizar el archivo {ruta_archivo}: {e}")
        return "🚫No funciona"

def ClasificarArchivos():
    carpeta_archivos = Path("archivos")
    carpeta_pdf = carpeta_archivos / "pdf"
    carpeta_txt = carpeta_archivos / "txt"
    carpeta_clasificacion = carpeta_archivos / "Clasificación archivos"

    carpeta_clasificacion.mkdir(parents=True, exist_ok=True)

    for carpeta in [carpeta_pdf, carpeta_txt]:
        for archivo in carpeta.rglob("*.*"):
            if archivo.suffix.lower() in [".pdf", ".txt"]:
                categoria = AnalizarArchivo(archivo)
                destino = carpeta_clasificacion / categoria

                destino.mkdir(parents=True, exist_ok=True)

                time.sleep(1)

                try:
                    shutil.move(str(archivo), str(destino / archivo.name))
                    print(f"{archivo.name} movido a {destino}")
                except Exception as e:
                    print(f"Error al mover {archivo}: {e}")