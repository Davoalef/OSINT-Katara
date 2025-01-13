from pathlib import Path
import pdfplumber
import re
import shutil

def AnalizarPDF(ruta_pdf):
    from main import tokenizer, model
    contenido_texto = ""
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                contenido_texto += pagina.extract_text() + "\n"

        inputs = tokenizer(contenido_texto, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        tokens = outputs.last_hidden_state.mean(dim=1).detach().numpy()

        if re.search(r"\b(algorithm|sequential|conditional|conditional|conditional|cyclic|algorithm|calculate|print|convert|process|digitize|design|digitize|design|calculate|print|convert|process|digitize|design|algoritmo|secuencial|condicional|condicional|ciclico|algoritmo|calcular|imprimir|convertir|procesar|digitalizar|diseñar)\b", contenido_texto, re.I):
            if "ejercicio" in contenido_texto.lower():
                return "Funciona/ejercicios"
            else:
                return "Funciona/algoritmos"
        else:
            return "No funciona"
    except Exception as e:
        print(f"Error al analizar el PDF {ruta_pdf}: {e}")
        return "No funciona"

def ClasificarPDFs():
    carpeta_pdf = Path("pdf")
    clasificacion_carpeta = carpeta_pdf / "Clasificación archivos"
    clasificacion_carpeta.mkdir(parents=True, exist_ok=True)

    for pdf_file in carpeta_pdf.rglob("*.pdf"):
        categoria = AnalizarPDF(pdf_file)
        destino = clasificacion_carpeta / categoria
        destino.mkdir(parents=True, exist_ok=True)
        shutil.move(str(pdf_file), str(destino / pdf_file.name))
        print(f"{pdf_file.name} movido a {destino}")
