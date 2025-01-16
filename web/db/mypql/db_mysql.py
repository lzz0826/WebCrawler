import pymysql
from web.config.yaml_config import Global


def insert_data(obj):
    conn = pymysql.connect(
        host=str(Global.yml_data['datasource']['host']),
        port=int(Global.yml_data['datasource']['port']),
        user=str(Global.yml_data['datasource']['username']),
        password=str(Global.yml_data['datasource']['password']),
        database=str(Global.yml_data['datasource']['database']),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            conn.commit()
            values = (
                obj.id, obj.source, obj.article_id, obj.title, str(obj.tags), obj.content, str(obj.images),
                obj.source_url, obj.download_url, obj.folder_path, obj.status, obj.memo, obj.update_time,
                obj.create_time
            )
            insert_query = '''
                INSERT IGNORE INTO article (id, source, article_id, title,tags , content, images, source_url, download_url, folder_path, status, memo, update_time, create_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, values)
            conn.commit()
    finally:
        conn.close()


def count_data(source, article_id):
    conn = pymysql.connect(
        host=str(Global.yml_data['datasource']['host']),
        port=int(Global.yml_data['datasource']['port']),
        user=str(Global.yml_data['datasource']['username']),
        password=str(Global.yml_data['datasource']['password']),
        database=str(Global.yml_data['datasource']['database']),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            count_query = '''
                SELECT COUNT(*) AS count FROM article WHERE source = %s AND article_id = %s
            '''
            cursor.execute(count_query, (source, article_id))
            result = cursor.fetchone()
            count = result['count']
            return count
    finally:
        conn.close()


def insert_analyze(obj):
    conn = pymysql.connect(
        host=str(Global.yml_data['datasource']['host']),
        port=int(Global.yml_data['datasource']['port']),
        user=str(Global.yml_data['datasource']['username']),
        password=str(Global.yml_data['datasource']['password']),
        database=str(Global.yml_data['datasource']['database']),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            conn.commit()
            values = (
                obj.id, obj.articl_id, obj.source, obj.provider, str(obj.file_size), obj.md5, obj.upload_start_time,
                obj.upload_end_time, obj.download_start_time, obj.download_end_time
            )
            insert_query = '''
                INSERT IGNORE INTO article_analyze (id, articl_id, source, provider,file_size , md5, upload_start_time, 
                upload_end_time, download_start_time, download_end_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, values)
            conn.commit()
    finally:
        conn.close()