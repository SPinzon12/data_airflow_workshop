import pandas as pd
import json
import logging

def categorizar_tempo(tempo):
    if 40 <= tempo <= 108:
        return 'Lento'
    elif 108 < tempo <= 168:
        return 'Moderado'
    elif 168 < tempo <= 216:
        return 'Rápido'
    else:
        return 'Extremadamente Rápido'

def read_csv():
    spotify_df = pd.read_csv("./dataset/spotify_dataset.csv")
    logging.info("Extracción finalizada")
    return spotify_df.to_json(orient='records')

def transform_csv(**kwargs):
    ti = kwargs["ti"]
    json_data = json.loads(ti.xcom_pull(task_ids="read_csv"))
    spotify_df = pd.json_normalize(data=json_data)

    spotify_df['track_name_group'] = spotify_df['track_name'].str.lower()
    popular_songs_df = spotify_df.groupby(['track_name_group', 'artists'])['popularity'].idxmax()
    most_popular_songs = spotify_df.loc[popular_songs_df].drop(columns=['track_name_group'])
    spotify_df = most_popular_songs
    spotify_df['duration'] = spotify_df['duration_ms'] / 60000
    spotify_df['duration'] = spotify_df['duration'].round(2)
    spotify_df['tempo_categorizado'] = spotify_df['tempo'].apply(categorizar_tempo)
    spotify_df['artists'] = spotify_df['artists'].str.split(';').str.get(0)
    selected_columns = ["track_name", "tempo_categorizado", "duration", "danceability","acousticness", "speechiness", "artists"]
    spotify_df = spotify_df[selected_columns]
    spotify_df = spotify_df.rename(columns={'tempo_categorizado': 'tempo'})
    spotify_df['danceability'] = spotify_df['danceability'].round(2)
    spotify_df['acousticness'] = spotify_df['acousticness'].round(2)
    spotify_df['speechiness'] = spotify_df['speechiness'].round(2)

    logging.info(f"Transformaciones finalizadas")
    return spotify_df.to_json(orient='records')