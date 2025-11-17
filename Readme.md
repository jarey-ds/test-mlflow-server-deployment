# Validación de servidor MLflow

Este repositorio contiene dos scripts de utilidad con el objetivo de testear el correcto comportamiento de un servidor MLflow.

## Contextualización

El servidor MLFlow cuyo despliegue se pretende validar posee la siguiente configuración:
- backend storage: Postgresql
- artifact storage: filesystem local al servidor

Los scripts proporcionados son agnósticos de esta configuración y son válidos para cualquier cambio de configuración en la misma del lado del servidor.

## Aproximación

- src/mlflow_test_experiment_creation.py: Como su nombre indica realiza la validación de la creación de un nuevo experimento en el servidor MLFlow.
- src/mlflow_test_model_storage: Realiza la validación de la ejecución de un "run" y tras su ejecución, realiza el guardado del modelo generado como un artefacto en el registro de modelos del servidor MLFlow.

## Uso
### 1 - Instalación de requisitos y variables de entorno
Instalación de requerimientos python

`pip install -r setup/requirements.txt`

Exportación de variables de entorno apuntando al servidor MLflow deseado:

`export MLFLOW_TRACKING_URI=http://178.60.252.123:4020`

`export MLFLOW_S3_ENDPOINT_URL=http://178.60.252.123:4021`

`export AWS_ACCESS_KEY_ID=admin`

`export AWS_SECRET_ACCESS_KEY=sample_key`

`export AWS_REGION=us-east-1`

`export AWS_BUCKET_NAME=mlflow`

Nota: Se recomienda el uso de un entorno virutal para la instalación de este set de requerimientos (conda, venv etc)

### 2 - Ejecución de script de creación de experimento
`python src/mlflow_test_expriment_creation.py -experiment-name "Nombre de mi experimento único"`

El script proporcionará por salida standard el identificador del experimento creado, a emplear en el script del paso 3.

Nota: el parámetro -experiment-name es un string que debe ir entrecomillado si incluye espacios, y es opcional. 
De no proporcionarse el sscript tratará de componer un nombre único empleando para ello la generación de un número pseudoaleatorio.

Nótese que de no proporcionarse un nombre único, la aproximación pseudoaleatoria no garantiza la generación de un nombre no usado previamente en el servidor,
en caso de obtener una excepción por nombre ya existente, volver a ejecutar el script o proporcuionar un nombre único (los nombres de experimentos aparecen listados en la sección "Experiments" de la UI Mlflow.)


#### 2.1 - Ejemplo de ejecución

##### input
`python src/mlflow_test_experiment_creation.py -experiment-name "Creación experimento Dataspartan"`
##### output
`Experimento creado correctamente con el id: 7

#### 3 - Ejecución de script de generación y registro de modelo
`python src/mlflow_test_model_storage.py -experiment-id ID`

El parámetro ID es un argumento obligatorio, que debe corresponderse con el de un experimento previamente creado por medio del script del paso 2
(o tomarse desde el listado de experimentos válidos por medio de la UI MLflow del servidor)

La ejecución de este script creará un modelo ML por medio de scikit-learn que registrará en el almacenamiento de modelos del servidor MlFlow.
Dicho modelo será consultable por medio de la pestaña "Models" de la MLFlow UI del servidor.

#### 3.1 - Ejemplo de ejecución
##### input
`python src/mlflow_test_model_storage.py -experiment-id 7`
##### output
`Registered model 'sk-learn-random-forest-reg-model' already exists. Creating a new version of this model...
2022/11/11 12:54:11 INFO mlflow.tracking._model_registry.client: Waiting up to 300 seconds for model version to finish creation.                     Model name: sk-learn-random-forest-reg-model, version 10
Created version '10' of model 'sk-learn-random-forest-reg-model'.
`

## Consideraciones

El usuario necesita permisos de escritura sobre el directorio de ejecución de los scripts ya que se creará una carpeta con el nombre "mlruns" en su interior,
de acuerdo a lo especificado en el script del punto 2 (ver su contenido), este comportamiento puede cambiarse a voluntad del programador/usuario.