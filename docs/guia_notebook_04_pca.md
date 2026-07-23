# Guía del notebook 04: PCA con las 12 variables

## 1. Finalidad

`04_pca_and_cluster_profiling.ipynb` reduce las 12 variables del preprocessing a un conjunto más pequeño de componentes principales. Su salida se entrega a la compañera responsable de K-Means; este notebook no ajusta ni evalúa K-Means.

PCA permite resumir variables correlacionadas sin descartar manualmente ninguna de las candidatas acordadas en los notebooks 01 y 02.

## 2. Contrato de entrada

El notebook carga `data/processed/exoplanets_preprocessed.csv`, que debe contener:

- una fila por exoplaneta;
- `pl_name` único y sin nulos;
- las 12 variables numéricas;
- cero nulos y cero infinitos;
- las transformaciones, el escalado y la imputación ya realizados por el notebook 03.

La configuración utilizada es:

```python
USE_DEMO_DATA = False
PROCESSED_DATA_PATH = Path("data/processed/exoplanets_preprocessed.csv")

FEATURE_COLUMNS = [
    "pl_orbper",
    "pl_orbsmax",
    "pl_rade",
    "pl_bmasse",
    "pl_orbeccen",
    "pl_insol",
    "pl_eqt",
    "st_teff",
    "st_rad",
    "st_mass",
    "st_met",
    "st_logg",
]

DATA_ALREADY_SCALED = True
VARIANCE_THRESHOLD = 0.85
```

`pl_name` solo identifica filas y no entra en PCA. Como el notebook 03 ya aplicó `RobustScaler`, PCA no debe volver a escalar.

## 3. Qué es PCA

PCA crea nuevas variables llamadas componentes principales:

- cada componente es una combinación lineal de las 12 variables;
- PC1 explica la mayor variación posible;
- PC2 explica la mayor parte restante y es perpendicular a PC1;
- las componentes posteriores siguen la misma lógica;
- la suma de varianza explicada permite decidir cuántas conservar.

PCA es una técnica no supervisada: no conoce clusters ni clases. Reduce dimensionalidad, pero no decide por sí sola cuántos grupos existen.

## 4. Selección del número de componentes

Primero se ajusta PCA con las 12 componentes posibles. Después se elige el menor número cuya varianza acumulada alcanza el 85 %.

| Componente | Varianza individual | Varianza acumulada |
|---|---:|---:|
| PC1 | 44,65 % | 44,65 % |
| PC2 | 29,56 % | 74,21 % |
| PC3 | 9,41 % | 83,62 % |
| PC4 | 6,74 % | 90,35 % |

Tres componentes no alcanzan el umbral: se quedan en 83,62 %. Por eso se conservan cuatro, con 90,35 % de la varianza total.

La gráfica de varianza por componente es un *scree plot* de PCA y únicamente justifica cuántas componentes se conservan.

## 5. Interpretación de loadings

Los *loadings* indican cuánto contribuye cada variable a cada componente. Se interpretan por su magnitud absoluta y por las relaciones de signos.

### PC1: dimensión orbital

Mayores contribuciones:

- `pl_orbsmax`: 0,810;
- `pl_orbper`: 0,386;
- `pl_orbeccen`: 0,219.

PC1 resume principalmente el tamaño y periodo de la órbita.

### PC2: gradiente estelar y térmico

Mayores contribuciones absolutas:

- `st_logg`: 0,442;
- `st_rad`: -0,405;
- `pl_eqt`: -0,369.

También contribuye `st_mass` con -0,362. La componente contrapone gravedad superficial frente a radio, masa y condiciones térmicas.

### PC3: excentricidad

Mayores contribuciones:

- `pl_orbeccen`: 0,941;
- `pl_orbsmax`: -0,240;
- `pl_bmasse`: 0,152.

La excentricidad domina claramente esta dimensión.

### PC4: metalicidad y propiedades planetarias

Mayores contribuciones:

- `st_met`: 0,830;
- `pl_bmasse`: 0,292;
- `pl_rade`: 0,265.

Esta componente conserva sobre todo la información de metalicidad que no había quedado resumida en las tres primeras.

El signo global de una componente es arbitrario: todos sus signos podrían invertirse y la solución matemática sería equivalente. Por eso no debe interpretarse un signo aislado como “bueno”, “malo”, “alto” o “bajo” sin observar el resto.

## 6. Proyecciones 2D y 3D

La gráfica PC1-PC2 muestra el 74,21 % de la variación y resulta útil para ver la estructura general. La gráfica 3D añade PC3 y alcanza el 83,62 %.

Ninguna de las dos sustituye el espacio de cuatro componentes que debe recibir K-Means. La cuarta componente no aparece en la proyección 3D, pero sí forma parte del archivo entregado para clustering.

Cuando exista `data/processed/cluster_labels.csv` con `pl_name` y `cluster`, el notebook podrá unir las etiquetas y colorear las proyecciones. La unión se hace por identificador, no por posición de fila.

## 7. Validaciones

Antes de ajustar PCA, el notebook verifica:

- que existen las 12 columnas en el orden previsto;
- que son numéricas;
- que no contienen nulos ni infinitos;
- que `pl_name` no tiene duplicados;
- que no hay variables constantes.

Después comprueba que los scores no tienen nulos, que las dimensiones son coherentes y que la varianza retenida alcanza el umbral. Con los datos actuales procesa 733 observaciones, 12 variables y 4 componentes; el error medio de reconstrucción es 0,066834.

## 8. Artefactos exportados

En `data/processed/pca/` se generan:

- `pca_scores.csv`: `pl_name`, PC1, PC2, PC3 y PC4;
- `pca_explained_variance.csv`: varianza individual y acumulada;
- `pca_loadings.csv`: contribución de cada variable;
- `pca_model.joblib`: modelo PCA ajustado;
- `pca_metadata.json`: contrato y parámetros.

La compañera de K-Means debe usar las cuatro columnas PC1-PC4 de `pca_scores.csv`. Para transformar nuevos datos, primero se aplica el pipeline del notebook 03 y luego `pca_model.joblib`, siempre respetando el orden de las 12 variables.

## 9. Limitaciones

- PCA es sensible a la muestra y a las decisiones previas de transformación.
- `pl_insol` contiene mucha imputación y debe interpretarse con prudencia.
- El filtro de completitud retiene pocos descubrimientos de 2026, por lo que existe posible sesgo temporal.
- La imputación KNN puede suavizar casos raros.
- Un gráfico visualmente separado no demuestra por sí solo que existan clusters válidos.

## 10. Resumen de decisiones.

> Partimos de las 12 variables candidatas ya preprocesadas. PCA resume sus correlaciones y, con un umbral del 85 %, necesita cuatro componentes que conservan el 90,35 % de la varianza. Las dos primeras describen sobre todo órbita y un gradiente estelar-térmico; la tercera conserva la excentricidad y la cuarta la metalicidad. Entregamos las cuatro componentes a K-Means y usamos las proyecciones 2D y 3D solo para visualizar.

## 11. Orden de ejecución

1. Ejecutar `03_preprocessing.ipynb` completo.
2. Comprobar que existe `exoplanets_preprocessed.csv` con 733 filas y 12 variables.
3. Ejecutar `04_pca_and_cluster_profiling.ipynb` completo.
4. Revisar la tabla de varianza y los loadings.
5. Entregar `pca_scores.csv` y el resto de artefactos a la responsable de K-Means.
