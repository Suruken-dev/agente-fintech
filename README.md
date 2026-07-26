<!-- Título principal con badge de estado -->
# 🏦 Agente Fintech · Asistente Virtual con RAG

<!-- Insignias (puedes cambiar los enlaces) -->
<p align="center">
  <img src="https://img.shields.io/badge/versión-1.0.0-blue.svg" alt="Versión">
  <img src="https://img.shields.io/badge/Python-3.12+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/LangChain-✅-orange.svg" alt="LangChain">
  <img src="https://img.shields.io/badge/Streamlit-✅-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/FastAPI-✅-teal.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/FAISS-✅-purple.svg" alt="FAISS">
  <img src="https://img.shields.io/badge/Despliegue-OCI-✔️-brightgreen.svg" alt="OCI">
</p>

---

## 📖 Descripción del Proyecto

Este proyecto consiste en un **agente de inteligencia artificial corporativo** diseñado para responder preguntas de los colaboradores de una empresa Fintech, basándose exclusivamente en documentos internos como políticas de privacidad, términos y condiciones, tarifas, preguntas frecuentes y catálogos de productos.

El sistema utiliza **RAG (Retrieval-Augmented Generation)** para recuperar fragmentos relevantes de los documentos y generar respuestas precisas, citando siempre las fuentes originales.

### 🎯 Objetivo
- Proporcionar un asistente conversacional accesible para todos los empleados.
- Garantizar respuestas basadas en información oficial y actualizada.
- Reducir el tiempo de búsqueda en la documentación interna.
- Ofrecer trazabilidad mediante la citación de fuentes.

---

## ✨ Características principales

- ✅ **Multi‑formato**: Soporta PDF, Word, Excel, Markdown, HTML y CSV.
- ✅ **Indexación vectorial**: Embeddings con `paraphrase-multilingual-MiniLM-L12-v2` y FAISS.
- ✅ **Backend robusto**: API REST con FastAPI y LangChain.
- ✅ **Interfaz amigable**: Chat web con Streamlit, historial y visualización de fuentes.
- ✅ **Contenerización**: Docker y Docker Compose listos para despliegue.
- ✅ **Despliegue en la nube**: Preparado para Oracle Cloud Infrastructure (OCI).
- ✅ **Trazabilidad**: Registro de preguntas y respuestas en logs.

---

## 🧰 Tecnologías utilizadas

| Categoría | Tecnología |
| :--- | :--- |
| **Lenguaje** | Python 3.12 |
| **Framework Backend** | FastAPI, Uvicorn |
| **Frontend** | Streamlit |
| **Procesamiento de documentos** | LangChain, Unstructured, PyPDF, python-docx, openpyxl |
| **Embeddings** | HuggingFace `paraphrase-multilingual-MiniLM-L12-v2` |
| **Vectorstore** | FAISS (búsqueda semántica local) |
| **LLM** | Google Gemini (vía `langchain-google-genai`) |
| **Contenerización** | Docker, Docker Compose |
| **Nube** | Oracle Cloud Infrastructure (OCI) |

---

## 📂 Estructura del proyecto
agente-fintech/
├── app/
│ ├── api.py # Endpoints FastAPI
│ ├── ingest.py # Pipeline de ingestión y generación del vectorstore
│ └── rag.py # Lógica RAG (recuperación + generación)
├── ui/
│ └── app.py # Aplicación Streamlit (chat web)
├── data/ # Documentos fuente (PDF, Word, Excel, etc.)
├── vectorstore/ # Índice FAISS generado (local)
├── logs/ # Registros de actividad
├── requirements.txt # Dependencias Python
├── Dockerfile # Imagen Docker
├── docker-compose.yml # Orquestación de contenedores
├── .env # Variables de entorno (NO subir a GitHub)
├── .gitignore # Archivos a excluir
└── README.md # Este archivo
---

## 🚀 Instalación y ejecución local

### 1. Clonar el repositorio
```bash
git clone https://github.com/Suruken-dev/agente-fintech.git
cd agente-fintech

### 2. Crear y activar entorno virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

#3. Instalar dependencias
pip install -r requirements.txt

#4. Configurar variables de entorno

Crea un archivo .env en la raíz con tu clave de Gemini:

GOOGLE_API_KEY=tu_clave_aqui
VECTORSTORE_DIR=./vectorstore
EMBEDDINGS_MODEL=paraphrase-multilingual-MiniLM-L12-v2
LLM_MODEL=gemini-2.0-flash-001
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_DOCUMENTS=5

#5. Indexar los documentos (generar vectorstore)
python app/ingest.py

#6. Ejecutar la API (FastAPI)
uvicorn app.api:app --reload --host 127.0.0.1 --port 8000

#7. Ejecutar la interfaz (Streamlit)
En otra terminal (con el entorno activado):

streamlit run ui/app.py

#8. Abrir el navegador
API: http://localhost:8000/docs

Interfaz: http://localhost:8501


🐳 Despliegue en Oracle Cloud (OCI)
El proyecto está contenerizado para facilitar el despliegue en OCI.

1. Construir la imagen Docker
bash
docker build -t agente-fintech .
2. Ejecutar con Docker Compose
bash
docker-compose up -d
3. En OCI Compute (VM)
Crear una instancia VM.Standard.E2.1.Micro (Always Free).

Instalar Docker y Docker Compose.

Clonar el repositorio.

Configurar el archivo .env con las variables necesarias.

Ejecutar docker-compose up -d.

Abrir los puertos 8000 (API) y 8501 (Streamlit) en la VCN.

📸 Evidencia de ejecución en la nube
Requisito del desafío: Incluir una imagen o video del agente funcionando en la nube.

<img src="https://via.placeholder.com/800x400?text=Captura+de+pantalla+del+agente+en+OCI" alt="Agente ejecutándose en OCI" width="800">
(Reemplaza este placeholder con tu captura real una vez desplegado).

🤝 Cómo contribuir
Haz un fork del proyecto.

Crea tu rama de características (git checkout -b feature/nueva-funcionalidad).

Realiza tus cambios y haz commit (git commit -m 'Añadir nueva funcionalidad').

Sube tu rama (git push origin feature/nueva-funcionalidad).

Abre un Pull Request.

📄 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

✒️ Autor
Andrés
GitHub · LinkedIn

🙏 Agradecimientos
Alura Latam por el desafío y el material educativo.

Google Gemini por la API de LLM.

Comunidad de código abierto por las herramientas utilizadas.

<p align="center">Hecho con ❤️ para aprender y compartir.</p> ```
🎨 Notas para personalizar:
Insignias: Las rutas de las insignias son ejemplos genéricos. Puedes personalizarlas desde shields.io.

Imagen de evidencia: Reemplaza el placeholder de la captura por una imagen real de tu agente ejecutándose en OCI (es un requisito del desafío).

Autor: Cambia los enlaces y el nombre por los tuyos.

Licencia: Si no tienes licencia, puedes omitir esa sección o añadir una.
