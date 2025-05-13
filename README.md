# Katara
Algoritmo OSINT para la identificación, descarga, recopilación y clasificación automática de archivos TXT y PDF en los motores de búsqueda Google y Google Scholar.

## Video de complementación
https://youtu.be/ifU7aYgq4ls 

## 🚀 Estructura "Katara"

Dentro del proyecto, verás las siguientes carpetas y archivos:

```text
├── __pycache__/
├── env/
├── pdf/
│   ├── __search_filetype_pdf/
│   ├── __search_filetype_txt/
│   ├── __resultados_academico_search_filetype_pdf.json
│   ├── __resultados_academico_search_filetype_txt.json
│   ├── __resultados_google_search_filetype_pdf.json
│   ├── __resultados_google_search_filetype_txt.json
│   └── Clasificaciòn archivos/
├── buscarGoogle.py
├── buscarGoogleAcademico.py
├── clasificador.py
├── main.py
└── requirements.txt
```

## 🧞 Comandos

Todos los comandos se ejecutan desde la raíz del proyecto, desde un terminal:

| Command                             | Action                                                        |
| :-----------------------------------| :-------------------------------------------------------------|
| `pip install requirements.txt`      | Instala las dependencias                                      |
| `python main.py`                    | Inicia el proyecto y descarga el modelo de clasificaciòn      |

## 👀 ¿Què modelo de clasificaciòn usamos?

https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B 

## ¿Qué es DeepSeek?

DeepSeek-R1-Zero, un modelo entrenado mediante aprendizaje por refuerzo a gran escala (RL) sin un ajuste fino supervisado (SFT) como paso preliminar, demostró un rendimiento notable en tareas de razonamiento. Gracias al RL, DeepSeek-R1-Zero desarrolló de forma natural numerosos comportamientos de razonamiento potentes e interesantes.

Sin embargo, DeepSeek-R1-Zero enfrenta desafíos como repeticiones interminables, baja legibilidad y mezcla de idiomas. Para abordar estos problemas y mejorar aún más el rendimiento en razonamiento, presentamos DeepSeek-R1, que incorpora datos de inicio en frío antes del entrenamiento con RL. DeepSeek-R1 logra un rendimiento comparable al de OpenAI-o1 en tareas de matemáticas, programación y razonamiento.

Para apoyar a la comunidad de investigación, hemos liberado el código abierto de DeepSeek-R1-Zero, DeepSeek-R1 y seis modelos densos destilados a partir de DeepSeek-R1, basados en Llama y Qwen. DeepSeek-R1-Distill-Qwen-32B supera a OpenAI-o1-mini en diversas métricas de evaluación, estableciendo nuevos resultados de vanguardia para modelos densos.

## 👀 ¿Còmo funciona el Algoritmo Osint Katara?

El sistema desarrollado tiene como objetivo automatizar el análisis, clasificación y extracción de información visual (algoritmos y diagramas) desde archivos PDF y TXT obtenidos mediante técnicas OSINT. Para ello, se emplean dos componentes clave de inteligencia artificial:

- Un modelo de lenguaje de gran escala (LLM): [DeepSeek-R1-Distill-Qwen-1.5B] para clasificación semántica.
- Una red neuronal convolucional (CNN) personalizada para la detección visual de algoritmos en documentos escaneados o renderizados como imagen.

1. Pipeline General del Sistema

El sistema sigue el siguiente flujo:

1. **Descarga de documentos PDF/TXT** desde búsquedas en Google utilizando Selenium.
2. **Clasificación textual** de los documentos con un modelo LLM (DeepSeek).
3. **Extracción y análisis visual** de documentos clasificados como "Ejercicios" mediante un modelo CNN.

---

2. Clasificación con DeepSeek

El modelo [`DeepSeek-R1-Distill-Qwen-1.5B`] es una versión eficiente de un LLM autoregresivo entrenado en múltiples tareas de lenguaje natural. Se emplea aquí como un **clasificador semántico multitarea**:

#### Proceso:

1. Se extrae el texto de los documentos PDF/TXT utilizando `pdfplumber` o lectura directa.
2. Se construye un *prompt instructivo*, como:
3. Se envía el prompt al modelo DeepSeek mediante `transformers.pipeline("text-generation")`.
4. El resultado es un texto generado por el modelo donde se infiere una categoría.
5. Si la categoría coincide con alguna de las definidas, se clasifica el archivo y se mueve a su carpeta correspondiente.

---

3. Procesamiento con CNN

Los archivos clasificados como **“Ejercicios”** se asumen como candidatos a contener **algoritmos escritos o diagramas de flujo**. Dado que pueden estar embebidos como imágenes o escaneos, se emplea un modelo **CNN personalizado** para detectarlos visualmente.

#### Proceso:

1. Se renderiza cada página del PDF como una imagen `.png` (con `PyMuPDF`).
2. Estas imágenes se pasan por la **red neuronal convolucional**, entrenada previamente con un dataset de imágenes con y sin algoritmos.
3. La CNN devuelve una probabilidad o etiqueta binaria:
- `1`: contiene algoritmo o diagrama.
- `0`: irrelevante.
4. Solo las imágenes etiquetadas como positivas se guardan en la carpeta `"imagenes de algoritmos"`.

---

4. Resultados Esperados

- Documentos correctamente clasificados en carpetas por tipo: teoría, ejercicios, diagramas.
- Imágenes con algoritmos extraídas de documentos escaneados sin intervención humana.
- Flujo completamente automatizado y escalable para grandes volúmenes de archivos.


