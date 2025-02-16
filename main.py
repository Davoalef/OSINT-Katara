from buscarGoogle import BuscarGoogle
from buscarGoogleAcademico import BuscarGoogleAcademico
from clasificador import ClasificarArchivos
from transformers import AutoTokenizer, AutoModel
from pathlib import Path
from selenium.webdriver.chrome.options import Options
import sys
import subprocess
import concurrent.futures
import torch

# Verificar si el script se ejecuta en la terminal
if len(sys.argv) == 1:
    subprocess.run(['start', 'cmd', '/K', 'python', __file__, 'run_in_cmd'], shell=True)
    sys.exit()

modelo_nombre = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

tokenizer = AutoTokenizer.from_pretrained(modelo_nombre, trust_remote_code=True)

modelo = AutoModel.from_pretrained(
    modelo_nombre,
    trust_remote_code=True,
    torch_dtype=torch.float32,  # Forzar FP32
    device_map={"": "cpu"}  # Asegurar que todo se carga en CPU
)

# Función para mostrar el encabezado del programa
def HabeasData():
    print("==================================================================================================")
    print("   ██░ ██  ▄▄▄       ▄▄▄▄   ▓█████ ▄▄▄        ██████    ▓█████▄  ▄▄▄     ████████▓ ▄▄▄            ")
    print("  ▓██░ ██▒▒████▄    ▓█████▄ ▓█   ▀▒████▄    ▒██    ▒    ▒██▀ ██▌▒████▄   ▓  ██▒    ████▄          ")
    print("  ▒██▀▀██░▒██  ▀█▄  ▒██▒ ▄██▒███  ▒██  ▀█▄  ░ ▓██▄      ░██   █▌▒██  ▀█▄ ▒ ▓██░ ▒░▒██  ▀█▄        ")
    print("  ░▓█ ░██ ░██▄▄▄▄██ ▒██░█▀  ▒▓█  ▄░██▄▄▄▄██   ▒   ██▒   ░▓█▄   ▌░██▄▄▄▄██░ ▓██▓ ░ ░██▄▄▄▄██       ")
    print("  ░▓█▒░██▓ ▓█   ▓██▒░▓█  ▀█▓░▒████▒▓█   ▓██▒▒██████▒▒   ░▒████▓  ▓█   ▓██▒ ▒██▒ ░  ▓█   ▓██▒      ")
    print("  ▒ ░░▒░▒ ▒▒   ▓▒ ░░▒▓███▀▒░░ ▒░ ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░    ▒▒▓  ▒  ▒▒   ▓▒█░ ▒ ░░    ▒▒   ▓▒█░       ")
    print("  ▒ ░▒░ ░  ▒   ▒▒ ░▒░▒   ░  ░ ░  ░ ▒   ▒▒ ░░ ░▒  ░ ░    ░ ▒  ▒   ▒   ▒▒ ░   ░      ▒   ▒▒ ░       ")
    print("  ░  ░░ ░  ░   ▒    ░    ░    ░    ░   ▒   ░  ░  ░      ░ ░  ░   ░   ▒    ░        ░   ▒          ")
    print("  ░  ░  ░      ░  ░ ░         ░  ░     ░  ░      ░        ░          ░  ░              ░  ░       ")
    print("                         ░                              ░                                         ")
    print("==================================================================================================")
    print("||                                                                                              ||")
    print("||                                  Realiza búsquedas automáticas                               ||")
    print("||                            Descarga PDFs y guarda resultados en JSON                         ||")
    print("||                                                                                              ||")
    print("==================================================================================================")
    print(">>>                                        !Comencemos¡                                        <<<")
    print("==================================================================================================")

# Función para ingresar palabras clave
def PalabrasClaves():
    while True:
        n_palabras = int(input("\nIngresa el número de búsquedas que vas a realizar: "))
        if n_palabras > 0:
            break
        else:
            print("Error, ingresa un valor numérico válido.")
    
    palabras_clave = []
    for i in range(n_palabras):
        palabra = input(f"\nPalabra clave {i + 1}: ").strip()  
        palabra_pdf = f"{palabra} filetype:pdf"
        palabra_txt = f"{palabra} filetype:txt"
        palabras_clave.extend([palabra_pdf, palabra_txt])
    
    return palabras_clave

options = Options()
options.add_argument("--window-size=1080,720")

# Función principal para ejecutar el programa
def Ejecutar():
    HabeasData()
    palabras_clave = PalabrasClaves()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(BuscarGoogle, palabras_clave)
        executor.map(BuscarGoogleAcademico, palabras_clave)

    ClasificarArchivos()
    print("Proceso de búsqueda y clasificación completado.")

# Ejecutar el programa en si mismo
if __name__ == "__main__":
    Ejecutar()