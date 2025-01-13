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
    time.sleep(3)
    palabra.send_keys(Keys.RETURN)
    time.sleep(3)
    
    Algoritmos_titulo = []
    Algoritmos_link = []

    def ScrollPagina():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def ExtraerMetaDatos():
        page = BeautifulSoup(driver.page_source, 'html.parser')
        for resultado in page.findAll('div', attrs={'class': 'gs_r gs_or gs_scl'}):
            titulo = resultado.find('h3', attrs={'class': 'gs_rt'})
            if titulo and titulo.a:
                Algoritmos_titulo.append(titulo.text)
                link = titulo.a.get('href')
                Algoritmos_link.append(link)
                if link.endswith(".pdf"):
                    DescargarPDF(link, palabra_clave)
            else:
                Algoritmos_titulo.append('No hay título')
                Algoritmos_link.append('No hay link')

    def DescargarPDF(link, carpeta_clave, tiempo_limite=60):
        try:
            carpeta_clave = palabra_clave.replace(" ", "_").replace(":", "_")
            Path(f"pdf/{carpeta_clave}").mkdir(parents=True, exist_ok=True)
            
            response = requests.get(link, timeout=tiempo_limite, stream=True)
            nombre_pdf = os.path.join(f"pdf/{carpeta_clave}", link.split("/")[-1])
            with open(nombre_pdf, 'wb') as f:
                f.write(response.content)
            time.sleep(3)
            print(f"PDF descargado en {nombre_pdf}")

        except Exception as e:
            print(f"Error al descargar el PDF {link}: {e}")

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
            print(f"Error al intentar encontrar el botón de siguiente página: {e}")
            return False

    while True:
        ScrollPagina()
        time.sleep(3)
        ExtraerMetaDatos()
        time.sleep(3)
        if not SiguientePagina():
            print(f"\nNo hay más páginas para {palabra_clave} en Google Académico.")
            break
        time.sleep(3)

    carpeta_clave = palabra_clave.replace(" ", "_").replace(":", "_")
    archivo_json = f'pdf/resultados_academico_{carpeta_clave}.json'
    datos = [{'titulo': Algoritmos_titulo[i], 'link': Algoritmos_link[i]} for i in range(len(Algoritmos_titulo))]
    
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    print(f"\nDatos guardados en {archivo_json}")
    driver.quit()

