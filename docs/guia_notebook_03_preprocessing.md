# Guía del notebook 03: preprocessing de las 12 variables

## 1. Qué hace este notebook

`03_preprocessing.ipynb` transforma el extracto de TESS del NASA Exoplanet Archive en una matriz numérica apta para PCA y clustering. Parte exactamente de las 12 variables candidatas acordadas en `01_data_understanding.ipynb` y `02_eda.ipynb`; no realiza una reducción adicional de variables.

El archivo usado en la validación contiene 910 exoplanetas y 355 columnas. `pl_name` es el identificador: no tiene nulos ni duplicados y nunca se utiliza como variable del modelo.

## 2. Variables conservadas

### Variables planetarias

| Variable | Significado |
|---|---|
| `pl_orbper` | Periodo orbital en días. |
| `pl_orbsmax` | Semieje mayor orbital en unidades astronómicas. |
| `pl_rade` | Radio planetario en radios terrestres. |
| `pl_bmasse` | Masa planetaria en masas terrestres. |
| `pl_orbeccen` | Excentricidad orbital, acotada entre 0 y 1. |
| `pl_insol` | Flujo de insolación recibido, relativo a la Tierra. |
| `pl_eqt` | Temperatura de equilibrio planetaria en kelvin. |

### Variables estelares

| Variable | Significado |
|---|---|
| `st_teff` | Temperatura efectiva de la estrella en kelvin. |
| `st_rad` | Radio estelar en radios solares. |
| `st_mass` | Masa estelar en masas solares. |
| `st_met` | Metalicidad estelar. |
| `st_logg` | Logaritmo de la gravedad superficial estelar. |

Aunque existen correlaciones fuertes, se mantienen las 12 porque son las candidatas definidas por el EDA y PCA está diseñado para resumir redundancia. El clustering deberá recibir las componentes PCA, no las 12 columnas crudas.

## 3. Controles de calidad iniciales

El notebook comprueba:

- que están presentes `pl_name`, las 12 variables y `disc_year`;
- que las variables pueden convertirse a formato numérico;
- que no hay identificadores nulos o repetidos;
- que periodo, semieje, radio, masa, insolación, temperatura y parámetros estelares positivos respetan su dominio;
- que `pl_orbeccen` se encuentra entre 0 y 1.

En el extracto validado no apareció ninguna violación de esos rangos físicos.

## 4. Ausencia de datos

| Variable | % de nulos inicial |
|---|---:|
| `pl_insol` | 57,58 % |
| `pl_bmasse` | 31,76 % |
| `pl_orbeccen` | 31,32 % |
| `pl_eqt` | 26,26 % |
| `st_met` | 24,51 % |
| `pl_orbsmax` | 22,53 % |
| `st_mass` | 13,30 % |
| `st_logg` | 9,56 % |
| `st_teff` | 2,53 % |
| `pl_rade` | 1,21 % |
| `st_rad` | 0,33 % |
| `pl_orbper` | 0,11 % |

No se eliminan columnas por ausencia, porque el requisito es conservar las 12 candidatas. Tampoco se imputan filas casi vacías.

### Filtro de completitud

Se exige que cada planeta tenga al menos 8 de las 12 variables observadas. Así, como máximo se imputan cuatro valores por fila.

- Filas originales: 910.
- Filas retenidas: 733 (80,55 %).
- Filas excluidas: 177.
- Casos completos: 249.
- Celdas que se imputan dentro de la muestra retenida: 9,99 %.

El archivo `preprocessing_row_audit.csv` conserva la decisión por planeta para que la exclusión sea auditable.

### Riesgo que debe explicarse

Incluso tras el filtro, `pl_insol` falta en 379 de 733 filas (51,71 %). Se conserva por decisión del proyecto, pero cualquier interpretación de esta variable debe hacerse con cautela.

Además, la retención para descubrimientos de 2026 es 33,92 %, muy inferior a otros años. Probablemente son registros recientes todavía incompletos. Esto introduce un posible sesgo temporal hacia planetas con mediciones más consolidadas.

## 5. Outliers

El rango intercuartílico se usa como auditoría descriptiva, no como regla automática de borrado. En astronomía, un valor extremo puede ser un objeto real e interesante.

No se eliminan filas, no se winsoriza y no se recortan valores. En su lugar se aplican transformaciones y escalado robusto para reducir su influencia sin destruir información.

## 6. Transformaciones

Se aplica `log1p(x) = log(1 + x)` a variables positivas y muy asimétricas:

- `pl_orbper`
- `pl_orbsmax`
- `pl_rade`
- `pl_bmasse`
- `pl_insol`
- `st_rad`

No se transforma `pl_orbeccen` porque está acotada entre 0 y 1. Tampoco se transforma `st_logg`, porque ya representa una magnitud logarítmica. Las demás variables permanecen en su escala funcional antes del escalado.

## 7. Escalado e imputación

El orden del pipeline es:

1. transformaciones `log1p` por columna;
2. `RobustScaler`;
3. `KNNImputer(n_neighbors=5, weights="distance")`.

El escalado debe ocurrir antes de KNN porque KNN calcula distancias: sin escalado, las unidades de mayor rango dominarían. `RobustScaler` usa mediana y rango intercuartílico, por lo que es más resistente a extremos que un escalado basado en media y desviación típica.

### Por qué se eligió KNN

La decisión se probó usando los 249 casos completos. Se ocultó aleatoriamente el 10 % de sus valores, con semilla 42, y se comparó la reconstrucción en el espacio transformado y escalado:

| Método | RMSE | MAE |
|---|---:|---:|
| Mediana | 0,7168 | 0,5651 |
| KNN, 5 vecinos y pesos por distancia | 0,4026 | 0,2422 |

KNN obtuvo menor error en ambas métricas. La comparación no elimina toda incertidumbre —especialmente en `pl_insol`—, pero aporta una justificación reproducible.

## 8. Resultado y artefactos

El resultado principal es `data/processed/exoplanets_preprocessed.csv`, con:

- 733 filas;
- `pl_name` más las 12 variables, en el orden acordado;
- cero nulos;
- cero infinitos;
- cero identificadores duplicados.

También se generan:

- `exoplanets_selected_raw.csv`: valores originales de las filas retenidas;
- `preprocessing_row_audit.csv`: auditoría de inclusión por planeta;
- `preprocessing_quality_summary.csv`: resumen de calidad;
- `preprocessing_scaler_comparison.csv`: comparación descriptiva de scalers;
- `preprocessing_imputer_comparison.csv`: prueba mediana frente a KNN;
- `preprocessing_pipeline.joblib`: pipeline ajustado y reutilizable;
- `preprocessing_metadata.json`: variables, orden, reglas y parámetros.

## 9. Conexión con el notebook 04

El notebook PCA carga directamente `exoplanets_preprocessed.csv`, valida las 12 columnas y no vuelve a escalar. El orden de `FEATURE_COLUMNS` debe coincidir exactamente con el metadata y con el pipeline.

Para datos nuevos se debe cargar `preprocessing_pipeline.joblib`; no se deben recalcular transformaciones, vecinos o escalas con una sola observación.

## 10. resumen de decisiones

> Conservamos las 12 variables candidatas seleccionadas en el EDA. Para no imputar perfiles casi vacíos exigimos al menos 8 mediciones por planeta, lo que conserva 733 objetos. Aplicamos log1p a las variables positivas más sesgadas, RobustScaler para limitar la influencia de extremos y KNN con cinco vecinos. KNN se eligió porque reconstruyó mejor valores ocultados que la mediana. No borramos outliers físicos y documentamos como limitaciones la alta imputación de insolación y el sesgo de completitud de 2026.

## 11. Reproducción

1. Colocar el CSV en `data/raw/exoplanets.csv`.
2. Ejecutar `03_preprocessing.ipynb` desde la primera hasta la última celda.
3. Revisar que finalice con 12 variables, cero nulos y cero infinitos.
4. Confirmar los artefactos en `data/processed/`.
5. Ejecutar después `04_pca_and_cluster_profiling.ipynb`.

Si NASA actualiza la tabla, las cifras pueden cambiar y deben volver a calcularse; las reglas del pipeline seguirán siendo reproducibles.
