from minio import Minio
from minio.error import S3Error

# Создаем клиент MinIO
client = Minio(
    "localhost:9000",
    access_key="myaccesskey",
    secret_key="mysecretpassword",
    secure=False  # Убедитесь, что этот флаг установлен в False, если вы работаете локально и не используете HTTPS
)

# Параметры файла
bucket_name = "achievements"  # Имя вашего бакета
file_path = "path/to/your/local_image.svg"  # Путь к вашему локальному файлу
file_name = "image.svg"  # Имя файла в MinIO

# Создаем бакет, если его еще нет
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

# Загружаем файл в MinIO
try:
    client.fput_object(
        bucket_name,
        file_name,
        file_path,
        content_type="image/svg+xml"
    )
    print(f"Файл {file_name} успешно загружен в бакет {bucket_name}.")
except S3Error as e:
    print(f"Ошибка загрузки файла: {e}")
