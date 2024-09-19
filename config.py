stand = 'eis3'

ora_user = 'system'
ora_password = 'SYSTEM'
ora_ip = 'eis-db-oracle-rezfstore01.eis3.fk.dks.lanit.ru'
ora_port = 1521
ora_service_name = 'rezfs.zakupki.gov.ru'
sid = 'rezfstoredb'

pg_database = 'filestore_db'
pg_host = 'eis-db-unfsd.eis3.fk.dks.lanit.ru'
#pg_host = '127.0.0.1'
pg_port = '5432'
pg_user = 'fs_main_rw'
pg_password = 'fs_main_rw'
create_date = '2024-08-06 10:30:00'

minio_user = 'minioadmin'
minio_password = 'minioadmin'
minio_host = '01.eis3.fk.dks.lanit.ru:9091'

num_threads = 5

minio_list = ['eis-minio-ebdfs', 'eis-minio-fksdfs', 'lkp-minio-lkpfs', 'eis-minio-rkshardfs', 'eis-minio-rdikfs', 'fz223-minio-fz223fs']

context_minio_mapping = {'bc': 'eis-minio-ebdfs',
                        'rgk2': 'eis-minio-ebdfs',
                        'rbg': 'eis-minio-ebdfs',
                        'rgk': 'eis-minio-ebdfs',
                        'rskp': 'eis-minio-ebdfs',
                        'roko': 'eis-minio-fksdfs',
                        'rpg': 'eis-minio-fksdfs',
                        'rpz': 'eis-minio-fksdfs',
                        'audit': 'eis-minio-fksdfs',
                        'rko': 'eis-minio-fksdfs',
                        'rd': 'eis-minio-fksdfs',
                        'rpgz': 'eis-minio-fksdfs',
                        'dizk': 'eis-minio-fksdfs',
                        'pricereq': 'eis-minio-fksdfs',
                        'ktru': 'eis-minio-fksdfs',
                        'rpec': 'eis-minio-fksdfs',
                        'fs_rsktru': 'eis-minio-fksdfs',
                        'rsktru': 'eis-minio-fksdfs',
                        'oboz': 'eis-minio-fksdfs',
                        'rep': 'eis-minio-fksdfs',
                        'rkpo': 'eis-minio-fksdfs',
                        'rpnz': 'eis-minio-fksdfs',
                        'npa': 'eis-minio-fksdfs',
                        'rau': 'eis-minio-fksdfs',
                        'agr': 'eis-minio-fksdfs',
                        'btk': 'eis-minio-fksdfs',
                        'ropt': 'eis-minio-fksdfs',
                        'rirz': 'eis-minio-fksdfs',
                        'proz': 'eis-minio-fksdfs',
                        'priz': 'eis-minio-fksdfs',
                        'ris': 'eis-minio-fksdfs',
                        'ppa': 'eis-minio-fksdfs',
                        'pbo': 'eis-minio-fksdfs',
                        'routes': 'eis-minio-fksdfs',
                        'rec': 'eis-minio-fksdfs',
                        'fs_eacts': 'lkp-minio-lkpfs',
                        'eacts': 'lkp-minio-lkpfs',
                        'fs_els': 'lkp-minio-lkpfs',
                        'els': 'lkp-minio-lkpfs',
                        'fs_rsd': 'lkp-minio-lkpfs',
                        'rsd': 'lkp-minio-lkpfs',
                        'fs_complaint': 'lkp-minio-lkpfs',
                        'complaint': 'lkp-minio-lkpfs',
                        'pzkp': 'lkp-minio-lkpfs',
                        'rgk3': 'eis-minio-rkshardfs',
                        'rdik': 'eis-minio-rdikfs',
                        'fz223': 'fz223-minio-fz223fs',
                        'controls': 'eis-minio-fksdfs',
                        'rsok': 'eis-minio-fksdfs'
                        }