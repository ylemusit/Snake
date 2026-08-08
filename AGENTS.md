# Instrucciones del proyecto archivado

## Estado del proyecto

Este proyecto está archivado.

No se considera desarrollo activo.

Antes de modificar cualquier archivo:

1. Lee `docs/CURRENT_STATE.md`.
2. Identifica el motivo concreto por el que se ha retomado.
3. Inspecciona únicamente los archivos necesarios para esa tarea.
4. No modernices, refactorices ni actualices el proyecto por iniciativa propia.

## Principio de trabajo

Trabaja con el contexto mínimo suficiente.

No analices todo el repositorio por defecto.

No asumas que dependencias, versiones, integraciones o decisiones antiguas siguen siendo vigentes.

Si una tarea requiere información externa susceptible de haber cambiado, verifícala antes de implementarla.

## Alcance

Cada conversación debe centrarse en un único objetivo.

Si durante el trabajo aparecen mejoras adicionales:

- no las implementes automáticamente;
- indícalas como pendientes;
- recomienda tratarlas en una tarea nueva.

## Conservación

Prioriza conservar el comportamiento y estructura existentes.

Evita:

- refactorizaciones generales;
- migraciones de framework;
- actualizaciones masivas de dependencias;
- cambios cosméticos;
- reestructuraciones innecesarias;
- eliminación de archivos históricos.

Solo realiza cambios estructurales si son necesarios para cumplir el objetivo solicitado.

## Verificación

Antes de considerar terminada una tarea:

- ejecuta la comprobación mínima relevante;
- verifica que no se ha roto el comportamiento existente;
- no ejecutes suites amplias si no son necesarias.

Si no puede verificarse el resultado, indícalo claramente.

## Documentación

Actualiza `docs/CURRENT_STATE.md` únicamente si el estado del proyecto cambia materialmente.

Si el proyecto vuelve a desarrollo activo, no continúes tratándolo como archivado.

En ese caso, recomienda migrarlo a la estructura `ACTIVE`.

## Finalización

Al terminar informa de forma compacta:

1. qué se ha cambiado;
2. qué archivos se han modificado;
3. cómo se ha verificado;
4. si el proyecto continúa archivado o debe reactivarse.