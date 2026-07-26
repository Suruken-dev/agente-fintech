import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Cargar variables de entorno (.env)
load_dotenv()

# Rutas y parámetros desde el archivo .env
DATA_PATH = "./data"
VECTORSTORE_PATH = os.getenv("VECTORSTORE_DIR", "./vectorstore")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

# --------------------------------------------------------------------
# Mapeo de categorías (Fase 1) basado en el nombre del archivo
# --------------------------------------------------------------------
CATEGORY_MAP = {
    "politica_privacidad": "Legal y Compliance",
    "terminos_condiciones": "Legal y Compliance",
    "tarifas_comisiones": "Financiero y Contable",
    "faq_transacciones": "Operacional",
    "seguridad_fraudes": "Legal y Compliance",
    "catalogo_productos": "Marketing y Comercial"
}

def get_category(filename):
    """Asigna una categoría según el nombre del archivo."""
    for key, category in CATEGORY_MAP.items():
        if key in filename.lower():
            return category
    return "General"

# --------------------------------------------------------------------
# Inicio del proceso de ingestión
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Iniciando proceso de ingestión...")
    print(f"📂 Leyendo documentos desde: {DATA_PATH}")
    
    # 1. Cargar TODOS los archivos con UnstructuredFileLoader
    #    (soporta PDF, DOCX, XLSX, MD, HTML, CSV y muchos más)
    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.*",  # Lee todos los archivos de la carpeta y subcarpetas
        loader_cls=UnstructuredFileLoader,
        show_progress=True,
        loader_kwargs={"mode": "single"}  # Extrae el texto completo del documento
    )
    docs = loader.load()
    
    if not docs:
        print("❌ No se encontraron documentos en la carpeta data/")
        exit(1)
    
    print(f"✅ Documentos cargados: {len(docs)}")
    
    # 2. Enriquecer con metadatos (categoría, responsable, fecha, etc.)
    for doc in docs:
        source_path = doc.metadata.get("source", "")
        filename = os.path.basename(source_path)
        
        # Asignar categoría
        category = get_category(filename)
        doc.metadata["category"] = category
        doc.metadata["filename"] = filename
        
        # Asignar responsable (dueño del documento)
        doc.metadata["responsible"] = f"Área de {category.split(' y ')[0] if ' y ' in category else category.split(' ')[0]}"
        
        # Guardar la ruta relativa para citar la fuente en la respuesta
        doc.metadata["source_path"] = source_path
        
        # Fecha de ingestión
        doc.metadata["ingested_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"  📄 {filename} → {category}")
    
    # 3. Dividir el texto en fragmentos (chunks) con superposición
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )
    chunks = text_splitter.split_documents(docs)
    print(f"✂️  Documentos divididos en {len(chunks)} fragmentos (chunks)")
    
    # 4. Generar los embeddings (vectores numéricos)
    print(f"🧠 Generando embeddings con el modelo: {EMBEDDINGS_MODEL}")
    print("   (Esto puede tomar unos minutos la primera vez que descarga el modelo...)")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)
    
    # 5. Construir el índice FAISS y guardarlo en disco
    print(f"💾 Construyendo índice FAISS y guardando en: {VECTORSTORE_PATH}")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_PATH)
    
    print("✅ ¡Ingestión completada exitosamente!")
    print(f"📊 Vectorstore guardado en: {VECTORSTORE_PATH}")
    print(f"📌 Total de documentos indexados: {len(docs)}")
    print(f"📌 Total de fragmentos (chunks) indexados: {len(chunks)}")