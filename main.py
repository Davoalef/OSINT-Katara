from buscarGoogle import BuscarGoogle
from buscarGoogleAcademico import BuscarGoogleAcademico
from clasificador import ClasificarPDFs
from transformers import AutoTokenizer, AutoModel
from pathlib import Path
from selenium.webdriver.chrome.options import Options
import sys
import subprocess
import concurrent.futures

if len(sys.argv) == 1:
    subprocess.run(['start', 'cmd', '/K', 'python', __file__, 'run_in_cmd'], shell=True)
    sys.exit()
if sys.argv[1] == 'run_in_cmd':
    print("CMD")

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")

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

#==================================================================================================

def PalabrasClaves():
    while True:
        n_palabras = int(input("\nIngresa el número de busquedas que vas a realizar: "))
        if n_palabras > 0:
            break
        else:
            print("Error, valor númerico")
    
    palabras_clave = []
    for i in range(n_palabras):
        palabra = input(f"\nLa palabra clave es: {i + 1}. ")
        palabras_clave.append(palabra)
    
    return palabras_clave

Path("pdf").mkdir(parents=True, exist_ok=True)
options = Options()
options.add_argument("--window-size=1920,1080")

#==================================================================================================

def Ejecutar():
    HabeasData()
    palabras_clave = PalabrasClaves()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(BuscarGoogle, palabras_clave)
        executor.map(BuscarGoogleAcademico, palabras_clave)

    ClasificarPDFs()
    print("Proceso de búsqueda y clasificación completado.")

if __name__ == "__main__":
    Ejecutar()