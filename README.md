# airflow_workshop
Este taller es un ejercicio sobre cómo construir un ETL pipeline usando Apache Airflow,
la idea es extraer información utilizando tres fuentes de datos diferentes (API, archivo csv,
base de datos), a continuación, hacer algunas transformaciones y combinar los datos transformados para finalmente cargar en google drive como un archivo CSV y almacenar los datos en una DB.

## Acerca de los Datos

### Dataset CSV para Leer
- **Spotify Dataset:** El conjunto de datos de Spotify se encuentra disponible en [Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset). Este conjunto de datos contiene información sobre diversas pistas musicales, lo que incluye detalles sobre las canciones, artistas, géneros y características musicales.

### Dataset para Cargar en la Base de Datos Inicial
- **Grammys Dataset:** El conjunto de datos de los Premios Grammy se encuentra disponible en [Kaggle](https://www.kaggle.com/datasets/unanimad/grammy-awards). Este conjunto de datos contiene información sobre los prestigiosos premios musicales, que reconocen logros destacados en la industria de la música.

### Herramientas Utilizadas

- **Sistema de Gestión de Base de Datos:** Se eligió PostgreSQL debido a su familiaridad y capacidades.

- **Visualizaciones:** Se empleó Power BI para crear gráficos impactantes y conectados directamente desde la base de datos PostgreSQL.

- **Orquestación de Tareas:** Apache Airflow se utilizó para la orquestación y programación de tareas en el flujo de trabajo.

- **Almacenamiento de Datos:** La API de Google Drive se integró para el almacenamiento de datos, permitiendo el acceso y respaldo de archivos en Google Drive desde la aplicación.


## Cómo Utilizar
1. **Clonar el Repositorio:** Clona este repositorio en tu máquina local.

2. **Asegurar la Instalación de Python:** Asegúrate de tener Python instalado en tu sistema.

3. **Configuración de la Base de Datos:** Elige una de las siguientes opciones para configurar la base de datos:

   - **Opción 1: Instalar PostgreSQL:** Instala PostgreSQL en tu sistema.

   - **Opción 2: Contenedor Docker (Recomendado):** Despliega un contenedor Docker para la base de datos utilizando la siguiente plantilla de Docker Compose:

     ```yaml
     version: '3.1'

     services:

       db:
         image: postgres:latest
         restart: always
         environment:
           POSTGRES_USER: tu_usuario_de_postgres
           POSTGRES_PASSWORD: tu_contraseña_de_postgres
           POSTGRES_DB: tu_base_de_datos_postgres
         ports:
           - "5432:5432"
     ```
     Guarda esta configuración en un archivo `docker-compose.yml`.

4. **Crear un Entorno Virtual:** Crea un entorno virtual para este proyecto. Puedes hacerlo ejecutando el siguiente comando en tu terminal:

   ```bash
   python -m venv nombre_del_entorno

5. **Activar el Entorno Virtual:**
   - Luego, activa el entorno virtual (los comandos pueden variar según tu sistema operativo):
     - En Windows:

       ```bash
       nombre_del_entorno\Scripts\activate
       ```

     - En macOS y Linux:

       ```bash
       source nombre_del_entorno/bin/activate
       ```

6. **Instalar Dependencias:** Comienza por instalar las dependencias necesarias. Ejecuta el siguiente comando en tu terminal para instalarlas:

   ```bash
   pip install -r requirements.txt
   ```

7. **Configuración de Airflow:**

   Suponiendo que Airflow ya está instalado en la carpeta de tu repositorio, debes configurar el archivo `airflow.cfg`. En la sección `dags_folder`, asegúrate de especificar la ruta de los DAGs. Reemplaza `dags` por `etl_dag` para que se vea de la siguiente manera:

   ```bash
   dags_folder = /root/airflow_workshop/etl_dag
   Nota: Asegúrate de reemplazar `/root` con el nombre de usuario correspondiente.
   ```
   Además, es necesario ejecutar el siguiente comando para definir la variable de entorno AIRFLOW_HOME estando en la raíz del repositorio:

    ```bash
    export AIRFLOW_HOME=$(pwd)
    ```

8. **Configuración:**

    - **Creación del Archivo `db_config.json`:** Dentro de la carpeta `./etl_dag`, crea un archivo llamado `db_config.json` y utiliza la siguiente estructura JSON como plantilla. Asegúrate de reemplazar los marcadores de posición con tus credenciales reales:

      ```json
      {
          "user": "tu_usuario_de_postgres",
          "password": "tu_contraseña_de_postgres",
          "database": "tu_base_de_datos_postgres"
      }
      ```

    - **Creación del Archivo `credentials_module.json`:** Para obtener las credenciales necesarias, sigue las instrucciones de [este video](https://www.youtube.com/watch?v=ZI4XjwbpEwU). Asegúrate de que el archivo `credentials_module.json` también esté ubicado dentro de la carpeta `./etl_dag`.


9. **Obtener e Insertar el Conjunto de Datos:**

   Descarga el conjunto de datos de Spotify desde Kaggle y colócalo en la carpeta `./etl_dag/dataset`. Asegúrate de que el conjunto de datos de los Grammy se encuentre en la base de datos y se inserte en la tabla correspondiente llamada "grammy".

   Nota: Puedes nombrar la tabla de los Grammy como desees. Si decides utilizar un nombre diferente, asegúrate de ajustar la lectura de la tabla correspondiente en el archivo `./etl_dag/db_operations.py`.

10. **Ejecutar el DAG en Airflow:**
  
    Una vez que hayas configurado Airflow y tus DAGs estén en la ubicación correcta, inicia Airflow, utiliza el siguiente comando en la raíz del repositorio:
   
    ```bash
    airflow standalone
    ```
    Luego, inicia sesión en el panel de Airflow y busca el DAG con el nombre "workshop_dag". Ejecuta este DAG para comenzar el proceso ETL y procesar los datos.

    Nota: Asegúrate de que todos los pasos anteriores se hayan completado con éxito antes de ejecutar el DAG en Airflow.


Follow these steps in order to get started and work effectively on your project.