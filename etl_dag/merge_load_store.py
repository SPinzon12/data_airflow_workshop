import pandas as pd
import json
import logging
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError
import db_operations

# Configuración de registros (logs)
logging.basicConfig(level=logging.INFO)

credentials_directory = './etl_dag/credentials_module.json'

def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = credentials_directory
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credentials_directory)
    
    if gauth.credentials is None:
        logging.info("Iniciando autenticación local en el servidor web...")
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        logging.info("Actualizando token de acceso...")
        gauth.Refresh()
    else:
        logging.info("Autorización exitosa.")
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(credentials_directory)
    credentials = GoogleDrive(gauth)
    return credentials

def upload_file(file_path, folder_id):
    credentials = login()
    file_to_upload = credentials.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                                    "id": folder_id}]})
    file_to_upload['title'] = file_path.split("/")[-1]
    file_to_upload.SetContentFile(file_path)
    file_to_upload.Upload()
    logging.info(f"Archivo '{file_path}' subido exitosamente a Google Drive.")

def classify_decade(year):
    if 1950 <= year < 1960:
        return 1950
    elif 1960 <= year < 1970:
        return 1960
    elif 1970 <= year < 1980:
        return 1970
    elif 1980 <= year < 1990:
        return 1980
    elif 1990 <= year < 2000:
        return 1990
    elif 2000 <= year < 2010:
        return 2000
    elif 2010 <= year < 2020:
        return 2010
    else:
        return 999

def merge(**kwargs):
    ti = kwargs["ti"]
    json_data = json.loads(ti.xcom_pull(task_ids="transform_db"))
    grammy_df = pd.json_normalize(data=json_data)

    json_data = json.loads(ti.xcom_pull(task_ids="transform_csv"))
    spotify_df = pd.json_normalize(data=json_data)

    merge_df = spotify_df.merge(grammy_df, how="inner", left_on='track_name', right_on='nominee')
    merge_df = merge_df.drop_duplicates(subset=['grammy_id'])
    merge_df = merge_df.drop(['artists', 'nominee'], axis=1)
    merge_df['decade'] = merge_df['year'].apply(classify_decade)

    logging.info("Se ha realizado la fusión de datos con éxito.")
    return merge_df.to_json(orient='records')

def load(**kwargs):
    ti = kwargs["ti"]
    json_data = json.loads(ti.xcom_pull(task_ids="merge"))
    data = pd.json_normalize(data=json_data)

    logging.info("Cargando datos...")
    
    db_operations.insert_data(data)
    
    logging.info("Los datos se han cargado en: tracks")

def store(**kwargs):
    ti = kwargs["ti"]
    json_data = json.loads(ti.xcom_pull(task_ids="merge"))
    data = pd.json_normalize(data=json_data)
    data.to_csv('./dataset/data.csv')

    upload_file('./dataset/data.csv', '1KPtdh_iCBpPc_6WDjKLNetMzjGsYnDi-')
    logging.info("Archivo 'data.csv' almacenado y subido a Google Drive.")