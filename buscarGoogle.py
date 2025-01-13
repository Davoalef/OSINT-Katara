from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import os
import time
import json
import requests


def BuscarGoogle(palabra_clave):
    from main import options
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com/")
    palabra = driver.find_element("css selector", "textarea[name='q']")
    palabra.clear()
    palabra.send_keys(palabra_clave)
    time.sleep(3)
    palabra.send_keys(Keys.RETURN)
    time.sleep(3)
    
    Algoritmos_titulo = []
    Algoritmos_link = []

    def ScrollPagina():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    
    def ExtraerMetaDatos():
        page = BeautifulSoup(driver.page_source, 'html.parser')
        for Algoritmos in page.findAll('a', attrs={'jsname': 'UWckNb'}):
            titulo = Algoritmos.find('h3', attrs={'class': 'LC20lb MBeuO DKV0Md'})
            if titulo:
                Algoritmos_titulo.append(titulo.text)
            else:
                Algoritmos_titulo.append('No hay título')
            
            link = Algoritmos.get('href')
            if link:
                Algoritmos_link.append(link)
                if link.endswith(".pdf"):
                    DescargarPDF(link, palabra_clave)
                    time.sleep(3)
            else:
                Algoritmos_link.append('No hay link')
    
    def DescargarPDF(link, carpeta_clave, tiempo_limite=60):
        try:
            carpeta_clave = palabra_clave.replace(" ", "_").replace(":", "_")
            Path(f"pdf/{carpeta_clave}").mkdir(parents=True, exist_ok=True)
            
            response = requests.get(link, timeout=tiempo_limite, stream=True)
            nombre_pdf = os.path.join(f"pdf/{carpeta_clave}", link.split("/")[-1])
            with open(nombre_pdf, 'wb') as f:
                f.write(response.content)
            print(f"PDF descargado en {nombre_pdf}")

        except Exception as e:
            print(f"Error al descargar el PDF {link}: {e}")

    def SiguientePagina():
        try:
            siguiente = driver.find_element("css selector", "a#pnnext")
            time.sleep(3)
            siguiente.click()
            time.sleep(3)
            return True
        except:
            return False

    while True:
        ScrollPagina()
        time.sleep(3)
        ExtraerMetaDatos()
        time.sleep(3)
        if not SiguientePagina():
            print(f"\nNo hay más páginas para {palabra_clave} en Google.")
            break
        time.sleep(3)
    
    carpeta_clave = palabra_clave.replace(" ", "_").replace(":", "_")
    archivo_json = f'pdf/resultados_google_{carpeta_clave}.json'
    datos = [{'titulo': Algoritmos_titulo[i], 'link': Algoritmos_link[i]} for i in range(len(Algoritmos_titulo))]
    
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    print(f"\nDatos guardados en {archivo_json}")
    driver.quit()

