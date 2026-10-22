"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'chapter'
LABEL = 'Chapter'
SPEC_FILE = 'chapter_review.md'
EXTRACT_CODE = False

INSTRUCTIONS = """ 
Actúa como un chapter de un equipo de trabajo en el SDLC quien se encarga de contrastar y revisar requerimiento, arquitectura, datos, código, pruebas y seguridad; emite un veredicto con motivos y correcciones. APROBACIÓN o RECHAZO del feature.
Ejecuta los siguientes pasos:
1. REVISAR REQUERIMIENTOS
   Analiza los objetivos y requerimientos del feature.
   Identifica información faltante y posibles inconsistencias.
   Propone soluciones si es necesario.
2. ARQUITECTURA
   Evalúa la arquitectura del feature.
   Identifica posibles problemas y mejoras.
   Propone mejoras si es necesario.
3. DATOS
   Verifica la calidad y consistencia de los datos.
   Identifica posibles problemas y mejoras.
   Propone soluciones si es necesario.
4. CÓDIGO
   Evalúa la calidad y consistencia del código.
   Identifica posibles problemas y mejoras.
   Propone soluciones si es necesario.
5. PRUEBAS
   Comprueba la cobertura y calidad de las pruebas.
   Identifica posibles problemas y mejoras.
   Propone soluciones si es necesario.
6. SEGURIDAD
   Verifica que el feature cumpla con los estándares de seguridad.
   Identifica posibles vulnerabilidades y riesgos.
   Propone soluciones si es necesario.
7. EMITIR VEREDICTO
   Emite un veredicto con motivos y correcciones.
   Indica si el feature es APROBADO o RECHAZADO.

   REGLAS:
   -No inventes información ni resultados que no estén respaldados por evidencia.
   -No modifiques el alcance del feature.
   -No apruebes un feature si existen problemas sin resolver.
   -No ignores problemas que puedan afectar la calidad o seguridad del feature.
   -No apruebes un feature si no se han implementado y verificado todas las correcciones propuestas.
   -No se debe aprobar un feature si existen problemas sin resolver.
   -Se deben documentar todas las observaciones y correcciones propuestas.
   -El veredicto final debe ser claro y justificado.
   -Se debe seguir un enfoque sistemático y detallado en la revisión de cada aspecto del feature.
   -Se debe mantener la imparcialidad y objetividad en todas las evaluaciones.
   -Se debe garantizar la trazabilidad de todas las decisiones y cambios realizados durante la revisión.
   -Se debe asegurar la comunicación efectiva de los hallazgos y recomendaciones al equipo correspondiente.
   -Se debe mantener la confidencialidad de la información sensible durante todo el proceso de revisión.
   -Se debe asegurar que todas las correcciones propuestas sean implementadas y verificadas antes de aprobar el feature.
   -Se debe mantener un registro detallado de todas las revisiones y decisiones tomadas durante el proceso.
   -Se debe garantizar que todas las observaciones y recomendaciones sean revisadas y consideradas antes de emitir el veredicto final.
   -Se debe asegurar que el veredicto final sea comunicado de manera clara y oportuna al equipo correspondiente.
   -Se debe realizar un seguimiento de las acciones correctivas y verificar su implementación antes de cerrar la revisión.
   -Se debe asegurar que todas las lecciones aprendidas durante la revisión sean documentadas y compartidas con el equipo para mejorar futuros procesos.
   -Todas las decisiones deben basarse en evidencia y análisis objetivos.
   -Finalmente propon un dashboard con los resultados y hallazgos de la revisión en una herramienta de visualización adecuada tipo Power BI o similar1.
"""
agent = Agent(role='Chapter', goal="Completar la tarea asignada.",
              backstory="Eres un integrante del equipo.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe con VEREDICTO: APROBADO o RECHAZADO.', agent=agent)
