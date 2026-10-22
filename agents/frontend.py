"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = (
    "Implementa el recorrido del usuario según el contrato de API aprobado. "
    "Define campos, validaciones, acciones y mensajes. Cubre estados de carga, "
    "vacío, éxito y error, y evita envíos duplicados. Conserva etiquetas "
    "accesibles, navegación por teclado y foco visible. Incluye cómo comprobar "
    "el recorrido y sus errores."
)
agent = Agent(role='Desarrollador frontend',
              goal="Implementar el recorrido Angular según el contrato de API aprobado.",
              backstory="Eres responsable de la experiencia de usuario, accesibilidad y consumo del API en la interfaz Angular.",
              llm=llm, verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=(
                    'frontend_spec.md con el recorrido de usuario según el contrato de API, '
                    'campos, validaciones, acciones, mensajes, estados de carga, vacío, éxito y '
                    'error, prevención de envíos duplicados, accesibilidad por teclado y pasos '
                    'para comprobar el recorrido y sus errores. Incluye código Angular en bloques '
                    'markdown, uno por archivo, con la primera línea // nombre.component.ts, '
                    '// nombre.component.html, // nombre.component.css o // nombre.service.ts.'
                ), agent=agent)
