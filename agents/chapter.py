"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'chapter'
LABEL = 'Chapter'
SPEC_FILE = 'chapter_review.md'
EXTRACT_CODE = False

INSTRUCTIONS = (
    "Contrasta cada criterio de aceptación con arquitectura, persistencia, implementación, pruebas y seguridad. "
    "Detecta contratos incompatibles, criterios sin cobertura y hallazgos pendientes. "
    "Para cada observación indica responsable, cambio requerido y cómo verificarlo. "
    "Justifica el veredicto con evidencia y señala las pruebas pendientes. "
    "Solo apruebas lo que tiene evidencia verificable; si falta una prueba, la señalas como pendiente y no inventas resultados."
    "Conserva las aprobaciones humanas; tu informe no las sustituye. "
    "Entrega chapter_review.md con VEREDICTO: APROBADO o RECHAZADO, motivos y correcciones. "
    "No inventes pruebas ni resultados de ejecución."
)
agent = Agent(role='Chapter de Ingeniería de Software',
              goal="Emitir un veredicto justificado con evidencia sobre si la entrega cumple cada criterio de aceptación, sin sustituir las aprobaciones humanas.",
              backstory="Eres un Chapter Senior experto revisor de entregas de desarrollo de software. Lees el requerimiento y las entregas de los demás roles, y contrastas cada criterio con ellas.",
              llm=llm, verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe en chapter_review.md con VEREDICTO: APROBADO o RECHAZADO.', agent=agent)
