from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import os
import time
import json
import requests

def BuscarGoogleAcademico(palabra_clave):
    from main import options
    driver = webdriver.Chrome(options=options)
    driver.get("https://scholar.google.com/")
    palabra = driver.find_element("css selector", "input[name='q']")
    palabra.clear()
    palabra.send_keys(palabra_clave)
    time.sleep(5)
    palabra.send_keys(Keys.RETURN)
    time.sleep(5)
    
    Algoritmos_titulo = []
    Algoritmos_link = []

    def ScrollPagina():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(30)

    def ExtraerMetaDatos():
        page = BeautifulSoup(driver.page_source, 'html.parser')
        for resultado in page.findAll('div', attrs={'class': 'gs_r gs_or gs_scl'}):
            titulo = resultado.find('h3', attrs={'class': 'gs_rt'})
            if titulo and titulo.a:
                link = titulo.a.get('href')
                Algoritmos_titulo.append(titulo.text)
                Algoritmos_link.append(link)
                
                # Verificar el tipo de archivo antes de descargar
                if link.endswith(".pdf"):
                    DescargarArchivo(link, palabra_clave, "pdf")
                elif link.endswith(".txt"):
                    DescargarArchivo(link, palabra_clave, "txt")
            else:
                Algoritmos_titulo.append('No hay título')
                Algoritmos_link.append('No hay link')

    def DescargarArchivo(link, carpeta_clave, extension, tiempo_limite=60):
        """ Descarga archivos PDF y TXT en carpetas separadas. """
        try:
            carpeta_clave = palabra_clave.replace(" ", "_").replace(":", "_")
            carpeta_destino = f"archivos/{extension}/{carpeta_clave}"
            Path(carpeta_destino).mkdir(parents=True, exist_ok=True)

            response = requests.get(link, timeout=tiempo_limite, stream=True)
            nombre_archivo = os.path.join(carpeta_destino, link.split("/")[-1])

            with open(nombre_archivo, 'wb') as f:
                f.write(response.content)

            print(f"📂✅ Archivo descargado: {nombre_archivo}")

        except Exception as e:
            print(f"📁❌ Error al descargar {link}: {e}")

    def SiguientePagina():
        try:
            siguiente = driver.find_elements("css selector", "tbody a")[-1]
            
            if "Siguiente" in siguiente.text:
                time.sleep(3)
                siguiente.click()
                return True
            else:
                return False
        except Exception as e:
            print(f"❌ Error al intentar encontrar el botón de siguiente página: {e}")
            return False

    while True:
        ScrollPagina()
        time.sleep(3)
        ExtraerMetaDatos()
        time.sleep(3)
        if not SiguientePagina():
            print(f"\n🚀 No hay más páginas para `{palabra_clave}` en Google Académico.")
            break
        time.sleep(3)

    carpeta_clave = palabra_clave.replace(" ", "_").replace(":", "_")
    archivo_json = f'pdf/resultados_academico_{carpeta_clave}.json'
    datos = [{'titulo': Algoritmos_titulo[i], 'link': Algoritmos_link[i]} for i in range(len(Algoritmos_titulo))]
    
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    print(f"\nDatos guardados en {archivo_json}")
    driver.quit()