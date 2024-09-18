import psycopg2
from minio import Minio
from minio.error import S3Error
import config
import cx_Oracle
from datetime import datetime
import sql_scripts


def create_pg_conn(
        pg_host: str,
        pg_port: str,
        pg_database: str,
        pg_user: str,
        pg_password: str
):
    try:
        pg_conn = psycopg2.connect(dbname=pg_database, user=pg_user, password=pg_password, host=pg_host, port=pg_port)
    except:
        raise Exception("could not create a connection to Postgres database")
    return pg_conn


def close_pg_conn(pg_client):
    if pg_client is not None:
        pg_client.close()


def create_minio_client(endpoint: str,
                    access_key: str,
                    secret_key: str):
    try:
        minio_client = Minio(endpoint,
                       access_key,
                       secret_key,
                       secure=False
                       )
    except S3Error as exc:
        print("error occurred.", exc)
    return minio_client

def create_ora_conn(ora_user: str,
                    ora_password: str,
                    ora_ip: str,
                    ora_port: int,
                    ora_service_name: str):
    try:
        dsn_tns = cx_Oracle.makedsn(ora_ip, ora_port, service_name=ora_service_name)
        oracle_conn = cx_Oracle.connect(ora_user, ora_password, dsn_tns)
    except:
        raise Exception("could not create a connection to Oracle database")
    return oracle_conn


def close_ora_conn(ora_client):
    if ora_client is not None:
        ora_client.close()


if __name__ == '__main__':
    startTime = datetime.now()

    #pg
    pg_conn = create_pg_conn(config.pg_host, config.pg_port, config.pg_database, config.pg_user, config.pg_password)
    pg_conn.autocommit = True
    pg_cursor = pg_conn.cursor()
    date_threshold = datetime.strptime(config.create_date, '%Y-%m-%d %H:%M:%S')
    date_threshold_str = date_threshold.strftime('%Y-%m-%d %H:%M:%S')
    pg_cursor.execute(sql_scripts.pg_get_data, (date_threshold_str,))

    #minio
    minio_client = create_minio_client(config.minio_host, config.minio_user, config.minio_password)

    #ora
    cur_ora_conn = create_ora_conn(config.ora_user, config.ora_password,
                                 config.ora_ip, config.ora_port, config.ora_service_name)
    cur_ora_conn.autocommit = True
    ora_cursor = cur_ora_conn.cursor()
    try:
        while True:
            row = pg_cursor.fetchone()
            print(row)
            if not row:
                break
            content_uid = row[0].replace("-", "").upper()
            create_date = row[1]
            year_str = create_date.strftime("%Y")
            yyyymmdd_str = create_date.strftime("%Y%m%d")
            two_digits = content_uid[:2].upper()
            context = row[27]
            bucket_name = str("filestore-" + context + "-" + year_str)
            object_key = f"{yyyymmdd_str}/{two_digits}/{content_uid}"
            response = minio_client.get_object(bucket_name, object_key)
            file_content = response.read()
            #print(file_content)


    except (Exception, cx_Oracle.Error, psycopg2.Error) as error:
        print(f"Error: {error}")
    pg_cursor.close()
    close_pg_conn(pg_conn)