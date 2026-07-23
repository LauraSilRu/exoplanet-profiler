# 📊 Guía del notebook 05: Clustering & Model Evaluation

## 🎯 Objetivo
Agrupar los exoplanetas transformados tras la reducción de dimensionalidad (PCA) en "Familias Planetarias" coherentes utilizando algoritmos de aprendizaje no supervisado (K-Means y validación con DBSCAN/Jerárquico), evaluando su calidad matemática y estabilidad.

---

## 🗂️ Índice de Pasos

1. **Carga e Inspección de Datos Transformados**:
   - Importación de datos procesados tras la reducción de dimensionalidad con PCA (p. ej. `X_pca`).
2. **Entrenamiento de K-Means y Métricas de Evaluación**:
   - Iteración de K-Means para un rango de $K \in [2, 10]$.
   - Cálculo del Método del Codo (Inercia / WCSS).
   - Cálculo del Coeficiente de Silhouette promedio.
3. **Selección del $K$ Óptimo e Interpretación**:
   - Visualización combinada (Codo + Silhouette) y elección justificada del número de clusters.
   - Generación de las etiquetas definitivas de los clusters.
4. **Pruebas de Estabilidad y Robustez**:
   - Evaluación de la consistencia de los clusters frente a distintas semillas aleatorias (`random_state`).
   - Prueba de subsampling (evaluación con el 90% de los datos).
5. **Modelos Secundarios / Validación Comparativa (Opcional)**:
   - Exploración alternativa con DBSCAN o Clustering Jerárquico.
6. **Exportación de Artefactos**:
   - Guardado del modelo definitivo (`kmeans_model.pkl`) y exportación del DataFrame etiquetado para la DEMO y la narrativa del PO.