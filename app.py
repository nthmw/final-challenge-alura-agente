import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Configuración de interfaz básica requerida por el Challenge
st.set_page_config(page_title="Alura Agente - Santo Pegasus")
st.title("Santo Pegasus Soluciones - Asistente IA")
st.subheader("Base de conocimiento interno y soporte corporativo")

# Asegurar clave API
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "TU_GEMINI_API_KEY"

# Decorador para indexar el documento una sola vez en caché y optimizar rendimiento
@st.cache_resource
def inicializar_agente():
    # 1. Extracción y Carga
    loader = PyPDFLoader("Arquitectura de Microservicios y Mapa de Dominios — Santo Pegasus Soluciones.pdf")
    documentos = loader.load()

    # 2. Chunking reglamentario de Santo Pegasus (v2.4.0): máximo 512 tokens
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    chunks = text_splitter.split_documents(documentos)

    # 3. Indexación Vectorial (gemini-embedding-001)
    embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    vector_store = Chroma.from_documents(chunks, embeddings_model)

    # 4. Capa de Recuperación: Configurar K=4 estricto para evitar alucinaciones
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    # 5. Generación: Gemini 3.5 Flash
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.1)

    system_prompt = (
        "Eres el Agente de Inteligencia Artificial oficial de Santo Pegasus Soluciones.\n"
        "Tu tarea es responder preguntas de los colaboradores basándote exclusivamente en el contexto provisto.\n"
        "Si la solución o respuesta no se encuentra en el contexto, di textualmente:\n"
        "'No encontré esta información en los documentos disponibles.'\n"
        "Está terminantemente prohibido inventar datos, políticas o configuraciones.\n\n"
        "Contexto corporativo:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    document_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, document_chain)

# Instanciar la cadena RAG optimizada
try:
    rag_agent = inicializar_agente()
    st.success("Base de conocimientos indexada correctamente.")
except Exception as e:
    st.error(f"Error al inicializar la base de datos: {e}")

# Cuadro interactivo para la pregunta en lenguaje natural
user_query = st.text_input("Haz una pregunta sobre manuales, arquitectura, incidentes o políticas:")

if user_query:
    with st.spinner("Buscando en los manuales de Santo Pegasus..."):
        response = rag_agent.invoke({"input": user_query})
        st.markdown("### Respuesta del Agente:")
        st.write(response["answer"])
