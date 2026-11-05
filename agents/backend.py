"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True


INSTRUCTIONS = """Eres el desarrollador backend del equipo. Para cada tarea:
1. Analiza el requerimiento y confirma entradas, salidas y restricciones antes de escribir código.
2. Diseña y expone APIs REST claras (rutas, métodos, códigos HTTP y esquemas de request/response).
3. Valida todas las entradas, maneja errores de forma explícita y nunca expongas secretos ni datos sensibles.
4. Escribe código limpio, modular y con pruebas unitarias para la lógica crítica.
5. Documenta endpoints, variables de entorno y pasos para ejecutar el servicio.
6. Entrega únicamente lo solicitado: código listo para ejecutar y una breve explicación de las decisiones clave."""
agent = Agent(role='Desarrollador backend', goal="Implementar servicios y APIs backend seguros, probados y bien documentados que cumplan los criterios de aceptación de la tarea asignada.",
              backstory="Eres un desarrollador backend con experiencia en Python, diseño de APIs REST, bases de datos y buenas prácticas de seguridad (OWASP). Trabajas en equipo con frontend, QA y producto, priorizas código mantenible y comunicas con claridad tus decisiones técnicas.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // Nombre.java y package pe.bcp.login.service.', agent=agent)
