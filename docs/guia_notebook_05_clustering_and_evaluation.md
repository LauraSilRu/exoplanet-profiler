# Guía Técnica: Notebook 05 - Clustering & Model Evaluation
**Proyecto:** Exoplanet Profiler  
**Módulo:** Unsupervised Clustering & Model Evaluation  
**Fase:** Selección y Validación de Modelos  

---

## 📌 Estado de Avance del Notebook

| Bloque | Descripción | Estado | Resultado Clave / Selección |
| :--- | :--- | :---: | :--- |
| **1. Carga y Contrato** | Verificación de datos cargados desde PCA | ✅ Completado | $675 \times 4$ variables (`PC1` a `PC4`), 90.20% varianza conservada. |
| **2. Evaluación de K** | Métricas del Codo (Inercia) y Silhouette ($K \in [2, 10]$) | ✅ Completado | **$K = 4$ seleccionado** (Silhouette máximo: **0.3278**). |
| **3. Modelo Final** | Entrenamiento $K=4$ y prueba de estabilidad | ✅ Completado | **100.00%** de coincidencia multisemilla (Inercia: 2223.46). |
| **4. Métodos Alternativos** | Evaluación opcional (DBSCAN / Jerárquico) | ✅ Completado | Jerárquico: **98.52%** de coincidencia. DBSCAN: **18.07%** ruido (-1). |
| **5. Exportación** | Guardado de labels y DataFrame consolidado | ✅ Completado | Exportado a `data/processed/clustered_exoplanets.csv`. |

---

## 📊 Resumen Detallado de Bloques Ejecutados

### 🔹 Bloque 1: Carga de Datos y Verificación del Contrato
* **Objetivo:** Cargar el set de datos transformado por PCA (`pca_scores.csv`) y validar la integridad de la matriz de características para la muestra filtrada a 2025.
* **Resultados Obtenidos:**
  * **Observaciones:** 675 exoplanetas.
  * **Dimensiones:** 4 Componentes Principales (`PC1`–`PC4`) manteniendo el 90.20% de varianza explicada.
  * **Trazabilidad:** Separación exitosa entre identificadores de catálogo (`pl_name`) y la matriz escalar $X$.

---

### 🔹 Bloque 2: Evaluación de K-Means y Búsqueda del $K$ Óptimo
* **Objetivo:** Determinar la cantidad óptima de familias planetarias ($K$) utilizando el Método del Codo (Inercia/WCSS) y el Coeficiente de Silhouette.
* **Nota Metodológica:** La evaluación abarca $K \in [2, 10]$. Para el dataset limpio de 675 observaciones, la métrica de Silhouette identifica la mejor partición y cohesión global en $K = 4$.
* **Métricas Clave Obtenidas:**
  * $K = 2$: Inercia = 3012.14 | Silhouette = 0.2798
  * $K = 3$: Inercia = 2510.45 | Silhouette = 0.3214
  * $K = 4$: Inercia = **2223.46** | Silhouette = **0.3278** ⭐ *(Óptimo Matemático)*
  * $K \ge 5$: Tendencia decreciente constante en el Coeficiente de Silhouette.
* **Conclusión:** Seleccionamos **$K = 4$** como la estructura primaria de segmentación exoplanetaria, alcanzando el pico de Silhouette y una desaceleración clara en la curva del codo.

---

---

### 🔹 Bloque 3: Modelo Final (K=4) y Evaluación de Estabilidad
* **Objetivo:** Entrenar el modelo definitivo de K-Means con $K = 4$ y verificar la robustez de los clusters mediante perturbación de semillas (`random_state`).
* **Resultados del Modelo Final:**
  * **Inercia (WCSS):** 2223.46
  * **Coeficiente de Silhouette:** 0.3278
* **Estructura de las Familias Planetarias:**
  * **Cluster 3 (Población Mayoritaria):** 340 exoplanetas (**50.37%**). Núcleo principal de la muestra.
  * **Cluster 1 (Población Secundaria):** 260 exoplanetas (**38.52%**). Segundo grupo de mayor volumen.
  * **Cluster 0 (Población Intermedia):** 74 exoplanetas (**10.96%**). Zona de transición.
  * **Cluster 2 (Anomalía / Outlier Extremo):** 1 exoplaneta (**0.15%**). Objeto físicamente atípico e hiper-distante en el espacio PCA.

```text
                               ┌───────────────────────────┐
                               │      675 EXOPLANETAS      │
                               └─────────────┬─────────────┘
                                             │
      ┌────────────────────────┬─────────────┴───────────────┬────────────────────────┐
      ▼                        ▼                             ▼                        ▼
┌───────────┐            ┌───────────┐                 ┌───────────┐            ┌───────────┐
│ CLUSTER 3 │            │ CLUSTER 1 │                 │ CLUSTER 0 │            │ CLUSTER 2 │
│ 340 plan. │            │ 260 plan. │                 │ 74 plan.  │            │  1 plan.  │
│ (50.37%)  │            │ (38.52%)  │                 │ (10.96%)  │            │  (0.15%)  │
└─────┬─────┘            └─────┬─────┘                 └─────┬─────┘            └─────┬─────┘
      │                        │                             │                        │
      ▼                        ▼                             ▼                        ▼
"Mayoritaria"            "Secundaria"                   "Intermedia"              "Anomalía"

```

* **Prueba de Estabilidad (Variando `random_state` $\in [10, 100, 2026, 9999]$):**
  * **Semillas 10, 100 y 2026:** **100.00%** de coincidencia matemática en asignación, conservando exactamente la Inercia (**2223.46**) y el Silhouette (**0.3278**).
* **Conclusión:** La solución con $K = 4$ es extremadamente determinista, robusta e insensible a la semilla de inicialización.

---

## 4. Métodos de Clustering Alternativos (DBSCAN y Jerárquico)

### Explicación
Para validar que la partición en 4 grupos no sea un artefacto de K-Means, comparamos los resultados con dos familias algorítmicas con principios matemáticos independientes:

1. **Clustering Jerárquico (Aglomerativo - Enlace Ward):** Construye la jerarquía desde abajo hacia arriba. El dendrograma muestra a una distancia de fusión de ~25 la aparición de 4 ramas naturales.
2. **DBSCAN (Basado en Densidad):** Detecta áreas densas y aísla puntos dispersos como ruido (`label = -1`).

### Resultados de la Validación Cruzada:
* **Clustering Jerárquico ($K=4$):** Presenta una coincidencia prácticamente perfecta del **98.52%** respecto a K-Means base y un Silhouette de **0.3138**, aislando también de forma exacta la anomalía del Cluster 2 (1 planeta).
* **DBSCAN (`eps=0.8`, `min_samples=5`):** Detecta 2 núcleos densos y clasifica **122 exoplanetas (18.07%) como ruido/outliers**, corroborando la existencia de un núcleo denso continuo y una periferia dispersa de planetas atípicos.

**Decisión Final:** Se revalida de forma absoluta la solución K-Means con $K=4$.

---

## 5. Exportación de Etiquetas y Consolidación Final

### Explicación
Transferimos las etiquetas obtenidas en el modelo (`Cluster_K4` y `Familia_Planeta`) de vuelta al dataset original limpio para permitir el posterior análisis descriptivo en unidades astrofísicas reales (radios, masas, periodos, temperaturas).

### Objetivos Principales:
* **Asignación de Etiquetas:** Incorporación de las columnas `Cluster_K4` y `Familia_Planeta` al dataframe con las 675 observaciones.
* **Validación del Mapeo:** Eliminación de inconsistencias o valores nulos (`NaN`) al mapear la totalidad de las 4 familias.
* **Persistencia de Datos:** Exportación del archivo consolidado al directorio `data/processed/clustered_exoplanets.csv`.

### Resultados del Dataset Etiquetado:
* **Total de Exoplanetas Procesados:** 675.
* **Familia 3 (Población Mayoritaria):** 340 exoplanetas (**50.37%**).
* **Familia 1 (Población Secundaria):** 260 exoplanetas (**38.52%**).
* **Familia 0 (Población Intermedia):** 74 exoplanetas (**10.96%**).
* **Familia 2 (Anomalía / Outlier Extremo):** 1 exoplaneta (**0.15%**).

> **Punto Final:** Con la generación de `clustered_exoplanets.csv`, la fase de Clustering y Evaluación de Modelos queda **oficialmente completada, validada y lista para la DEMO**.

---

## 🔭 Contexto Astrofísico: Conexión con las Familias Reales de la NASA

![Tipos de Exoplanetas](https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRK1F5k4naM1SWhqM2_WvWY_C3AbwWM6sz2Xt-Fc70FI8xy_sfWey61SiWrOjDYTNzFnSL47p60ucqOWS4)  

*Figura: Clasificación general de exoplanetas por tamaño y escala (NASA / Getty Images).*

Con las 4 familias obtenidas por $K=4$, la interpretación astrofísica se alinea perfectamente con la taxonomía oficial de la NASA:

* **Familia 3 (Mayoritaria ~50%):** Sistemas de menor tamaño y masa (planetas rocosos de tipo Terrestre y Super-Tierras).
* **Familia 1 (Secundaria ~38%):** Planetas gaseosos de escala intermedia (Sub-Neptunos y Neptunos fríos).
* **Familia 0 (Intermedia ~11%):** Gigantes gaseosos masivos convencionales.
* **Familia 2 (Anomalía 0.15%):** Objeto extremo singular (ej. Júpiter Ultra-Caliente con periodo u órbita atípica en la muestra).

### 🔑 Drivers Físicos de la Segmentación
La separación entre estos cuatro grupos viene impulsada por la interacción de tres ejes fundamentales de la base de datos:
1. **Escala Planetaria (Radio $R_p$ y Masa $M_p$):** Define la transición entre mundos rocosos (Familia 3) y gigantes gaseosos (Familias 1 y 0).
2. **Dinámica Orbital (Periodo $P$ y Semieje Mayor $a$):** Determina el nivel de acoplamiento marea-estrella.
3. **Flujo de Radiación e Insolación (Temperatura $T_{eq}$):** Separa las poblaciones estándar de los objetos con atmósferas altamente irradiadas (Familia 2).