import pandas as pd
import json
import logging
import db_operations

def read_db():
    grammy_df = db_operations.run_query()
    logging.info("Extracción finalizada")
    logging.debug('Los datos extraídos son: ', grammy_df)
    return grammy_df.to_json(orient='records')

def transform_db(**kwargs):
    ti = kwargs["ti"]
    json_data = json.loads(ti.xcom_pull(task_ids="read_db"))
    grammy_df = pd.json_normalize(data=json_data)
    
    grammy_df = grammy_df[grammy_df['artist'] != 'NaN']
    grammy_df = grammy_df[['winner', 'nominee', 'grammy_id', 'artist', 'year']]
    grammy_df = grammy_df.rename(columns={'winner': 'is_nominee'})

    logging.info(f"Los datos transformados son: {grammy_df}")
    return grammy_df.to_json(orient='records')

