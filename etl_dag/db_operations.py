import psycopg2
import pandas as pd
import json

def create_connection():
    try:
        with open('./etl_dag/db_config.json') as file:
            config = json.load(file)
        cnx = psycopg2.connect(
            host='localhost',
            user=config["user"],
            password=config["password"],
            database=config["database"]
        )
        print('Conexión exitosa!!')
    except psycopg2.Error as e:
        cnx = None
        print('No se puede conectar:', e)
    return cnx

def run_query():
    sql='''SELECT *
    FROM grammy
    '''
    cnx = create_connection()
    cur = cnx.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [col[0] for col in cur.description]
    df = pd.DataFrame(rows)
    df.rename(columns=dict(zip(range(len(columns)), columns)), inplace=True)  
    cnx.close()
    return df

def create_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS tracks (
        track_name VARCHAR(255) NOT NULL,
        tempo VARCHAR(255) NOT NULL,
        duration FLOAT NOT NULL,
        danceability FLOAT NOT NULL,
        acousticness FLOAT NOT NULL,
        speechiness FLOAT NOT NULL,
        is_nominee BOOLEAN NOT NULL,
        grammy_id INT NOT NULL,
        artist VARCHAR(255) NOT NULL,
        year INT NOT NULL,
        decade INT NOT NULL
    );
    '''
    cxn = None
    try:
        cnx = create_connection()
        cur = cnx.cursor()
        cur.execute(create_table_query)
        cur.close()
        cnx.commit()
        print('Tabla creada exitosamente')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cnx is not None:
            cnx.close()

def insert_data(df):
    column_names = df.columns.tolist()
    insert_query = f"""
        INSERT INTO tracks({", ".join(column_names)})
        VALUES ({", ".join(["%s"] * len(column_names))})
    """
    cxn = None
    try:
        create_table()
        cnx = create_connection()
        cur = cnx.cursor()
        for index, row in df.iterrows():
            values = tuple(row)
            cur.execute(insert_query, values)
        cur.close()
        cnx.commit()
        print("Datos insertados exitosamente desde el DataFrame.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cnx is not None:
            cnx.close()