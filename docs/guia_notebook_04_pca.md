# Guía del notebook 04: PCA sobre exoplanetas hasta 2025

## 1. Finalidad

`04_pca_and_cluster_profiling.ipynb` reduce las 12 variables procesadas por el notebook 03 a un número menor de componentes principales.

No realiza clustering. Su salida es el contrato de entrada para el notebook 05.

## 2. Contrato de entrada

El notebook carga:

- `data/processed/exoplanets_preprocessed.csv`;
- `data/processed/preprocessing_metadata.json`;
- `data/raw/exoplanets.csv`, únicamente para verificar años.

Antes de ajustar PCA exige:

```python
EXPECTED_MAX_DISCOVERY_YEAR = 2025
EXPECTED_ROWS = 675
DATA_ALREADY_SCALED = True
VARIANCE_THRESHOLD = 0.85
```

La ejecución se detiene si:

- la metadata no declara el corte en 2025;
- el CSV no contiene 675 filas;
- aparece un planeta de 2026;
- faltan variables;
- existen nulos, infinitos o identificadores duplicados.

## 3. Por qué no se vuelve a escalar

El notebook 03 ya aplica:

1. transformaciones `log1p`;
2. `RobustScaler`;
3. imputación KNN.

PCA utiliza directamente esa matriz. Un segundo escalado cambiaría el peso relativo definido por el preprocessing.

## 4. Selección de componentes

Se ajusta primero un PCA completo y se conserva el número mínimo de componentes que supera el 85 % de varianza acumulada.

| Componente | Varianza individual | Varianza acumulada |
|---|---:|---:|
| PC1 | 44,02 % | 44,02 % |
| PC2 | 30,20 % | 74,22 % |
| PC3 | 9,60 % | 83,81 % |
| PC4 | 6,39 % | **90,20 %** |

Tres componentes no alcanzan el umbral. Por eso el clustering debe usar PC1–PC4.

## 5. Interpretación de los loadings

### PC1: escala orbital

- `pl_orbsmax`: 0,808;
- `pl_orbper`: 0,385;
- `pl_orbeccen`: 0,245.

PC1 resume principalmente la extensión y duración de la órbita.

### PC2: gradiente estelar y térmico

- `st_logg`: 0,451;
- `st_rad`: −0,407;
- `st_mass`: −0,365.

También intervienen `pl_eqt` y `pl_insol`. La componente contrapone gravedad superficial frente a tamaño y masa estelar y condiciones térmicas.

### PC3: excentricidad

- `pl_orbeccen`: 0,945;
- `pl_orbsmax`: −0,259;
- `pl_bmasse`: 0,116.

La forma de la órbita domina esta componente.

### PC4: metalicidad y tamaño planetario

- `st_met`: 0,811;
- `pl_bmasse`: 0,326;
- `pl_rade`: 0,296.

PC4 conserva principalmente información de metalicidad y propiedades físicas del planeta.

El signo global de una componente es arbitrario. La importancia se interpreta mediante la magnitud absoluta del loading.

## 6. Proyecciones

- PC1–PC2 representa el 74,22 % de la varianza.
- PC1–PC3 representa el 83,81 %.
- El espacio final PC1–PC4 representa el 90,20 %.

Las gráficas 2D y 3D ayudan a comunicar, pero no sustituyen las cuatro dimensiones utilizadas por K-Means.

## 7. Validaciones

El notebook confirma:

- 675 observaciones;
- año máximo 2025;
- 12 variables de entrada;
- 4 componentes;
- varianza retenida de 0,901999;
- error medio de reconstrucción de 0,068419;
- ausencia de nulos en scores y loadings.

## 8. Artefactos exportados

En `data/processed/pca/` se generan:

- `pca_scores.csv`: `pl_name`, PC1, PC2, PC3 y PC4;
- `pca_explained_variance.csv`;
- `pca_loadings.csv`;
- `pca_model.joblib`;
- `pca_metadata.json`.

`pca_metadata.json` registra:

- fuente del preprocessing;
- 675 filas;
- año máximo 2025;
- orden de variables;
- umbral de 85 %;
- cuatro componentes;
- varianza retenida.

## 9. Conexión con clustering

El siguiente notebook debe cargar:

```python
pca_scores = pd.read_csv("data/processed/pca/pca_scores.csv")
X_kmeans = pca_scores[["PC1", "PC2", "PC3", "PC4"]]
```

`pl_name` conserva la trazabilidad, pero nunca entra en K-Means.

Al cambiar de 731 a 675 observaciones, las métricas y conclusiones antiguas del notebook 05 dejan de ser válidas hasta que ese notebook se vuelva a ejecutar y documentar.

## 10. Limitaciones

- PCA describe exclusivamente la muestra hasta 2025.
- PCA resume relaciones lineales.
- `pl_insol` hereda incertidumbre de imputación.
- Una separación visual no demuestra por sí sola la existencia de clusters.
- La elección de K debe considerar silhouette, inercia, tamaños, estabilidad e interpretación física.

## 11. Reproducción

1. Ejecutar primero `03_preprocessing.ipynb`.
2. Confirmar 675 filas y el corte 2025 en la metadata.
3. Ejecutar `04_pca_and_cluster_profiling.ipynb`.
4. Confirmar cuatro componentes y 90,20 % de varianza.
5. Revisar loadings y proyecciones.
6. Entregar `pca_scores.csv` al responsable de clustering.
