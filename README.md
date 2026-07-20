# Alura Agente - Santo Pegasus Soluciones

**Desarrollado por:** Nathaly Prieto

Este proyecto es la entrega final del **Challenge Alura Agente** para la formación ONE AI FOR TECH. Consiste en un asistente de Inteligencia Artificial desarrollado para interactuar con la base de conocimiento interno (manuales, arquitectura e incidentes) de la empresa Santo Pegasus Soluciones.

## Descripción General

El objetivo de este proyecto es resolver la pérdida de tiempo en la búsqueda de información interna. El agente permite a los colaboradores realizar preguntas en lenguaje natural y obtener respuestas precisas, extraídas exclusivamente de los documentos oficiales de la empresa, evitando alucinaciones mediante un prompt de sistema estricto.

## Arquitectura de la Solución

El sistema utiliza una arquitectura RAG (Retrieval-Augmented Generation) compuesta por las siguientes etapas:

1. **Extracción y Carga:** Se utiliza `PyPDFLoader` para leer el documento de arquitectura de microservicios.
2. **Chunking:** El texto se divide en fragmentos de 1200 caracteres con un solapamiento de 150 usando `RecursiveCharacterTextSplitter`.
3. **Indexación Vectorial:** Se generan embeddings utilizando el modelo `gemini-embedding-001` de Google y se almacenan en una base de datos vectorial `Chroma`.
4. **Recuperación (Retrieval):** Se recuperan los 4 fragmentos (K=4) más relevantes semánticamente según la consulta del usuario.
5. **Generación:** El modelo `gemini-3.5-flash` recibe el contexto recuperado y formula la respuesta final, respetando la regla de no inventar información.

## Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Framework Web:** Streamlit
* **Orquestación IA:** LangChain / LangChain Classic
* **Modelos IA:** Google Gemini API (Generación y Embeddings)
* **Base de Datos Vectorial:** ChromaDB
* **Despliegue Cloud:** Oracle Cloud Infrastructure (OCI Compute)

## Instrucciones de Ejecución (Local)

1. Clona este repositorio.
2. Crea un entorno virtual e instala las dependencias (`pip install -r requirements.txt`). *Asegúrate de tener instalados `langchain`, `langchain-classic`, `langchain-google-genai`, `streamlit`, `chromadb` y `pypdf`.*
3. Coloca el PDF de Santo Pegasus en la raíz del proyecto: `Arquitectura de Microservicios y Mapa de Dominios — Santo Pegasus Soluciones.pdf`
4. Configura tu variable de entorno con tu API Key de Gemini:

   ```bash
   export GOOGLE_API_KEY="tu_clave_aqui"
   ```

5. Ejecuta la aplicación:

   ```bash
   streamlit run app.py
   ```

## Despliegue en OCI

La aplicación fue desplegada en una instancia de **OCI Compute** (Ubuntu). Para exponerla en la red:

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Recuerda configurar las reglas de **Security List / Network Security Group** para permitir tráfico entrante en el puerto 8501.

## Evidencias del Despliegue en OCI

**1. Pantalla Inicial (Indexación exitosa):**

![Indexación](evidencias/challenge1.png)

**2. Prueba de flujo (Agendamiento):**

![Flujo Agendamiento](evidencias/challenge2.png)

**3. Prueba técnica (Auth Service):**

![Prueba Auth](evidencias/challenge3.png)

**4. Control de alucinaciones (Fallback):**

![Prueba Alucinacion](evidencias/challenge4.png)
