#test
pg_get_data = u"""
select fm.file_uid,
    fm.context,
    fm.file_name,
    fm.state,
    fm.state_after_handlers,
    fm.create_date,
    fm.update_date,
    fm.content_location,
    cm.content_uid,
    cm.create_date,
    cm.upload_date,
    cm.mime_type_id,
    cm.upload_status,
    cm.file_size,
    cm.gost34_hash,
    cm.sha256_hash,
    cm.crypto_date,
    cm.crypto_status,
    cm.crypto_message,
    cm.av_check_date,
    cm.av_check_status,
    cm.av_check_message,
    cm.converted_content_uid,
    cm.convert_date,
    cm.convert_status,
    cm.convert_message,
    cm.macro_check_date,
    cm.macro_check_status,
    cm.macro_check_message,
    cm.forbidden_check_date,
    cm.forbidden_check_status,
    cm.forbidden_check_result,
    cm.forbidden_check_message,
    cm.container_name
from fs_main.content_metadata cm
join fs_main.file_metadata fm 
on cm.content_uid = fm.content_uid
where cm.create_date >= %s
and not fm.is_migrated;
"""

ora_insert = """
insert into FS_MAIN.FILE_AND_CONTENT_METADATA (FILE_UID, CONTEXT, FILE_NAME, STATE, STATE_AFTER_HANDLERS, CREATE_DATE_FM, UPDATE_DATE_FM,
CONTENT_LOCATION, CONTENT_UID, CREATE_DATE, UPLOAD_DATE,
MIME_TYPE_ID, UPLOAD_STATUS, FILE_SIZE, SIGN_GOST34, SIGN_SHA256, CRYPTO_DATE, CRYPTO_STATUS,
CRYPTO_MESSAGE, AV_CHECK_DATE, AV_CHECK_STATUS, AV_CHECK_MESSAGE, CONVERTED_CONTENT_UID,
CONVERT_DATE, CONVERT_STATUS, CONVERT_MESSAGE, MACRO_CHECK_DATE, MACRO_CHECK_STATUS,
MACRO_CHECK_MESSAGE, FORBIDDEN_CHECK_DATE, FORBIDDEN_CHECK_STATUS, FORBIDDEN_CHECK_RESULT, FORBIDDEN_CHECK_MESSAGE,
CONTAINER_NAME, FILE_CONTENT)
values (:file_uid, :context, :file_name, :state, :state_after_handlers, :create_date_fm, :update_date_fm,
:content_location, :content_uid, :create_date, :upload_date,
:mime_type_id, :upload_status, :file_size, :sign_gost34, :sign_sha256, :crypto_date, :crypto_status,
:crypto_message, :av_check_date, :av_check_status, :av_check_message, :converted_content_uid,
:convert_date, :convert_status, :convert_message, :macro_check_date, :macro_check_status,
:macro_check_message, :forbidden_check_date, :forbidden_check_status, :forbidden_check_result, :forbidden_check_message,
:container_name, :file_content)
"""

pg_upd = """
update fs_main.file_metadata
set is_migrated = true
where file_uid = %s
"""

ora_merge = """

"""