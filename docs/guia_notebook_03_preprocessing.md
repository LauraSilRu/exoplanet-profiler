# Guía del notebook 03: preprocessing con corte temporal hasta 2025

## 1. Finalidad

`03_preprocessing.ipynb` convierte el catálogo TESS del NASA Exoplanet Archive en una matriz numérica apta para PCA y clustering.

El notebook conserva las 12 variables definidas en los notebooks 01 y 02, pero aplica una regla temporal previa:

```python
MAX_DISCOVERY_YEAR = 2025
disc_year <= MAX_DISCOVERY_YEAR
```

Los descubrimientos de 2026 quedan fuera antes de ajustar transformaciones, escalado o imputación. De esta forma no influyen indirectamente en el pipeline.

## 2. Resultado principal

| Etapa | Planetas |
|---|---:|
| Catálogo original | 910 |
| Excluidos por pertenecer a 2026 | 171 |
| Elegibles hasta 2025 | 739 |
| Excluidos por tener menos de 8 mediciones | 64 |
| Procesados finalmente | **675** |

La salida final contiene 675 planetas, 12 variables, cero nulos, cero infinitos y cero identificadores duplicados.

## 3. Variables utilizadas

### Planetarias

| Variable | Significado |
|---|---|
| `pl_orbper` | Periodo orbital en días. |
| `pl_orbsmax` | Semieje mayor en unidades astronómicas. |
| `pl_rade` | Radio en radios terrestres. |
| `pl_bmasse` | Masa en masas terrestres. |
| `pl_orbeccen` | Excentricidad orbital. |
| `pl_insol` | Insolación relativa a la Tierra. |
| `pl_eqt` | Temperatura de equilibrio en kelvin. |

### Estelares

| Variable | Significado |
|---|---|
| `st_teff` | Temperatura efectiva estelar. |
| `st_rad` | Radio estelar. |
| `st_mass` | Masa estelar. |
| `st_met` | Metalicidad. |
| `st_logg` | Gravedad superficial logarítmica. |

`pl_name` y `disc_year` mantienen trazabilidad, pero no son variables del modelo.

## 4. Orden de las decisiones

El orden es importante:

1. Cargar y validar las 910 filas.
2. Convertir años y variables a valores numéricos.
3. Aplicar `disc_year <= 2025`.
4. Medir completitud en las 739 filas elegibles.
5. Exigir al menos 8 de las 12 mediciones.
6. Ajustar transformaciones, scaler e imputador únicamente con las 675 filas retenidas.
7. Exportar datos y auditorías.

Filtrar antes del pipeline evita que estadísticas o vecinos de 2026 intervengan en el procesamiento.

## 5. Controles estructurales y físicos

El notebook comprueba:

- presencia de `pl_name`, `disc_year` y las 12 variables;
- identificadores únicos y no nulos;
- años no nulos;
- ausencia de filas exactamente duplicadas;
- conversión numérica sin introducir nulos;
- positividad de las magnitudes físicas que lo requieren;
- excentricidad entre 0 y 1.

El catálogo actual no presenta violaciones de estas reglas.

## 6. Valores ausentes

La ausencia se calcula después de excluir 2026.

| Variable | Nulos antes del filtro de completitud | % | Nulos en los 675 retenidos | % |
|---|---:|---:|---:|---:|
| `pl_insol` | 374 | 50,61 % | 342 | 50,67 % |
| `pl_bmasse` | 167 | 22,60 % | 112 | 16,59 % |
| `pl_orbeccen` | 160 | 21,65 % | 108 | 16,00 % |
| `pl_eqt` | 122 | 16,51 % | 78 | 11,56 % |
| `pl_orbsmax` | 89 | 12,04 % | 64 | 9,48 % |
| `st_met` | 109 | 14,75 % | 51 | 7,56 % |

`pl_insol` sigue siendo la variable con mayor incertidumbre. Una interpretación sobre habitabilidad no debería depender únicamente de esta columna.

## 7. Filtro de completitud

Cada planeta debe aportar al menos 8 variables observadas. Así se imputan como máximo cuatro de las doce características.

- Elegibles hasta 2025: 739.
- Casos completos: 233.
- Excluidos por completitud: 64.
- Retenidos: 675.
- Celdas a imputar dentro de la muestra retenida: aproximadamente 10 %.

`preprocessing_row_audit.csv` contiene una fila para cada uno de los 910 planetas y distingue:

- `retenido`;
- `menos_de_8_mediciones`;
- `fuera_corte_temporal_2026`.

## 8. Outliers y transformaciones

Los outliers se describen mediante IQR, pero no se eliminan ni winsorizan. En astronomía pueden representar objetos reales de interés.

Se aplica `log1p` a:

- `pl_orbper`;
- `pl_orbsmax`;
- `pl_rade`;
- `pl_bmasse`;
- `pl_insol`;
- `st_rad`.

Después se aplica `RobustScaler`, coherente con la decisión de preservar observaciones extremas.

## 9. Imputación

El pipeline final usa:

```python
KNNImputer(n_neighbors=5, weights="distance")
```

La comparación se realiza ocultando de forma reproducible el 10 % de los valores de los 233 casos completos.

| Método | RMSE | MAE |
|---|---:|---:|
| Mediana | 0,7829 | 0,5918 |
| KNN, 5 vecinos | **0,4718** | **0,2613** |

KNN obtiene menor error y se mantiene como imputador.

## 10. Artefactos exportados

En `data/processed/` se generan:

- `exoplanets_preprocessed.csv`: salida principal para PCA;
- `exoplanets_selected_raw.csv`: las mismas 675 filas en unidades originales;
- `preprocessing_row_audit.csv`: trazabilidad de las 910 decisiones;
- `preprocessing_quality_summary.csv`;
- `preprocessing_scaler_comparison.csv`;
- `preprocessing_imputer_comparison.csv`;
- `preprocessing_pipeline.joblib`;
- `preprocessing_metadata.json`.

La metadata registra el corte temporal, los recuentos y todos los parámetros.

## 11. Limitaciones

- El análisis no representa descubrimientos de 2026.
- La alta imputación de `pl_insol` introduce incertidumbre.
- KNN puede suavizar observaciones excepcionales.
- Los resultados dependen de la versión local del catálogo.
- El pipeline debe volver a entrenarse si se cambia el año máximo.

## 12. Reproducción

1. Colocar el catálogo en `data/raw/exoplanets.csv`.
2. Ejecutar `03_preprocessing.ipynb` de principio a fin.
3. Confirmar 675 filas y año máximo 2025.
4. Confirmar cero nulos e infinitos.
5. Revisar `preprocessing_row_audit.csv`.
6. Ejecutar después `04_pca_and_cluster_profiling.ipynb`.
