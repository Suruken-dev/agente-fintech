import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(
    page_title="Asistente Fintech",
    page_icon="🏦",
    layout="wide"
)

# Título
st.title("🏦 Agente Fintech")
st.markdown("Asistente virtual para consultas sobre documentos internos de FinBank Digital.")

# Inicializar el historial de mensajes en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar los mensajes del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Si es un mensaje del asistente y tiene fuentes, mostrarlas
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 Ver fuentes consultadas"):
                for source in message["sources"]:
                    st.write(f"- **{source['filename']}** (Categoría: {source['category']})")
                    st.caption(f"Fragmento: {source['content_preview']}")

# Entrada de texto para la pregunta
if prompt := st.chat_input("Escribe tu pregunta sobre FinBank..."):
    # Añadir la pregunta del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamar a la API
    with st.chat_message("assistant"):
        with st.spinner("🔍 Buscando en los documentos..."):
            try:
                # Ajusta la URL si tu API corre en otro puerto o máquina
                response = requests.post(
                    "http://localhost:8000/ask",
                    json={"question": prompt},
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])

                    st.markdown(answer)
                    if sources:
                        with st.expander("📚 Ver fuentes consultadas"):
                            for source in sources:
                                st.write(f"- **{source['filename']}** (Categoría: {source['category']})")
                                st.caption(f"Fragmento: {source['content_preview']}")

                    # Guardar la respuesta y fuentes en el historial
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                else:
                    error_msg = f"Error {response.status_code}: No se pudo obtener respuesta del servidor."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except requests.exceptions.ConnectionError:
                st.error("❌ No se pudo conectar con la API. Asegúrate de que el servidor esté corriendo en http://localhost:8000")
            except Exception as e:
                st.error(f"⚠️ Ocurrió un error: {str(e)}")