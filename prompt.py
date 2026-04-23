# ==== PROMPT ====

def ejemplo_prompts():
    return [
        "Muéstrame los primeros 5 accidentes",
        "Dame accidentes en California",
        "Quiero ver la severidad de accidentes",
        "Dame 10 accidentes con visibilidad baja"
    ]


def ayuda_prompt():
    return """
Ejemplos de uso del sistema:

--prompt "Muéstrame los primeros 10 accidentes"
--presentacion "Hola mundo"
--negocio all
--data all
--data 5
--query "SELECT * FROM accidentes LIMIT 5"
"""