# Guía Técnica: Notebook 05 - Clustering & Model Evaluation
**Proyecto:** Exoplanet Profiler  
**Módulo:** Unsupervised Clustering & Model Evaluation  
**Fase:** Selección y Validación de Modelos  

---

## 📌 Estado de Avance del Notebook

| Bloque | Descripción | Estado | Resultado Clave / Selección |
| :--- | :--- | :---: | :--- |
| **1. Carga y Contrato** | Verificación de datos cargados desde PCA | ✅ Completado | $731 \times 4$ variables (`PC1` a `PC4`), 90.35% varianza conservada. |
| **2. Evaluación de K** | Métricas del Codo (Inercia) y Silhouette ($K \in [2, 10]$) | ✅ Completado | **$K = 2$ seleccionado** (Silhouette máximo: **0.4950**). |
| **3. Modelo Final** | Entrenamiento $K=2$ y prueba de estabilidad | ✅ Completado | **99.04% - 100.00%** de coincidencia multisemilla. |
| **4. Métodos Alternativos** | Evaluación opcional (DBSCAN / Jerárquico) | ✅ Completado | Jerárquico: **97.13%** de coincidencia. DBSCAN confirma outliers. |
| **5. Exportación** | Guardado de labels y DataFrame consolidado | ✅ Completado | Exportado a `data/processed/clustered_exoplanets.csv`. |

---

## 📊 Resumen Detallado de Bloques Ejecutados

### 🔹 Bloque 1: Carga de Datos y Verificación del Contrato
* **Objetivo:** Cargar el set de datos transformado por PCA (`pca_scores.csv`) y validar la integridad de la matriz de características.
* **Resultados Obtenidos:**
  * **Observaciones:** 731 exoplanetas.
  * **Dimensiones:** 4 Componentes Principales (`PC1`–`PC4`).
  * **Trazabilidad:** Separación exitosa entre identificadores (`pl_name`) y matriz de trabajo $X$.

---

### 🔹 Bloque 2: Evaluación de K-Means y Búsqueda del $K$ Óptimo
* **Objetivo:** Determinar la cantidad óptima de familias planetarias ($K$) utilizando el Método del Codo (Inercia/WCSS) y el Coeficiente de Silhouette.
* **Nota Metodológica:** La evaluación parte desde $K = 2$ dado que el Coeficiente de Silhouette requiere comparar la distancia intra-cluster con la de un grupo vecino; para $K = 1$ la métrica no está matemáticamente definida.
* **Métricas Clave Obtenidas:**
  * $K = 2$: Inercia = **4023.36** | Silhouette = **0.4950** ⭐ *(Óptimo Matemático)*
  * $K = 3$: Inercia = **2820.81** | Silhouette = **0.3223**
  * $K = 4$: Inercia = **2392.98** | Silhouette = **0.3238**
  * $K \ge 5$: Silhouette cae por debajo de 0.28.
* **Conclusión:** Seleccionamos **$K = 2$** como la estructura primaria de segmentación exoplanetaria, respaldada por el pico claro de la métrica de Silhouette.

---

### 🔹 Bloque 3: Modelo Final (K=2) y Evaluación de Estabilidad
* **Objetivo:** Entrenar el modelo definitivo de K-Means con $K = 2$ y verificar la robustez de los clusters mediante perturbación de semillas (`random_state`).
* **Resultados del Modelo Final:**
  * **Inercia (WCSS):** 4023.36
  * **Coeficiente de Silhouette:** 0.4950
* **Estructura de las Familias Planetarias:**
  * **Cluster 0 (Población Estándar):** 667 exoplanetas (**91.24%**). Representa la categoría generalista mayoritaria.
  * **Cluster 1 (Grupo Exótico / Atípico):** 64 exoplanetas (**8.76%**). Representa objetos con propiedades físicas u orbitales extremas.

                          ┌───────────────────────────┐
                          │      731 EXOPLANETAS      │
                          └─────────────┬─────────────┘
                                        │
                        ┌───────────────┴─────────────────┐
                        ▼                                 ▼
                  ┌─────────────────┐             ┌─────────────────┐
                  │    CLUSTER 0    │             │    CLUSTER 1    │
                  │  667 planetas   │             │   64 planetas   │
                  │    (91.24%)     │             │     (8.76%)     │
                  └────────┬────────┘             └────────┬────────┘
                           │                               │
                           ▼                               ▼
                "La Regla / Estándar"           "Los Exóticos / Extremos"

* **Prueba de Estabilidad (Variando `random_state` $\in [10, 100, 2026, 9999]$):**
  * Semillas 10, 2026 y 9999: **100.00%** de coincidencia en la asignación de clusters.
  * Semilla 100: **99.04%** de coincidencia (Inercia: 4025.21, Silhouette: 0.4796).
* **Conclusión:** La solución de $K = 2$ es altamente estable, reproducible y libre de sesgo por inicialización de centroides.

---

## 4. Métodos de Clustering Alternativos (DBSCAN y Jerárquico)

### Explicación
Para validar la robustez de la segmentación obtenida con K-Means ($K=2$), probamos otros dos algoritmos con fundamentos matemáticos distintos para comprobar si descubren la misma estructura subyacente en los datos:

1. **DBSCAN (Basado en Densidad):** Agrupa observaciones que están muy cerca unas de otras en zonas de alta densidad. Si un dato está aislado y no tiene suficientes vecinos cerca, no lo fuerza dentro de un grupo, sino que lo identifica como ruido o valor atípico (`label = -1`).
2. **Clustering Jerárquico (Aglomerativo):** Agrupa los planetas desde abajo hacia arriba (de individual a general) construyendo una estructura en árbol (*dendrograma*). Nos ayuda a ver de forma intuitiva cómo se van fusionando los grupos paso a paso.

* **Conclusión (Validación Cruzada):**

  * **Clustering Jerárquico:** Coincide casi al 100% (**97.13%**) con los resultados de K-Means. Su gráfico (*dendrograma*) muestra de forma evidente que la masa de datos se divide de forma natural en dos grandes ramas principales desde la parte superior.
  * **DBSCAN:** Confirma que la inmensa mayoría de los exoplanetas están muy concentrados en un grupo común, mientras que identifica a la minoría (~60 planetas) como observaciones aisladas o atípicas (*outliers*).

* **Decisión Final:** Mantenemos la segmentación en **2 grupos ($K=2$) con K-Means**, habiendo demostrado por múltiples vías que es la estructura más real, estable e interpretable.

## 5. Exportación de Etiquetas y Consolidación Final

### Explicación
El último bloque del notebook tiene como objetivo la **transferencia de resultados del espacio del modelo al espacio de los datos originales**. Una vez validado y seleccionado el algoritmo K-Means ($K=2$), asignamos la etiqueta correspondiente a cada registro del conjunto de datos limpio para permitir la interpretación de las propiedades físicas de los exoplanetas en sus unidades originales.

---

### Objetivos Principales:
1. **Asignación de Etiquetas:** Creación de las columnas `Cluster_K2` (numérica) y `Familia_Planeta` (descriptiva) para categorizar de forma intuitiva los dos grupos identificados.
2. **Validación de la Distribución:** Inspección del balance final entre la población generalista y la población atípica/exótica.
3. **Persistencia de Datos:** Exportación del dataset etiquetado al directorio `data/processed/` bajo el nombre `clustered_exoplanets.csv`.

---

### Resultados del Dataset Etiquetado:
* **Población Total Procesada:** 731 exoplanetas.
* **Familia 0 (Población Estándar):** 667 exoplanetas (**91.25%**).
* **Familia 1 (Población Exótica / Atípica):** 64 exoplanetas (**8.75%**).

---

> **Punto Final:** Con la generación de `clustered_exoplanets.csv`, el pipeline de machine learning para la fase de Clustering queda oficialmente **cerrado, validado y documentado**.

---

## 🔭 Contexto Astrofísico: Conexión con las Familias Reales de la NASA

![Tipos de Exoplanetas](https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRK1F5k4naM1SWhqM2_WvWY_C3AbwWM6sz2Xt-Fc70FI8xy_sfWey61SiWrOjDYTNzFnSL47p60ucqOWS4)
*Figura: Clasificación general de exoplanetas por tamaño y escala (NASA / Getty Images).*

Para facilitar la interpretación física de los clusters obtenidos, relacionamos las etiquetas del modelo con las cuatro categorías planetarias reconocidas por la NASA:

1. **Terrestres & Super-Tierras:** Planetas rocosos de radio pequeño a medio ($< 2 R_\oplus$).
2. **Sub-Neptunos:** Planetas gaseosos de tamaño intermedio ($2 - 4 R_\oplus$).
3. **Gigantes Gaseosos (incl. Júpiters Calientes):** Planetas masivos ($> 4 R_\oplus$).

### Interpretación Astrofísica de la Segmentación:
* **Familia 0 (Población Estándar ~91%):** Captura el continuo de planetas rocosos, Super-Tierras y Sub-Neptunos. Constituyen la regla general de la muestra TESS.
* **Familia 1 (Población Exótica ~9%):** Aísla la cola de la distribución formada por Gigantes Gaseosos masivos y Júpiters Calientes de parámetros orbitales extremos.