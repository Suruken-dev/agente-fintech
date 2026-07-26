import os
import time
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "./vectorstore")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-flash-001")
TOP_K = int(os.getenv("TOP_K_DOCUMENTS", 5))

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("❌ GOOGLE_API_KEY no encontrada en .env")

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)
vectorstore = FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)

# Inicializamos el LLM (se creará dentro de la función para poder reintentar)
def create_llm():
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=google_api_key,
        temperature=0.2,
        top_p=0.95,
        convert_system_message_to_human=True,
    )

prompt_template = """
Eres un asistente corporativo especializado en responder preguntas basándote ÚNICAMENTE en el contexto proporcionado.

INSTRUCCIONES:
- Si la respuesta NO está en el contexto, di claramente: "No encontré información sobre eso en los documentos disponibles."
- NO uses conocimiento externo.
- Cita la fuente de cada información usando el nombre del archivo y la página (si está disponible).
- Si hay varias fuentes, enuméralas al final.

CONTEXTO:
{context}

PREGUNTA: {question}

RESPUESTA:
"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

def ask_question_with_retry(question: str, max_retries=3):
    """
    Intenta hacer la pregunta con reintentos en caso de error 429 (cuota).
    """
    retries = 0
    backoff = 2  # segundos iniciales

    while retries <= max_retries:
        try:
            # Crear una nueva instancia de LLM en cada intento (por si acaso)
            llm = create_llm()
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={"k": TOP_K}),
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True,
            )
            result = qa_chain.invoke({"query": question})
            
            # Si llegamos aquí, fue exitoso
            answer = result["result"]
            sources = []
            for doc in result["source_documents"]:
                sources.append({
                    "filename": doc.metadata.get("filename", "Desconocido"),
                    "category": doc.metadata.get("category", "General"),
                    "page": doc.metadata.get("page", "N/A"),
                    "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
            return {
                "question": question,
                "answer": answer,
                "sources": sources
            }
        
        except ResourceExhausted as e:
            # Error 429 (cuota excedida)
            retries += 1
            if retries > max_retries:
                raise Exception("Se agotaron los reintentos por cuota excedida. Intenta más tarde.") from e
            print(f"⚠️ Cuota excedida. Reintento {retries}/{max_retries} en {backoff} segundos...")
            time.sleep(backoff)
            backoff *= 2  # backoff exponencial: 2, 4, 8 segundos
        
        except Exception as e:
            # Otros errores (404, etc.) los lanzamos directamente
            raise e
    
    # Fallback por si sale del bucle sin retorno
    raise Exception("No se pudo completar la pregunta después de varios intentos.")

# Función pública para mantener la interfaz igual que antes
def ask_question(question: str):
    return ask_question_with_retry(question)