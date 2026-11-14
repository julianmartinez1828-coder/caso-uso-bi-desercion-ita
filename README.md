# Caso de Uso de Business Intelligence para el Seguimiento de la Deserción Estudiantil

## Guía 11 – Casos de Uso de BI

**Asignatura:** Inteligencia de Negocios Avanzada y Toma de Decisiones  
**Eje temático:** Business Analytics e Inteligencia Artificial  
**Institución analizada:** Instituto Tecnológico Andino (ITA)  
**Docente:** Juan José Osorio Tabares  
**Fecha:** Noviembre de 2026

## Integrantes

- Nelson Julián Martínez Bedoya
- Samuel Nieto Pardo
- Juan Sebastián Torres Agudelo
- Mauricio Esteban Varela Cañón

## Descripción del proyecto

Este proyecto presenta un caso de uso de Business Intelligence aplicado al seguimiento de la deserción estudiantil en el Instituto Tecnológico Andino (ITA), una institución educativa ficticia creada con fines académicos.

El propósito es integrar información académica, financiera y de bienestar para identificar los factores relacionados con la deserción y apoyar la toma de decisiones orientadas a la permanencia estudiantil.

## Problema identificado

La institución ha presentado un aumento progresivo en la deserción estudiantil. Sin embargo, la información se encuentra distribuida en diferentes sistemas y archivos, como el sistema académico, la plataforma virtual, el módulo financiero y los registros de Bienestar Institucional.

Esta situación dificulta identificar a tiempo los estudiantes que presentan señales de riesgo, conocer dónde se concentra el problema y establecer acciones de acompañamiento.

## Preguntas de negocio

El análisis busca responder las siguientes preguntas:

1. ¿En qué programas, sedes, modalidades y semestres se concentra la deserción estudiantil?
2. ¿Qué relación existe entre la asistencia, el rendimiento académico y la probabilidad de abandono?
3. ¿Qué influencia tienen la mora y el tipo de financiación en la decisión de retirarse?

## Objetivo general

Diseñar un caso de uso de Business Intelligence que integre datos académicos, financieros y de bienestar para identificar factores asociados a la deserción estudiantil y apoyar las decisiones de permanencia.

## Datos utilizados

La base de datos fue simulada con fines académicos y contiene 11.790 registros de matrícula correspondientes a los periodos comprendidos entre 2023-1 y 2026-1.

Las principales variables utilizadas son:

- Periodo académico.
- Sede.
- Programa.
- Modalidad.
- Semestre.
- Asistencia.
- Promedio académico.
- Estado de cartera.
- Tipo de financiación.
- Créditos inscritos.
- Créditos aprobados.
- Estado del estudiante.
- Nivel de riesgo.

Los datos no representan información real de una institución educativa.

## Fuentes de datos

Las fuentes consideradas para el caso de uso son:

- Sistema de Información Académica (SIA).
- Plataforma Moodle.
- Módulo financiero y de cartera.
- Archivos de Bienestar Institucional.
- Archivos Excel y CSV de apoyo.

## Proceso ETL

El proceso de preparación de los datos se desarrolló en tres etapas:

### Extracción

Se obtuvieron los datos académicos, financieros y de bienestar desde las fuentes definidas para el caso.

### Transformación

Se limpiaron los registros, se revisaron valores faltantes, se unificaron identificadores, se validaron los periodos y se calcularon variables derivadas como la tasa de deserción y el nivel de riesgo.

### Carga

Los datos transformados se consolidaron en un repositorio para realizar los cálculos, generar los indicadores y alimentar el dashboard.

## Indicadores KPI

El dashboard incluye los siguientes indicadores:

- Tasa de deserción.
- Porcentaje de estudiantes en mora.
- Asistencia promedio.
- Porcentaje de créditos aprobados.
- Número de estudiantes en riesgo alto.

Estos indicadores permiten observar el comportamiento general de la institución y localizar los grupos que requieren atención.

## Dashboard

El dashboard permite analizar la información mediante:

- Tarjetas KPI.
- Gráfico de deserción por periodo.
- Gráfico de deserción por programa.
- Gráfico de deserción según el nivel de asistencia.
- Tabla de detalle por sede.
- Filtro por periodo.
- Filtro por sede.
- Filtro por programa.
- Filtro por modalidad.
- Filtro por semestre.

La segmentación temporal permite comparar la evolución de la deserción entre los diferentes periodos académicos.

## Arquitectura de la solución

El flujo general de la solución es:

```text
Fuentes de datos
        ↓
Extracción
        ↓
Transformación y validación
        ↓
Repositorio de datos
        ↓
Cálculo de indicadores
        ↓
Dashboard
        ↓
Interpretación de resultados
        ↓
Toma de decisiones
