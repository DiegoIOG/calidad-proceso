# ETL de Calidad de Proceso – Python → Excel → Power BI

## Descripción
Proyecto de ingeniería de datos que implementa un **pipeline ETL de calidad de proceso industrial**.  
El flujo del proyecto:

1. **Generación de datos simulados** de producción (piezas producidas y defectuosas por máquina, turno y producto).  
2. **Limpieza de datos** aplicando reglas de calidad:  
   - eliminar registros con piezas producidas ≤ 0  
   - eliminar registros con piezas defectuosas < 0  
   - eliminar registros con campos vacíos (maquina, turno, producto)  
3. **Cálculo de métricas de calidad**:  
   - Tasa de defectos por registro  
   - Bandera de calidad (OK / NO OK)  
   - KPIs agregados: total producidas, total defectuosas, promedio tasa de defectos  
4. **Exportación a Excel** con 2 hojas listas para Power BI:  
   - datos_limpios → datos limpios por registro  
   - kpis_calidad → resumen de métricas de calidad  
5 **Dashboard Power Bi** :
   - Filtros  Fecha , Producto, Maquina ,Turno y Total de registros 
   - Grafica de lineas comparacion por defecto
   - Grafica Barra de pastel por piezas OK Y NO OK

---

## Herramientas

- Python  
- pandas → manipulación de datos  
- faker → generación de datos simulados  
- openpyxl → exportación a Excel  
- datetime → manejo de fechas  
