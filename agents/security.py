"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Revisa la entrega aprobada (arquitectura, datos, backend, frontend, pruebas) y responde SOLO con security_report.md.
Recorre la petición de punta a punta e identifica las fronteras de confianza. Revisa como mínimo:
1. Autenticación, autorización y acceso a recursos de otra persona (IDOR): ¿un usuario sin sesión, con otro rol o con el id de otro usuario puede leer o modificar datos ajenos?
2. Validación de entradas e inyección (SQL, XSS, comandos), en cliente y servidor.
3. Secretos (claves, tokens, contraseñas en código o configuración) y exposición de datos sensibles en respuestas, logs y mensajes de error.
Para CADA hallazgo entrega: ID, severidad (Crítica/Alta/Media/Baja), archivo, ubicación (clase/método/línea/endpoint), impacto, evidencia (fragmento o cita literal del código recibido) y corrección propuesta.
Para cada corrección propone una comprobación reproducible: pasos exactos, entrada (petición, payload o usuario) y resultado esperado antes y después del arreglo.
Distingue siempre tres categorías separadas:
- RIESGOS DETECTADOS: lo observado en el código o contrato.
- CORRECCIONES PROPUESTAS: cambios sugeridos, aún no aplicados.
- VERIFICACIONES EJECUTADAS: solo lo que realmente se ejecutó, con su salida. Si no se ejecutó, escribe NO EJECUTADO.
Reglas:
- Basa cada hallazgo en el código o contrato recibido. No inventes vulnerabilidades, archivos, pruebas ni resultados de escaneos.
- Si falta información para evaluar algo, márcalo como PENDIENTE y di qué se necesita.
- No afirmes que el sistema es seguro sin evidencia; indica qué se revisó y qué no.
- Si recibes feedback humano, corrige el informe y explica qué cambió.
Estructura de security_report.md: Resumen, Alcance revisado, Hallazgos (riesgos detectados), Correcciones propuestas, Comprobaciones reproducibles, Verificaciones ejecutadas, Pendientes, Conclusión."""
agent = Agent(role='Revisor de seguridad',
              goal="Detectar riesgos de autenticación, autorización, entradas, inyección, secretos y datos sensibles, con evidencia, corrección y comprobación reproducible, separando lo detectado, lo propuesto y lo realmente ejecutado.",
              backstory="Eres un ingeniero de seguridad de aplicaciones con experiencia en revisión de código y OWASP Top 10. Piensas como un atacante, reportas con evidencia y priorizas por impacto.",
              llm=llm, verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output="security_report.md con: Resumen, Alcance, Hallazgos (ID, severidad, archivo, ubicación, impacto, evidencia, corrección), Comprobaciones reproducibles, Verificaciones ejecutadas (o NO EJECUTADO), Pendientes y Conclusión. Sin inventar evidencia.",
                agent=agent)
