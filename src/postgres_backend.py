import os

import psycopg2
import psycopg2.extensions


params = {
    "host": os.environ['POSTGRES_HOST'],
    "port": os.environ['POSTGRES_PORT'],
    "user": "postgres"
}
conn = psycopg2.connect(**params)

psycopg2.extensions.register_type(
    psycopg2.extensions.UNICODE,
    conn
)
conn.set_isolation_level(
    psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
)
cursor = conn.cursor()

def read_links_mapping(short_url = None):
    res_dict = {}
    if short_url is None:
        url_filter = ""
    else:
        url_filter = f"""
            WHERE
                short_url = '{short_url}'
        """
    sql_str = f"""
        SELECT 
            short_url, origin_url
        FROM short_links
        {url_filter}
    """
    # выгружаем данные из БД в Python
    cursor.execute(sql_str)
    data = [a for a in cursor.fetchall()]
    for i in data:
        res_dict[i[0]] = i[1]
    return res_dict


def insert_links(urls_dict):
    arr = [
        (k, v) for k, v in urls_dict.items()
    ]
    insert_query = f"INSERT INTO short_links (short_url, origin_url) VALUES (%s, %s)"

    for row in arr:
        cursor.execute(insert_query, (row[0], row[1]))
    conn.commit()
