import psycopg2
from minio import Minio
from minio.error import S3Error
import config
import cx_Oracle
from datetime import datetime
import sql_scripts
import threading

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

def migrate(thred_num):
    #pg
    pg_conn = create_pg_conn(config.pg_host, config.pg_port, config.pg_database, config.pg_user, config.pg_password)
    pg_conn.autocommit = True
    pg_cursor = pg_conn.cursor()
    date_threshold = datetime.strptime(config.create_date, '%Y-%m-%d %H:%M:%S')
    date_threshold_str = date_threshold.strftime('%Y-%m-%d %H:%M:%S')
    pg_cursor.execute(sql_scripts.pg_get_data, (date_threshold_str,config.num_threads, thred_num))

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
            #print(row)
            if not row:
                break
            content_uid = row[8].replace("-", "").upper()
            create_date = row[9]
            year_str = create_date.strftime("%Y")
            yyyymmdd_str = create_date.strftime("%Y%m%d")
            two_digits = content_uid[:2].upper()
            context = row[1]
            bucket_name = str("filestore-" + context + "-" + year_str)
            object_key = f"{yyyymmdd_str}/{two_digits}/{content_uid}"
            file_content = minio_client.get_object(bucket_name, object_key).read()
            lob = ora_cursor.var(cx_Oracle.BLOB)
            lob.setvalue(0, file_content)
            #print(file_content)
            file_uid_ins = row[0].replace("-", "").upper()
            context_ins = row[1]
            file_name_ins = row[2]
            state_ins = row[3]
            state_after_handlers_ins = row[4]
            create_date_fm_ins = row[5]
            update_date_fm_ins = row[6]
            content_location_ins = row[7]
            content_uid_ins = row[8].replace("-", "").upper()
            create_date_ins = row[9]
            upload_date_ins = row[10]
            mime_type_id_ins = row[11]
            upload_status_ins = row[12]
            file_size_ins = row[13]
            sign_gost34_ins = row[14]
            sign_sha256_ins = row[15]
            crypto_date_ins = row[16]
            crypto_status_ins = row[17]
            crypto_message_ins = row[18]
            av_check_date_ins = row[19]
            av_check_status_ins = row[20]
            av_check_message_ins = row[21]
            converted_content_uid_ins = row[22]
            if converted_content_uid_ins is not None:
                converted_content_uid_ins = converted_content_uid_ins.replace("-", "").upper()
            convert_date_ins = row[23]
            convert_status_ins = row[24]
            convert_message_ins = row[25]
            macro_check_date_ins = row[26]
            macro_check_status_ins = row[27]
            macro_check_message_ins = row[28]
            forbidden_check_date_ins = row[29]
            forbidden_check_status_ins = row[30]
            forbidden_check_result_ins = row[31]
            forbidden_check_message_ins = row[32]
            container_name_ins = row[33]
            ora_cursor.execute(sql_scripts.ora_insert, file_uid=file_uid_ins, context=context_ins,
                               file_name=file_name_ins, state=state_ins,
                               state_after_handlers=state_after_handlers_ins,
                               create_date_fm=create_date_fm_ins, update_date_fm=update_date_fm_ins,
                               content_location=content_location_ins, content_uid=content_uid_ins,
                               create_date=create_date_ins, upload_date=upload_date_ins,
                               mime_type_id=mime_type_id_ins, upload_status=upload_status_ins,
                               file_size=file_size_ins, sign_gost34=sign_gost34_ins, sign_sha256=sign_sha256_ins,
                               crypto_date=crypto_date_ins, crypto_status=crypto_status_ins,
                               crypto_message=crypto_message_ins, av_check_date=av_check_date_ins,
                               av_check_status=av_check_status_ins, av_check_message=av_check_message_ins,
                               converted_content_uid=converted_content_uid_ins, convert_date=convert_date_ins,
                               convert_status=convert_status_ins, convert_message=convert_message_ins,
                               macro_check_date=macro_check_date_ins, macro_check_status=macro_check_status_ins,
                               macro_check_message=macro_check_message_ins,
                               forbidden_check_date=forbidden_check_date_ins,
                               forbidden_check_status=forbidden_check_status_ins,
                               forbidden_check_result=forbidden_check_result_ins,
                               forbidden_check_message=forbidden_check_message_ins,
                               container_name=container_name_ins, file_content=lob)
            try:
                pg_conn.cursor().execute(sql_scripts.pg_upd, (row[0],))
            except Exception as e:
                print(f"Ошибка при обновлении данных в PostgreSQL: {e}")
    except (Exception, cx_Oracle.Error, psycopg2.Error) as error:
        print(f"Error: {error}")
    finally:
        # Закрываем курсоры и соединения
        ora_cursor.close()
        cur_ora_conn.close()
        pg_cursor.close()
        pg_conn.close()

if __name__ == '__main__':
    startTime = datetime.now()

    # Запускаем потоки
    threads = []
    for i in range(config.num_threads):
        thread = threading.Thread(target=migrate, args=(i,))
        threads.append(thread)
        thread.start()

    # Ждем завершения потоков
    for thread in threads:
        thread.join()

    endTime = datetime.now()
    print ("Время выполнения: ", endTime - startTime)