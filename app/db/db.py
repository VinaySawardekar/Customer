from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

USER = os.getenv('DB_USER')
HOST = os.getenv('DB_HOST')
PASSWORD = os.getenv('DB_PASSWORD')

conn = pymysql.connect(
    database="customer",
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=3306
)


