# ==== PERSISTENCIA ====

import os
import re
from data import get_all_data

# Gemini SDK moderno
from google import genai


# ===== CONFIG CLIENTE =====
def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Falta GEMINI_API_KEY en variables de entorno")

    return genai.Client(api_key=api_key)


# ===== PROMPT ENGINEERING =====
def construir_prompt_usuario(user_prompt):
    return f"""
        Eres un traductor de lenguaje natural a SQL.

        Reglas:
        - SOLO responde con SQL válido
        - NO uses markdown (no ```sql)
        - Tabla: accidentes
        - Columnas disponibles:
        ID, Severity, Start_Time, End_Time, City, State,
        Temperature(F), Visibility(mi), Weather_Condition
        - Usa LIMIT para limitar resultados
        - NO expliques nada

        Ejemplo:
        Usuario: dame 5 accidentes
        SQL: SELECT * FROM accidentes LIMIT 5;

        Usuario:
        {user_prompt}
    """


# ===== LIMPIEZA DE RESPUESTA =====
def limpiar_query(texto):
    texto = texto.strip()
    texto = texto.replace("```sql", "")
    texto = texto.replace("```", "")
    return texto.strip()


# ===== LLM → QUERY =====
def generar_query_con_llm(user_prompt):
    client = get_client()
    prompt = construir_prompt_usuario(user_prompt)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    return limpiar_query(response.text)


# ===== EJECUCIÓN DE QUERY =====
def ejecutar_query(query):
    data = get_all_data()

    # limpiar por seguridad
    query = limpiar_query(query)

    # ===== LIMIT =====
    limit_match = re.search(r"LIMIT (\d+)", query, re.IGNORECASE)
    if limit_match:
        n = int(limit_match.group(1))
        return data.head(n)

    # ===== SELECT básico =====
    if "SELECT" in query.upper():
        return data

    return "Query no soportado"


# ===== FLUJO COMPLETO =====
def ejecutar_prompt(prompt):
    query = generar_query_con_llm(prompt)
    resultado = ejecutar_query(query)

    return {
        "prompt": prompt,
        "query_generado": query,
        "resultado": resultado
    }