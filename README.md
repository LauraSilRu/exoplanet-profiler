🌌 ExoProfiler
Descubrimiento inteligente de familias de exoplanetas

ExoProfiler es un proyecto de Machine Learning no supervisado cuyo objetivo es descubrir patrones ocultos y posibles familias de exoplanetas a partir de sus características físicas, orbitales y estelares.

A partir de datos astronómicos reales, el proyecto explorará diferentes técnicas de clustering y reducción de dimensionalidad para identificar agrupaciones naturales entre exoplanetas sin partir de categorías o etiquetas previamente definidas.

🎯 Objetivo del proyecto

La exploración espacial genera grandes cantidades de información sobre planetas situados fuera de nuestro Sistema Solar. Estos mundos presentan características muy diferentes en cuanto a tamaño, masa, temperatura, órbita y entorno estelar.

El objetivo de ExoProfiler es analizar estas características mediante técnicas de aprendizaje no supervisado para:

Descubrir agrupaciones naturales de exoplanetas.
Identificar las características que definen cada grupo.
Visualizar las relaciones existentes entre diferentes tipos de mundos.
Encontrar exoplanetas con características similares.
Detectar planetas inusuales que puedan resultar interesantes para futuras investigaciones.

Los grupos obtenidos mediante los algoritmos serán posteriormente analizados e interpretados para construir diferentes Familias de Mundos basadas en los patrones encontrados en los datos.

🛰️ Problema planteado

Una organización dedicada a la investigación astronómica dispone de información sobre numerosos exoplanetas descubiertos mediante diferentes misiones y métodos de observación.

Sin embargo, analizar manualmente grandes cantidades de objetos astronómicos y encontrar relaciones entre ellos puede resultar complejo.

ExoProfiler propone utilizar Machine Learning no supervisado para descubrir automáticamente estructuras y patrones dentro de estos datos, facilitando su exploración y ayudando a identificar grupos de planetas con características similares.

🧠 Metodología

El proyecto seguirá un flujo de trabajo basado en análisis de datos y Machine Learning:

Comprensión y exploración de los datos
Análisis de las variables disponibles.
Estudio de tipos de datos.
Identificación de valores nulos.
Detección y análisis de valores atípicos.
Estudio de distribuciones y correlaciones.
Preprocesamiento
Selección de variables relevantes.
Tratamiento justificado de valores nulos.
Análisis de posibles outliers.
Transformación de variables cuando sea necesario.
Escalado de características.
Clustering
K-Means.
Exploración de algoritmos basados en densidad como DBSCAN.
Selección y comparación de modelos.
Evaluación
Método del codo.
Coeficiente de Silhouette.
Análisis de estabilidad de los clusters.
Evaluación de la interpretabilidad de los grupos obtenidos.
Reducción de dimensionalidad
Aplicación de PCA (Principal Component Analysis).
Representación visual de los clusters en espacios de menor dimensionalidad.
Perfilado de clusters
Análisis de las características principales de cada agrupación.
Interpretación de los patrones encontrados.
Creación de perfiles o Familias de Mundos.
🚀 Propuesta de producto

Como resultado del análisis se desarrollará un prototipo denominado ExoProfiler, una herramienta interactiva orientada a la exploración de exoplanetas.

La aplicación podrá permitir funcionalidades como:

🌌 Explorar las familias planetarias descubiertas.
🪐 Consultar el perfil de diferentes exoplanetas.
🔎 Encontrar mundos con características similares.
📊 Visualizar las agrupaciones obtenidas mediante Machine Learning.
🔬 Identificar objetos con características especialmente inusuales.

Las funcionalidades definitivas se determinarán a partir de los resultados obtenidos durante el análisis y modelado de los datos.

📂 Estructura del proyecto
exoplanet-profiler/
│
├── data/
│   ├── raw/                    # Datos originales
│   └── processed/              # Datos procesados
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_preprocessing.ipynb
│   ├── 04_clustering.ipynb
│   └── 05_pca_and_cluster_profiling.ipynb
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── clustering.py
│   └── visualization.py
│
├── app/
│   └── app.py
│
├── docs/
│
├── .gitignore
├── README.md
└── requirements.txt
🛠️ Tecnologías

El proyecto utilizará principalmente:

Python
Pandas
NumPy
Matplotlib
Seaborn
Scikit-learn
Jupyter Notebook
Plotly
Streamlit
Git & GitHub
📊 Dataset

El proyecto utiliza datos astronómicos reales sobre exoplanetas descubiertos fuera de nuestro Sistema Solar.

El dataset contiene información relacionada con diferentes características planetarias y estelares, incluyendo variables relacionadas con:

Propiedades orbitales.
Tamaño y masa planetaria.
Temperatura.
Insolación recibida.
Características de la estrella anfitriona.

Durante la fase de exploración de datos se realizará un análisis detallado para seleccionar las variables más relevantes para el proceso de clustering.

La fuente exacta, criterios de selección y descripción detallada del dataset serán documentados una vez finalizada la fase inicial de comprensión de los datos.

🌍 Flujo general del proyecto
Datos astronómicos
        ↓
Comprensión de los datos
        ↓
Análisis exploratorio (EDA)
        ↓
Preprocesamiento
        ↓
Clustering
        ↓
Evaluación y estabilidad
        ↓
PCA y visualización
        ↓
Perfilado de clusters
        ↓
Familias de Mundos
        ↓
ExoProfiler
⚖️ Consideraciones éticas y limitaciones

El proyecto tendrá en cuenta las limitaciones derivadas de los datos disponibles y de los métodos utilizados para descubrir exoplanetas.

Los patrones encontrados por los algoritmos representan estructuras matemáticas presentes en los datos y no deben interpretarse automáticamente como categorías astronómicas oficiales.

También se analizarán posibles sesgos derivados de:

Los métodos utilizados para detectar exoplanetas.
La disponibilidad desigual de determinadas mediciones.
La presencia de valores ausentes.
La sobrerrepresentación de determinados tipos de planetas debido a las técnicas de observación.
👥 Equipo

Proyecto desarrollado por:

Elena
Helen
Jose
Elizabeth
Laura

📌 Estado del proyecto

🚧 Proyecto en desarrollo

Actualmente el proyecto se encuentra en la fase inicial de comprensión y exploración del dataset.

📄 Licencia

Este proyecto ha sido desarrollado con fines educativos y académicos.